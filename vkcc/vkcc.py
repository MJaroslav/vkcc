import npyscreen as nps
import vkcc.utils as utils
import vkcc.localization as l10n
from vkcc.vk import VK
from vkcc.settings import SETTINGS


class App(nps.StandardApp):
    def onStart(self):
        nps.setTheme(nps.Themes.TransparentThemeLightText)
        self.addForm("MAIN", MainForm, name=l10n.translate("form.MAIN.title"))
        self.addForm("LOGIN_NEW", LoginNewForm, name=l10n.translate("form.LOGIN_NEW.title"))
        self.addForm("LOGIN", LoginForm, name=l10n.translate("form.LOGIN.title"))
        self.addForm("PROFILE", VkProfileForm, name="Profile")


class ConfirmCancelPopupTranslated(nps.utilNotify.ConfirmCancelPopup):
    OK_BUTTON_TEXT = l10n.translate("button.ok.title")
    CANCEL_BUTTON_TEXT = l10n.translate("button.cancel.title")
    CANCEL_BUTTON_BR_OFFSET = (2, 15)


def notify_auth_handler():
    f = ConfirmCancelPopupTranslated(name=l10n.translate("popup.TWO_AUTH.title"), color='STANDOUT')
    f.preserve_selected_widget = True

    code = f.add(nps.TitleText, name=l10n.translate("titletext.popup.TWO_AUTH.code.title"))
    remember = f.add(nps.Checkbox, name=l10n.translate("checkbox.popup.TWO_AUTH.remember.title"))

    f.editw = 0
    f.edit()

    return code.value, remember.value


class ImageWidget(nps.wgwidget.Widget):
    def __init__(self, screen, img=None, autohide=True, *args, **keywords):
        super().__init__(screen, *args, **keywords)
        self.__img__ = img
        self.autohide = autohide

    def set_img(self, img):
        self.__img__ = img
        if self.autohide:
            self.hidden = not self.__img__
        self.update()

    def clear(self, usechar=' '):
        super().clear('X')
        self.parent.refresh()
        super().clear(usechar)

    def update(self, clear=True):
        x = self.relx
        y = self.rely
        w = self.width
        h = self.height
        x, y = utils.scale_by_char(x, y)
        w, h = utils.scale_by_char(w, h)
        utils.draw_image(self.__img__, x, y, w, h)


class FormButton(nps.ButtonPress):
    def __init__(self, screen, form=None, *args, **keywords):
        super().__init__(screen, *args, **keywords)
        if self.name:
            self.name += ".."
        self.__form__ = form

    def whenPressed(self):
        if self.__form__:
            self.find_parent_app().switchForm(self.__form__)


class AccountButton(FormButton):
    def __init__(self, screen, account, form=None, *args, **keywords):
        super().__init__(screen, form, *args, **keywords)
        self.account = account

    def _pre_edit(self):
        super()._pre_edit()
        self.parent.set_avatar(self.account)

    def _post_edit(self):
        super()._post_edit()
        self.parent.set_avatar(None)

    def whenPressed(self):
        if VK.login_by_token(self.account):
            super().whenPressed()


class MainForm(nps.ActionFormMinimal):
    OK_BUTTON_TEXT = l10n.translate("button.exit.title")
    FIX_MINIMUM_SIZE_WHEN_CREATED = False

    def create(self):
        self.login = self.add(FormButton, form="LOGIN", name=l10n.translate("button.form.MAIN.login.title"))
        self.settings = self.add(FormButton, form="SETTINGS", name=l10n.translate("button.form.MAIN.settings.title"))

    def login_click(self):
        self.parentApp.setNextForm(None)

    def on_ok(self):
        self.parentApp.setNextForm(None)


class LoginForm(nps.ActionFormMinimal):
    OK_BUTTON_TEXT = l10n.translate("button.back.title")
    FIX_MINIMUM_SIZE_WHEN_CREATED = False

    def create(self):
        self.add(FormButton, form="LOGIN_NEW", name=l10n.translate("button.from.LOGIN.login_new.title"))
        i = 0
        for account in SETTINGS.get_accounts():
            self.add(AccountButton, account=account, rely=4 + i, form=None, name=account["name"])
            i += 1
        self.avatar = self.add(ImageWidget, rely=1, relx=-21, editable=False, width=20, height=10)

    def on_ok(self):
        self.parentApp.switchFormPrevious()

    def set_avatar(self, account):
        if account:
            avatar = VK.get_avatar(account["id"], size="large")
            self.avatar.set_img(avatar)
        else:
            self.avatar.set_img(None)
        self.avatar.display()


class LoginNewForm(nps.ActionForm):
    OK_BUTTON_TEXT = l10n.translate("button.ok.title")
    CANCEL_BUTTON_TEXT = l10n.translate("button.cancel.title")
    CANCEL_BUTTON_BR_OFFSET = (2, 15)
    FIX_MINIMUM_SIZE_WHEN_CREATED = False

    def create(self):
        self.login = self.add(nps.TitleText, name=l10n.translate("titletext.form.LOGIN_NEW.login.title"))
        self.password = self.add(nps.TitlePassword, name=l10n.translate("titlepassword.form.LOGIN_NEW.password.title"))
        self.remember = self.add(nps.Checkbox, name=l10n.translate("checkbox.form.LOGIN_NEW.remember.title"))

    def on_ok(self):
        result = VK.login_by_pass(self.login.value, self.password.value, notify_auth_handler, self.remember.value)
        if result:
            self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()


class VkProfileForm(nps.ActionForm):
    def create(self):
        pass

    def display(self, clear=True):
        super().display(clear)

    def on_ok(self):
        self.parentApp.setNextForm(None)

    def on_cancel(self):
        self.parentApp.switchForm("MAIN")
