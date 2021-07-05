from vkcc.settings import SETTINGS

LOCALE_EN = {
    "form.MAIN.title": "VK Console Client",
    "form.LOGIN.title": "Select user or login",
    "form.LOGIN_NEW.title": "Login",

    "popup.TWO_AUTH.title": "Two auth required",

    "button.exit.title": "Exit",
    "button.back.title": "Back",
    "button.cancel.title": "Cancel",
    "button.ok.title": "Ok",
    "button.form.MAIN.login.title": "Login",
    "button.form.MAIN.settings.title": "Settings",
    "button.form.LOGIN.login_new.title": "New user",
    "button.form.LOGIN.login.title": "Login",

    "titletext.form.LOGIN_NEW.login.title": "Login",
    "titletext.popup.TWO_AUTH.code.title": "Code",

    "titlepassword.form.LOGIN_NEW.password.title": "Password",

    "checkbox.form.LOGIN_NEW.remember.title": "Remember me",
    "checkbox.popup.TWO_AUTH.remember.title": "Remember device",

    "img.form.LOGIN.avatar.title": "Login as",
    "img.no.title": "Error",

    "box.form.LOGIN.accounts.title": "Select user"
}


LOCALE_RU = {
    "form.MAIN.title": "Консольный клиент VK",
    "form.LOGIN.title": "Выберите пользователя или войдите",
    "form.LOGIN_NEW.title": "Вход",

    "popup.TWO_AUTH.title": "Требуется двойная аутентификация",

    "button.exit.title": "Выйти",
    "button.back.title": "Назад",
    "button.cancel.title": "Отмена",
    "button.ok.title": "Готово",
    "button.form.MAIN.login.title": "Войти",
    "button.form.MAIN.settings.title": "Настройки",
    "button.form.LOGIN.login_new.title": "Новый пользователь",
    "button.form.LOGIN.login.title": "Войти",

    "titletext.form.LOGIN_NEW.login.title": "Логин",
    "titletext.popup.TWO_AUTH.code.title": "Код",

    "titlepassword.form.LOGIN_NEW.password.title": "Пароль",

    "checkbox.form.LOGIN_NEW.remember.title": "Запомнить меня",
    "checkbox.popup.TWO_AUTH.remember.title": "Запомнить устройство",

    "img.form.LOGIN.avatar.title": "Войти как",
    "img.no.title": "Ошибка",

    "box.form.LOGIN.accounts.title": "Выберете пользователя"
}
LOCALES = {
    "english": LOCALE_EN,
    "russian": LOCALE_RU
}


def __get_locale__():
    lang = SETTINGS.get_language()
    if lang in LOCALES:
        return LOCALES[lang]
    else:
        return LOCALE_EN


def translate(key, *args):
    locale = __get_locale__()
    if key in locale:
        return locale[key].format(*args)
    elif key in LOCALE_EN:
        return LOCALE_EN[key].format(*args)
    else:
        return key + "@[{}]".format(", ".join(args))

