import vkcc.config
from vkcc.config.locales import LOCALES


def translate(key, *args, **kwargs):
    locale = LOCALES[vkcc.config.configuration.get_language()]
    default_locale = LOCALES["DEFAULT"]
    if key in locale:
        return locale[key].format(*args, **kwargs)
    elif key in default_locale:
        return default_locale[key].format(*args, **kwargs)
    else:
        return key
