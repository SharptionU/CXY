import gettext
from typing import Callable
from fastapi import Request, HTTPException

from core.config import settings

try:
    lang_cfg = settings.language

except Exception as e:
    raise Exception("language config not found")

# 缓存已加载的翻译，避免重复加载
_translations_cache: dict[str, gettext.GNUTranslations] = {}


def load_translations(lang: str):
    """加载指定语言的翻译文件"""
    if lang in _translations_cache:
        return _translations_cache[lang]

    lang = lang_cfg.default if lang not in lang_cfg.support else lang
    # 尝试加载精确匹配的语言
    try:
        translations = gettext.translation(
            domain=lang_cfg.domain,
            localedir=lang_cfg.path,
            languages=[lang],
            fallback=True
        )
        _translations_cache[lang] = translations
        return translations

    except FileNotFoundError:
        pass


def gettext_translator(request: Request) -> Callable:
    """
    依赖项：获取当前请求的翻译函数
    从请求头 Accept-Language 提取第一个语言，返回对应翻译函数
    """
    # 从请求头获取语言偏好，默认使用zh_CN
    accept_language = request.headers.get("Accept-Language", lang_cfg.default).strip()

    # 提取第一个语言（忽略后续内容和质量值）
    # 示例："zh-CN,zh;q=0.9,en;q=0.8" → 取"zh-CN"
    first_lang = accept_language.split(',')[0].split(';')[0].strip()

    # 规范化语言代码（如zh-cn -> zh_CN）
    first_lang.replace("-", "_")
    r = first_lang.split("_")
    if len(r)!= 2:
        valid_lang = lang_cfg.default
    else:
        valid_lang = f"{r[0].lower()}_{r[1].upper()}"
    translations = load_translations(valid_lang)
    return translations.gettext


def test_language():
    print("zh-cn".replace("-", "_"))


if __name__ == '__main__':
    test_language()
