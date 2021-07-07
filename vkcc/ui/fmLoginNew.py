import npyscreen as nps
from vkcc.ui.utilNotifyExtended import YesNoPopupTranslated
from vkcc.config import translate
from vkcc.ext import VK


class LoginNewForm(nps.ActionForm):
    OK_BUTTON_TEXT = translate("button.ok.title")
    CANCEL_BUTTON_TEXT = translate("button.cancel.title")
    CANCEL_BUTTON_BR_OFFSET = (2, 15)
    FIX_MINIMUM_SIZE_WHEN_CREATED = False

    def __init__(self, parentApp=None, framed=None, help=None, color='FORMDEFAULT', widget_list=None,
                 cycle_widgets=False, *args, **keywords):
        self.__login__ = None
        self.__password__ = None
        self.__remember__ = None
        super().__init__(translate("form.LOGIN_NEW.title"), parentApp, framed, help, color, widget_list, cycle_widgets,
                         *args, **keywords)

    def afterEditing(self):
        self.__login__.value = None
        self.__password__.value = None
        self.__remember__.value = False

    def create(self):
        self.__login__ = self.add(nps.TitleText, name=translate("titletext.form.LOGIN_NEW.login.title"))
        self.__password__ = self.add(nps.TitlePassword, name=translate("titlepassword.form.LOGIN_NEW.password.title"))
        self.__remember__ = self.add(nps.Checkbox, name=translate("checkbox.form.LOGIN_NEW.remember.title"))

    @staticmethod
    def notify_auth_handler():
        f = YesNoPopupTranslated(name=translate("popup.TWO_AUTH.title"), color='STANDOUT')
        f.preserve_selected_widget = True

        code = f.add(nps.TitleText, name=translate("titletext.popup.TWO_AUTH.code.title"))
        remember = f.add(nps.Checkbox, name=translate("checkbox.popup.TWO_AUTH.remember.title"))

        f.editw = 0
        f.edit()

        return code.value, remember.value

    def on_ok(self):
        result = VK.login_by_pass(self.__login__.value, self.__password__.value, self.notify_auth_handler,
                                  self.__remember__.value)
        if result:
            self.parentApp.switchFormPrevious()
            # self.parentApp.getForm("LOGIN").reload_accounts()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()
