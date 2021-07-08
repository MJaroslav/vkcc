import json
import os
from vkcc.config.locales import LOCALES

CONFIG_DIR = os.path.expanduser("~/.config/vkcc/")
os.makedirs(CONFIG_DIR, exist_ok=True)

CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

ACCOUNTS_FILE = os.path.join(CONFIG_DIR, "accounts.json")

DEFAULT_CONFIGURATION = {
    "selected": "global",
    "profiles": {
        "global": {
            "language": "english",
            "images": {
                "render": {
                    "method": "ueberzug"
                }
            }
        }
    }
}


class Configuration(object):
    def __init__(self):
        self.__data__ = {}
        self.__load__()

    def __load__(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as file:
                self.__data__ = json.load(file)
        else:
            with open(CONFIG_FILE, "w") as file:
                json.dump(DEFAULT_CONFIGURATION, file, indent=4)
            self.__data__ = DEFAULT_CONFIGURATION
        if os.path.exists(ACCOUNTS_FILE):
            with open(ACCOUNTS_FILE, "r") as file:
                self.__accounts__ = json.load(file)

    def __get_option__(self, key, default=None):
        keys = key.split(".")
        data = self.__data__.copy()
        while len(keys) > 1:
            if keys[0] in data:
                data = data[keys[0]]
                del keys[0]
            else:
                return default
        return data[keys[0]] if keys[0] in data else default

    def get_option(self, key, default=None):
        """ Make sure if you use this without call secure checks """
        current_profile = "profiles.{}.{}".format(self.get_profile(), key)
        global_profile = "profiles.global.{}".format(key)
        return self.__get_option__(current_profile, self.__get_option__(global_profile, default))

    def set_option(self, key, value, to_global=False):
        """ Make sure if you use this without call secure checks """
        key = "profiles.global.{}".format(key) if to_global else "profiles.{}.{}".format(self.get_profile(), key)
        keys = key.split(".")
        data = self.__data__
        if len(keys) > 1:
            for _k in keys[:-1]:
                if not (_k in data and isinstance(data[_k], dict)):
                    data.update({_k: {}})  # Add field or force set to dict type
                data = data[_k]
        data.update({keys[-1]: value})
        self.save()

    # profile

    def get_profile(self):
        return self.__get_option__("selected")

    def allowed_profiles(self):
        result = list(self.__get_option__("profiles", {}).keys())
        result.append("global") if "global" not in result else None
        return result

    def set_profile(self, selected):
        self.__data__["selected"] = selected
        self.save()

    # images.render.w3mimgdisplay.path

    def get_w3mimgdisplay(self):
        return self.get_option("images.render.w3mimgdisplay.path")

    # images.render.method

    def get_render_method(self):
        return self.get_option("images.render.method")

    def allowed_render_methods(self):
        return ["ueberzug", "w3mimgdisplay"]

    def set_render_method(self, method, to_global=False):
        self.set_option("images.render.method", method, to_global)

    # images.offset.x and images.offset.y NOT USED

    # def get_images_offset(self):
    #     return self.get_option("images.offset.x", 0), self.get_option("images.offset.y", 0)

    # language

    def get_language(self):
        return self.get_option("language", "english")

    def allowed_languages(self):
        result = list(LOCALES.keys())
        result.remove("DEFAULT")
        return result

    def set_language(self, language, to_global=False):
        self.set_option("language", language, to_global)

    # chars.width and chars.height NOT USED

    # def get_char_scale_size(self):
    #     return self.get_option("chars.width", -1), self.get_option("chars.height", -1)

    def save(self):
        with open(CONFIG_FILE, "w") as file:
            json.dump(self.__data__, file, indent=4)


class Accounts(object):
    def __init__(self):
        self.__accounts__ = {}
        self.__load__()

    def __load__(self):
        if os.path.exists(ACCOUNTS_FILE):
            with open(ACCOUNTS_FILE, "r") as file:
                self.__accounts__ = json.load(file)

    def get(self, index):
        return self.__accounts__[index]

    def get_all(self):
        return self.__accounts__.copy()

    def add(self, user_id, name, token):
        account = {
            "id": user_id,
            "name": name,
            "access_token": token
        }
        self.__accounts__ = [account for account in self.__accounts__ if account["id"] != user_id]
        self.__accounts__.append(account)
        self.save()

    def remove(self, acc):
        self.__accounts__ = [account for account in self.__accounts__ if account["id"] != acc["id"]]
        self.save()

    def save(self):
        with open(ACCOUNTS_FILE, "w") as file:
            json.dump(self.__accounts__, file, indent=4)


accounts = Accounts()
configuration = Configuration()
