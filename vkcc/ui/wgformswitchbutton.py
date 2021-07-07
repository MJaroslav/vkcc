import npyscreen as nps


class FormSwitchButton(nps.ButtonPress):
    def __init__(self, screen, form=None, when_pressed_function=None, *args, **keywords):
        super().__init__(screen, when_pressed_function, *args, **keywords)
        self.form = form
        if "name" in keywords:
            self.name = self.safe_string(keywords["name"] + "..")

    def whenPressed(self):
        app = self.find_parent_app()
        if app.has_form(self.form):
            app.switchForm(self.form)
