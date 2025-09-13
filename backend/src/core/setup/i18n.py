import i18n

def init_18n():
    i18n.load_path.append("./locales")  # 翻译文件目录
    i18n.set("locale", "zh")  # 默认语言
    i18n.set("fallback", "zh")  # 出错回退语言
    i18n.set("enable_memoization", True)  # 开启内存缓存
