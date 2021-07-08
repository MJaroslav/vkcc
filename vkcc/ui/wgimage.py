import npyscreen as nps
from vkcc.ext.imagedisplaymethod import get_render_method as renderer, DrawException
import os
import vkcc.config.localization as l10n


class Image(nps.MultiLine):
    _contained_widgets = nps.DummyWidget

    def __init__(self, screen, image=None, hide_if_none=False, *args, **keywords):
        super().__init__(screen, *args, **keywords)
        self._image_ = image
        self.hide_if_none = hide_if_none
        self.editable = False
        self.__draw_error_callback__ = keywords["draw_error_callback"] if "draw_error_callback" in keywords else None
        self.__image_changed_callback__ = keywords["image_changed_callback"] if "image_changed_callback" in keywords \
            else self.image_changed

    def destroy(self):
        self.clear()
        if self.__draw_error_callback__:
            self.__draw_error_callback__ = None
            del self.__draw_error_callback__
        self.__image_changed_callback__ = None
        del self.__image_changed_callback__

    def set_image(self, image):
        old = self._image_
        self._image_ = image
        if self.hide_if_none:
            self.hidden = not self._image_
        if old != self._image_:
            self.__image_changed_callback__()

    def image_changed(self):
        self.display()

    def display(self):
        try:
            if self.hidden or not self._image_:
                self.clear()
                self.parent.refresh()
            else:
                self.update()
                self.parent.refresh()
        except DrawException as e:
            if self.__draw_error_callback__ is not None:
                self.__draw_error_callback__(e)

    def update(self, clear=False):
        x = self.relx
        y = self.rely
        w = self.width
        h = self.height
        if x < 0 or y < 0:
            ww, wh = os.get_terminal_size()
            if x < 0:
                x = ww - w + x + 1
            if y < 0:
                y = wh - h + y + 1
        renderer().draw(self._image_, x, y, w, h)

    def clear(self, usechar=' '):
        x = self.relx
        y = self.rely
        w = self.width
        h = self.height
        if x < 0 or y < 0:
            ww, wh = os.get_terminal_size()
            if x < 0:
                x = ww - w + x + 1
            if y < 0:
                y = wh - h + y + 1
        renderer().clear(x, y, w, h)

    def resize(self):
        # super().resize()
        self.clear()


class ImageBoxed(nps.BoxTitle):
    _contained_widget = Image

    def __init__(self, screen, image=None, *args, **keywords):
        super().__init__(screen,
                         contained_widget_arguments={"image": image, "draw_error_callback": self.draw_error_callback,
                                                     "image_changed_callback": self.image_changed_callback},
                         *args, **keywords)
        self.editable = False

    def image_changed_callback(self):
        self.update()

    def draw_error_callback(self, error):
        # self.footer = l10n.translate("text.error.title")
        pass  # TODO: Make log warn

    # def update(self, clear=True):
    #     self.footer = None
    #     super().update(clear)

    def when_resized(self):
        self.entry_widget.height = self.height - 2
        self.entry_widget.width = self.width - 2
        self.entry_widget.relx = self.relx + 1
        self.entry_widget.rely = self.rely + 1
        self.entry_widget.set_size()

    # Proxy from Image
    def set_image(self, image):
        self.entry_widget.set_image(image)
