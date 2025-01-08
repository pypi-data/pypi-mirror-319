import os
import gradio as gr
import json
from pathlib import Path
from argparse import Namespace
from functools import wraps
from typing import Union, Tuple, Literal, Iterable, Dict, Any, Callable, overload
from waifuset import logging, tagging

WAIFUI_ROOT = Path(__file__).parent
JSON_ROOT = WAIFUI_ROOT / 'json'

TAGS_COLUMN = 'tags'
DESCRIPTION_COLUMN = 'description'

logger = logging.get_logger('UI')


def search_file(filename, search_path):
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            return os.path.abspath(os.path.join(root, filename))
    return None


SORTING_METHODS: Dict[str, Callable] = {}

FORMAT_PRESETS = {
    'train': tagging.fmt2train,
    'prompt': tagging.fmt2std,
    'danbooru': tagging.fmt2danbooru,
    'awa': tagging.fmt2awa,
    'unescape': tagging.fmt2unescape,
    'escape': tagging.fmt2escape,
}

SCORER2SCORE2QUALITY_FILENAME = 'score2quality.json'
SCORER2SCORE2QUALITY_PATH = search_file(SCORER2SCORE2QUALITY_FILENAME, JSON_ROOT)
if SCORER2SCORE2QUALITY_PATH is None:
    logger.warning(
        "Cannot find the \"{}\" file from {}. The quality score will not be displayed.".format(
            SCORER2SCORE2QUALITY_FILENAME,
            logging.yellow(f"{JSON_ROOT}/.../{SCORER2SCORE2QUALITY_FILENAME}.json")
        ))
else:
    # logger.debug(f'Find score2quality file at: {logging.yellow(SCORE2QUALITY_PATH)}')
    pass
SCORER2SCORE2QUALITY = None

TRANSLATION_EN2CN = None
TRANSLATION_CN2EN = None
TRANSLATION_TABLE_FILENAME = 'translation_cn.json'
TRANSLATION_TABLE_PATH = search_file(TRANSLATION_TABLE_FILENAME, JSON_ROOT)
if TRANSLATION_TABLE_PATH is None:
    logger.warning("Cannot find the translation file from {}. The language is set to English".format(logging.yellow(f"{JSON_ROOT}/.../{TRANSLATION_TABLE_FILENAME}")))
else:
    # logger.debug(f'Find translation file at: {logging.yellow(TRANSLATION_TABLE_PATH)}')
    pass

# typing
DataDict = Dict[str, Any]
ResultDict = Dict[str, Any]


class UIState(Namespace):
    pass


class UITab:
    def __init__(self, tab: gr.Tab):
        self.tab = tab


class UIBuffer(object):
    def __init__(self):
        self.buffer = {}

    def get(self, key):
        return self.buffer.get(key, None)

    def keys(self):
        return self.buffer.keys()

    def do(self, key, value):
        self.buffer.setdefault(key, ([], []))
        self.buffer[key][0].append(value.copy())
        self.buffer[key][1].clear()

    def delete(self, key):
        if key not in self.buffer:
            return None
        del self.buffer[key]

    def undo(self, key):
        if key not in self.buffer or len(self.buffer[key][0]) == 1:
            return None
        self.buffer[key][1].append(self.buffer[key][0].pop())
        return self.buffer[key][0][-1]

    def redo(self, key):
        if key not in self.buffer or not self.buffer[key][1]:
            return None
        self.buffer[key][0].append(self.buffer[key][1].pop())
        return self.buffer[key][0][-1]

    def latest(self, key):
        r"""
        Return the latest value of the key in the buffer.
        """
        if key not in self.buffer or len(self.buffer[key][0]) <= 1:
            return None
        return self.buffer[key][0][-1]

    def latests(self) -> Dict[str, Any]:
        r"""
        Return the latest value of each key in the buffer.
        """
        latests = {key: self.latest(key) for key in self.keys()}
        latests = {key: value for key, value in latests.items() if value is not None}
        return latests

    def __contains__(self, key):
        return key in self.buffer

    def __len__(self):
        return len(self.buffer)


class UIGallerySelectData:
    def __init__(self, index=None, key=None):
        self.index = index
        self.key = key

    @ overload
    def select(self, selected: gr.SelectData): ...

    @ overload
    def select(self, selected: Tuple[int, str]): ...

    def select(self, selected: Union[gr.SelectData, Tuple[int, str]]):
        if isinstance(selected, gr.SelectData):
            self.index = selected.index
            image_filename = selected.value['image']['orig_name']
            img_key = os.path.basename(os.path.splitext(image_filename)[0])
            self.key = img_key
        elif isinstance(selected, tuple):
            self.index, self.key = selected
        elif selected is None:
            self.index, self.key = None, None
        else:
            raise NotImplementedError


def EmojiButton(value, variant: Literal['primary', 'secondary', 'stop'] = "secondary", scale=0, min_width=40, *args, **kwargs):
    return gr.Button(value=value, variant=variant, scale=scale, min_width=min_width, *args, **kwargs)


def track_progress(progress: gr.Progress, desc=None, total=None, n=1):
    progress.n = 0  # initial call
    progress(0, desc=desc, total=total)

    def wrapper(func):
        def inner(*args, **kwargs):
            res = func(*args, **kwargs)
            progress.n += n
            progress((progress.n, total), desc=desc, total=total)
            return res
        return inner
    return wrapper


def open_file_folder(path: str):
    print(f"Open {path}")
    if path is None or path == "":
        return

    command = f'explorer /select,"{path}"'
    os.system(command)


def init_cn_translation():
    global TRANSLATION_EN2CN, TRANSLATION_CN2EN
    if TRANSLATION_EN2CN is not None and TRANSLATION_CN2EN is not None:
        return
    try:
        with open(TRANSLATION_TABLE_PATH, 'r', encoding='utf-8') as f:
            TRANSLATION_EN2CN = json.load(f)
        TRANSLATION_EN2CN = {k.lower(): v for k, v in TRANSLATION_EN2CN.items()}
        TRANSLATION_CN2EN = {v: k for k, v in TRANSLATION_EN2CN.items()}
    except FileNotFoundError:
        TRANSLATION_EN2CN = {}
        TRANSLATION_CN2EN = {}
        logger.warning(f'Cannot find the translation file from {logging.yellow(f"{JSON_ROOT}/.../{TRANSLATION_TABLE_FILENAME}")}')
    except Exception as e:
        TRANSLATION_EN2CN = {}
        TRANSLATION_CN2EN = {}
        logger.warning(f'Failed to load the translation file. Error: {e}')


def en2cn(text):
    if text is None:
        return None
    init_cn_translation()
    return TRANSLATION_EN2CN.get(text.strip().replace('_', ' ').lower(), text)


def cn2en(text):
    if text is None:
        return None
    init_cn_translation()
    return TRANSLATION_CN2EN.get(text.strip().replace('_', ' ').lower(), text)


def translate(text, language='en'):
    translator = {
        'en': cn2en,
        'cn': en2cn,
    }
    translator = translator.get(language, cn2en)
    if isinstance(text, str):
        return translator(text)
    elif isinstance(text, Iterable):
        return [translator(t) for t in text]
    else:
        raise TypeError(f'Unsupported type: {type(text)}')


def get_scorer2score2quality():
    global SCORER2SCORE2QUALITY
    if SCORER2SCORE2QUALITY is not None:
        return SCORER2SCORE2QUALITY
    try:
        with open(SCORER2SCORE2QUALITY_PATH, 'r', encoding='utf-8') as f:
            SCORER2SCORE2QUALITY = json.load(f)
        SCORER2SCORE2QUALITY = {name: {k: v for k, v in sorted(quality2score.items(), key=lambda item: item[1], reverse=True)} for name, quality2score in SCORER2SCORE2QUALITY.items()}
    except FileNotFoundError:
        SCORER2SCORE2QUALITY = {}
        raise gr.Error('Cannot find the quality2score file from {}'.format(logging.yellow(f"{JSON_ROOT}/.../quality2score.json")))
    except Exception as e:
        SCORER2SCORE2QUALITY = {}
        raise gr.Error('Failed to load `score2quality.json`. Error: %s' % e)
    return SCORER2SCORE2QUALITY


def convert_score2quality(score, scorer_type: Literal['ws4', 'as2']):
    scorer2score2quality = get_scorer2score2quality()
    score2quality = scorer2score2quality.get(scorer_type)
    if score2quality is None:
        return None
    for quality, score_range in score2quality.items():
        if score >= score_range:
            return quality
    return None


def kwargs_setter(func, **preset_kwargs):
    @ wraps(func)
    def wrapper(*args, **kwargs):
        kwargs.update(preset_kwargs)
        return func(*args, **kwargs)
    return wrapper


def patch_image_path_base_info(img_md):
    if not (img_path := img_md.get('image_path')):
        return None
    img_path = Path(img_path)
    if 'image_key' not in img_md:
        img_md['image_key'] = img_path.stem
    if 'category' not in img_md:
        img_md['category'] = img_path.parent.name
    if 'source' not in img_md:
        img_md['source'] = img_path.parent.parent.name
    return img_md


def patch_dirset(img_md):
    img_md = patch_image_path_base_info(img_md)
    img_md['caption'] = None
    return img_md
