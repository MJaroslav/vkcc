import npyscreen as nps
from vkcc.config import translate, configuration
import vkcc.core
from vkcc.ui.wgformswitchbutton import FormSwitchButton
from vkcc.ui.utilNotifyExtended import notify_yes_no_translated
from vkcc.ui.wgimage import ImageBoxed
from vkcc.ext import VK


class LoginForm(nps.ActionFormMinimal):
    class LoginButton(FormSwitchButton):
        def __init__(self, screen, form=None, is_delete=False, when_pressed_function=None, *args, **keywords):
            self.__is_delete__ = is_delete
            name = translate("button.form.LOGIN.delete.title") if is_delete else \
                translate("button.form.LOGIN.login.title")
            super().__init__(screen, form, when_pressed_function, name=name, *args, **keywords)

        def whenPressed(self):
            if self.__is_delete__:
                if notify_yes_no_translated(translate("text.sure.title") + "?", editw=1):
                    configuration.remove_account(self.parent.get_account())
                    self.parent.__accounts__.value = None
                    self.parent.__accounts__.update()
                    self.parent.set_account(None)
            else:
                if VK.login_by_token(self.parent.get_account()):
                    super().whenPressed()

    class AccountsBox(nps.BoxTitle):
        class AccountSelect(nps.SelectOne):
            def update(self, clear=True):
                super().update(clear)
                self.update_account()

            def find_selected(self):
                return self.value[0] if self.value else -1

            # def _post_edit(self):
            #     self.update_account()

            def update_account(self):
                selected = self.find_selected()
                if selected > -1:
                    self.parent.set_account(configuration.get_accounts()[selected])
                else:
                    self.parent.set_account(None)

        _contained_widget = AccountSelect

        def update(self, clear=True):
            self.entry_widget.values = list(map(lambda account: account["name"], configuration.get_accounts()))
            super().update(clear)

        def value_changed_callback(self, widget):
            self.parent.account = configuration.get_accounts()[widget.value[0]]

        def reset(self):
            self.entry_widget.value = None

    OK_BUTTON_TEXT = translate("button.back.title")
    FIX_MINIMUM_SIZE_WHEN_CREATED = False

    def __init__(self, *args, **keywords):
        self.__avatar__ = None
        self.__account__ = None
        self.__accounts__ = None
        self.__login_as__ = None
        self.__login__ = None
        self.__delete_account__ = None
        super().__init__(name=translate("form.LOGIN.title"), *args, **keywords)

    def beforeEditing(self):
        self.set_account(None)
        self.__accounts__.reset()

    def afterEditing(self):
        self.set_account(None)

    def create(self):
        self.add(FormSwitchButton, form=vkcc.core.FORM_LOGIN_NEW,
                 name=translate("button.form.LOGIN.login_new.title"))
        self.__accounts__ = self.add(self.AccountsBox, contained_widget_arguments={"slow_scroll": True}, rely=4,
                                     scroll_exit=True, width=-23, max_width=-18,
                                     name=translate("box.form.LOGIN.accounts.title"))
        self.__avatar__ = self.add(ImageBoxed, rely=1, relx=-21, name=translate("img.form.LOGIN.avatar.title"),
                                   width=20, height=10)
        self.__login_as__ = self.add(nps.FixedText, rely=11, relx=-20, editable=False)
        self.__login__ = self.add(self.LoginButton, rely=13, relx=-20, hidden=True)
        self.__delete_account__ = self.add(self.LoginButton, is_delete=True, rely=14, relx=-20, hidden=True)

    def on_ok(self):
        self.parentApp.switchFormPrevious()

    def get_account(self):
        return self.__account__

    def set_account(self, account):
        if account:
            self.__account__ = account
            avatar = VK.get_avatar(account["id"], size="large")
            self.__avatar__.set_image(avatar)
        else:
            self.__avatar__.set_image(None)
        # TODO: Try to fix resizing crash, caused by any update()
        self.__login_as__.value = account["name"] if account is not None else None
        self.__login__.hidden = account is None
        self.__delete_account__.hidden = account is None
        self.__login_as__.update()
        self.__login__.update()
        self.__delete_account__.update()
