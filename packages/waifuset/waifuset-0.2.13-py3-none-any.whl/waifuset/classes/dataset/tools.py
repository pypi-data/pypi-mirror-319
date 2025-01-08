import os
from pathlib import Path
from typing import List, Tuple, Dict, Any, Union, Literal
from .dict_dataset import DictDataset
from .auto_dataset import AutoDataset
from .sqlite3_dataset import SQLite3Dataset
from .dataset import Dataset
from .dataset_mixin import FromDiskMixin
from ... import logging, mapping, const

logger = logging.get_logger("dataset")


def get_dataset_cls_from_source(source):
    if issubclass(type(source), Dataset):
        return type(source)
    elif isinstance(source, dict):
        from .dict_dataset import DictDataset
        return DictDataset
    elif isinstance(source, (str, Path)):
        ext = os.path.splitext(source)[1]
        if not ext and os.path.isdir(source):
            from .directory_dataset import DirectoryDataset
            return DirectoryDataset
        elif ext == '.sqlite3' or ext == '.db':
            from .sqlite3_dataset import SQLite3Dataset
            return SQLite3Dataset
        elif ext == '.csv':
            from .csv_dataset import CSVDataset
            return CSVDataset
        elif ext == '.json':
            from .json_dataset import JSONDataset
            return JSONDataset
        else:
            raise NotImplementedError
    elif source is None:
        return None


def get_dataset_from_source(source, dataset_cls=None, **kwargs) -> Dataset:
    ds_cls = get_dataset_cls_from_source(source)
    if issubclass(ds_cls, FromDiskMixin):
        ds = ds_cls.from_disk(source, **kwargs)
    else:
        ds = ds_cls(source, **kwargs)
    if dataset_cls is not None:
        ds = dataset_cls.from_dataset(ds, **kwargs)
    return ds


def dump_dataset_to_disk(dataset: Dataset, fp: str, *args, **kwargs):
    from .dataset_mixin import ToDiskMixin
    cls_ = get_dataset_cls_from_source(fp)
    if not issubclass(cls_, ToDiskMixin):
        raise TypeError(f'{cls_} does not support dump')
    dumpset = cls_.from_dataset(dataset, *args, fp=fp, source=fp, **kwargs)
    dumpset.commit()


def load_fast_dataset(
    *source: List[str],
    merge_mode: Literal['union', 'intersection', 'update', 'no'] = 'union',
    local_only=False,
    dataset_cls=None,
    **default_kwargs,
) -> Union[Dataset, List[Dataset]]:
    verbose = default_kwargs.get('verbose', False)
    source = parse_source_input(source)
    if not source:
        from .dict_dataset import DictDataset
        return (dataset_cls or DictDataset).from_dict({})
    datasets = []
    for i, src in enumerate(source):
        if isinstance(src, Dataset):
            datasets.append(src)
            continue
        name_or_path = src.pop('name_or_path')
        primary_key = src.pop('primary_key', 'image_key')
        if local_only or os.path.exists(name_or_path):
            dataset = load_local_dataset(
                name_or_path,
                dataset_cls=dataset_cls,
                primary_key=primary_key,
                column_mapping=src.pop('column_mapping', default_kwargs.get('column_mapping', None)),
                remove_columns=src.pop('remove_columns', default_kwargs.get('remove_columns', None)),

                fp_key=src.pop('fp_key', default_kwargs.get('fp_key', 'image_path')),
                recur=src.pop('recur', default_kwargs.get('recur', True)),
                exts=src.pop('exts', default_kwargs.get('exts', const.IMAGE_EXTS)),
                tbname=src.pop('tbname', default_kwargs.get('tbname', None)),
                read_attrs=src.pop('read_attrs', default_kwargs.get('read_attrs', False)),
                verbose=src.pop('verbose', verbose),
                **src,
            )
        else:
            dataset = load_huggingface_dataset(
                name_or_path=name_or_path,
                dataset_cls=dataset_cls,
                primary_key=primary_key,
                column_mapping=src.pop('column_mapping', default_kwargs.get('column_mapping', {k: 'image' for k in ('image', 'png', 'jpg', 'jpeg', 'webp', 'jfif')})),
                remove_columns=src.pop('remove_columns', default_kwargs.get('remove_columns', None)),

                cache_dir=src.pop('cache_dir', default_kwargs.get('cache_dir', None)),
                token=src.pop('token', default_kwargs.get('token', None)),
                split=src.pop('split', default_kwargs.get('split', 'train')),
                max_retries=src.pop('max_retries', default_kwargs.get('max_retries', None)),
                verbose=src.pop('verbose', verbose),
                **src,
            )
        if (mapping := src.pop('mapping', None)) is not None:
            dataset = mapping(dataset)
        dataset.priority = src.pop('priority', i)
        datasets.append(dataset)
        logger.info(f"[{i}/{len(source)}] {dataset.name}: ", disable=not verbose)
        logger.info(dataset, no_prefix=True, disable=not verbose)
    if merge_mode != 'no':
        datasets.sort(key=lambda x: x.priority, reverse=True)
        dataset = accumulate_datasets(datasets, mode=merge_mode, verbose=verbose)
        if (mapping := default_kwargs.get('mapping', None)) is not None:
            dataset = mapping(dataset)
    else:
        dataset = datasets
    return dataset


def load_local_dataset(
    name_or_path: str,
    primary_key: str = 'image_key',
    column_mapping: Dict[str, str] = None,
    remove_columns: List[str] = None,
    fp_key: str = 'image_path',
    exts: List[str] = const.IMAGE_EXTS,
    recur: bool = False,
    tbname: str = None,
    read_attrs: bool = False,
    verbose: bool = False,
    dataset_cls: type = None,
    **kwargs: Dict[str, Any],
):
    localset = AutoDataset(
        name_or_path,
        dataset_cls=dataset_cls,
        fp_key=fp_key,
        exts=exts,
        primary_key=primary_key,
        recur=recur,
        tbname=tbname,
        verbose=verbose,
        **kwargs,
    )
    if column_mapping:
        localset = localset.rename_columns(column_mapping, tqdm_disable=True)
    if remove_columns:
        localset = localset.remove_columns(remove_columns, tqdm_disable=True)
    if primary_key not in localset.headers:
        def patch_key(dataset, primary_key) -> Dataset:
            for key, value in dataset.items():
                value[primary_key] = key
            if 'header' in dataset.__dict__ and primary_key not in dataset.header:
                dataset.header.append(primary_key)
            return dataset

        localset = patch_key(localset, primary_key)
    if read_attrs:
        if isinstance(localset, SQLite3Dataset):
            readset = localset.subset('caption', 'is NULL')
            readset.with_map(mapping.attr_reader, tqdm_disable=not verbose)
            localset.update(readset)
        else:
            localset.apply_map(mapping.attr_reader, condition=lambda img_md: img_md.get('caption') is None, tqdm_disable=not verbose)
    return localset


def load_huggingface_dataset(
    name_or_path: str,
    primary_key: str = 'image_key',
    column_mapping: Dict[str, str] = None,
    remove_columns: List[str] = None,
    cache_dir: str = None,
    token: str = None,
    split: str = 'train',
    max_retries: int = None,
    verbose: bool = False,
    dataset_cls: type = None,
    **kwargs: Dict[str, Any],
) -> Dataset:
    r"""
    Load dataset from HuggingFace and convert it to `dataset_cls`.
    """
    import datasets
    import requests
    from ..data.huggingface_data import HuggingFaceData
    try:
        import huggingface_hub.utils._errors
    except ImportError:
        raise ImportError("Please install huggingface-hub by `pip install huggingface-hub` to load dataset from HuggingFace.")
    if dataset_cls is None:
        from .dict_dataset import DictDataset
        dataset_cls = DictDataset
    if isinstance(column_mapping, (list, tuple)):
        column_mapping = {k: k for k in column_mapping}
    retries = 0
    while True:
        try:
            hfset: datasets.Dataset = datasets.load_dataset(
                name_or_path,
                cache_dir=cache_dir,
                split=split,
                token=token,
                **kwargs,
            )
            break
        except (huggingface_hub.utils._errors.HfHubHTTPError, ConnectionError, requests.exceptions.HTTPError, requests.exceptions.ReadTimeout):
            logger.print(logging.yellow(f"Connection error when downloading dataset `{name_or_path}` from HuggingFace. Retrying..."))
            if max_retries is not None and retries >= max_retries:
                raise
            retries += 1
            pass

    if remove_columns:
        hfset = hfset.remove_columns([k for k in hfset.column_names if k in remove_columns])

    column_mapping = column_mapping or {}
    if isinstance(column_mapping, (list, tuple)):
        column_mapping = {k: k for k in column_mapping}
    if '__key__' in hfset.column_names:
        column_mapping['__key__'] = primary_key
    if column_mapping:
        hfset = hfset.rename_columns({k: v for k, v in column_mapping.items() if k != v and k in hfset.column_names})

    dic = {}
    if primary_key not in hfset.column_names:
        for index in range(len(hfset)):
            img_key = str(index)
            dic[img_key] = HuggingFaceData(hfset, index=index, **{primary_key: img_key})
    else:
        for index, img_key in enumerate(hfset[primary_key]):
            dic[img_key] = HuggingFaceData(hfset, index=index, **{primary_key: img_key})
    return dataset_cls.from_dict(dic, verbose=verbose)


def parse_source_input(source: Union[List, Tuple, Dict, str, Path, None]) -> List[Dict[str, Any]]:
    if source is None:
        return []
    if not isinstance(source, (list, tuple)):
        source = [source]
    elif len(source) == 1 and isinstance(source[0], (list, tuple)):
        source = source[0]
    source = [
        dict(name_or_path=src) if isinstance(src, (str, Path))
        else src
        for src in source
    ]
    return source


def accumulate_datasets(datasets, mode: Literal['union', 'intersection', 'update'] = 'union', verbose=True) -> Dataset:
    if not datasets:
        return DictDataset.from_dict({})
    if len(datasets) == 1:
        return datasets[0]
    elif not all(ds.__class__ == datasets[0].__class__ for ds in datasets):
        logger.warning(f"Accumulating datasets with different types: {[ds.__class__.__name__ for ds in datasets]}, the type of the first dataset, DictDataset, will be used.")
        dataset_cls = DictDataset
    else:
        dataset_cls = datasets[0].__class__

    pivot_config = {}
    for ds in datasets:
        pivot_config.update(ds.config)
    pivot_config.pop('name', 'FastDataset')
    pivot_config['verbose'] = verbose
    pivotset = dataset_cls.from_dataset(datasets[0], **pivot_config)
    if 'header' in pivotset.__dict__:
        del pivotset.__dict__['header']
    if mode == 'union':
        img_keys = set()
        for ds in datasets:
            img_keys.update(ds.keys())
            if any(img_key is None for img_key in img_keys):
                logger.error(f"Dataset with None image key: {ds}")
    elif mode == 'intersection':
        img_keys = set(datasets[0].keys())
        for ds in datasets[1:]:
            img_keys.intersection_update(ds.keys())
            if any(img_key is None for img_key in img_keys):
                logger.error(f"Dataset with None image key: {ds}")
    elif mode == 'update':
        pass
    else:
        raise ValueError(f"Invalid mode: {mode}")

    for ds in logger.tqdm(datasets[1:], desc='accumulate datasets', position=1, disable=not verbose):
        if mode == 'update':
            pivotset.update(ds)
        else:
            for img_key in logger.tqdm(img_keys, desc='accumulate data', position=2, disable=not verbose):
                if (new_img_md := ds.get(img_key)) is not None:
                    if (old_img_md := pivotset.get(img_key)) is not None:
                        old_img_md.update(new_img_md)
                        if issubclass(new_img_md.__class__, old_img_md.__class__):
                            new_img_md.update(old_img_md)
                            pivotset[img_key] = new_img_md
                    else:
                        pivotset[img_key] = new_img_md

    if mode == 'intersection':
        for img_key in logger.tqdm(list(pivotset.keys()), desc='remove data', position=2, disable=not verbose):
            if img_key not in img_keys:
                del pivotset[img_key]

    return pivotset
