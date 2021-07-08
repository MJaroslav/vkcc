import npyscreen as nps
from vkcc.core import FORM_SETTINGS
from vkcc.ext import update_render_method
from vkcc.config import translate, configuration
from vkcc.config.locales import LOCALES
from vkcc.ui.utilNotifyExtended import notify_confirm_translated


# TODO: Try to refactor
class SettingsForm(nps.ActionFormMinimal):
    OK_BUTTON_TEXT = translate("button.back.title")

    def __init__(self, *args, **keywords):
        self.__language__ = None
        self.__profile__ = None
        self.__render__ = None
        super().__init__(name=translate("form.SETTINGS.title"), *args, **keywords)

    def create(self):
        self.__profile__ = self.add(nps.TitleCombo, name=translate("combo.form.SETTINGS.profile.title"),
                                    value_changed_callback=self.__on_profile_changed__)
        self.__language__ = self.add(nps.TitleCombo, name="Language", rely=4,
                                     value_changed_callback=self.__on_language_changed__)
        self.__render__ = self.add(nps.TitleCombo, name=translate("combo.form.SETTINGS.render.title"),
                                   value_changed_callback=self.__on_render_changed__)

    def __on_language_changed__(self, widget):
        languages = configuration.allowed_languages()
        current = languages[self.__language__.value]
        configuration.set_language(current)

    def __on_profile_changed__(self, widget):
        profiles = configuration.allowed_profiles()
        current = profiles[self.__profile__.value]
        configuration.set_profile(current)
        self.parentApp.switchForm(FORM_SETTINGS)  # Ha-ha is not display/update call

    def __on_render_changed__(self, widget):
        renders = configuration.allowed_render_methods()
        current = renders[self.__render__.value]
        configuration.set_render_method(current)
        update_render_method()

    def beforeEditing(self):
        profiles = configuration.allowed_profiles()
        current = profiles.index(configuration.get_profile())
        self.__profile__.set_values(profiles)
        self.__profile__.value = current
        languages = configuration.allowed_languages()
        current = languages.index(configuration.get_language())
        self.__language__.set_values(list(map(lambda language: LOCALES[language]["name"],
                                              configuration.allowed_languages())))
        self.__language__.value = current
        renders = configuration.allowed_render_methods()
        current = renders.index(configuration.get_render_method())
        self.__render__.set_values(renders)
        self.__render__.value = current

    def on_ok(self):
        notify_confirm_translated("text.restart.title")
        # TODO: Make markers for not restartable options
        self.parentApp.switchFormPrevious()


