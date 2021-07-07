import npyscreen as nps
from vkcc.config import translate, configuration
import vkcc.core
import vkcc.ui.wgformswitchbutton
import vkcc.ui.wgimage
from vkcc.ext import VK


class LoginForm(nps.ActionFormMinimal):
    class LoginButton(vkcc.ui.wgformswitchbutton.FormSwitchButton):
        def __init__(self, screen, form=None, is_delete=False, when_pressed_function=None, *args, **keywords):
            self.__is_delete__ = is_delete
            name = translate("button.form.LOGIN.delete.title") if is_delete else \
                translate("button.form.LOGIN.login.title")
            super().__init__(screen, form, when_pressed_function, name=name, *args, **keywords)

        def _pre_edit(self):
            super()._pre_edit()
            self.parent.set_account(self.parent.get_account())

        def _post_edit(self):
            super()._post_edit()
            self.parent.set_account(None)

        def whenPressed(self):
            if self.__is_delete__:
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
        self.__avatar__.set_image(None)
        self.__login_as__.value = None
        self.__accounts__.reset()

    def afterEditing(self):
        self.__avatar__.set_image(None)

    def create(self):
        self.add(vkcc.ui.wgformswitchbutton.FormSwitchButton, form=vkcc.core.FORM_LOGIN_NEW,
                 name=translate("button.form.LOGIN.login_new.title"))
        self.__accounts__ = self.add(self.AccountsBox, contained_widget_arguments={"slow_scroll": True}, rely=4,
                                     scroll_exit=True, width=-23, max_width=-18,
                                     name=translate("box.form.LOGIN.accounts.title"))
        self.__avatar__ = self.add(vkcc.ui.wgimage.ImageBoxed, rely=1, relx=-21,
                                   name=translate("img.form.LOGIN.avatar.title"), width=20, height=10)
        self.__login_as__ = self.add(nps.FixedText, rely=11, relx=-20, hidden=True, editable=False)
        self.__login__ = self.add(self.LoginButton, rely=13, relx=-20, hidden=True)
        self.__delete_account__ = self.add(self.LoginButton, is_delete=True, rely=14, relx=-20, hidden=True)
        self.__account__ = None

    def on_ok(self):
        self.parentApp.switchFormPrevious()

    def get_account(self):
        return self.__account__

    def set_account(self, account):
        old = self.__account__["id"] if self.__account__ else None
        if account:
            self.__account__ = account
            avatar = VK.get_avatar(account["id"], size="large")
            self.__avatar__.set_image(avatar)
        else:
            self.__avatar__.set_image(None)
        # TODO: Fix sync buttons
        # if old != (self.__account__["id"] if self.__account__ else None):
        self.__login_as__.value = account["name"] if account else None
        self.__login_as__.hidden = not self.__login_as__.value
        self.__login__.hidden = not self.__login_as__.value
        self.__delete_account__.hidden = not self.__login_as__.value
        self.__login_as__.update()
        self.__login__.update()
        self.__delete_account__.update()
