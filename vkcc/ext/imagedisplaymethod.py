import termios
import shlex
import subprocess
from builtins import Exception

from vkcc.config import configuration
import json
import os
import threading
import struct
import sys
import fcntl


class DrawException(BaseException):
    def __init__(self, cause_by: Exception):
        super().__init__(*cause_by.args)


class ImageDisplayMethod(object):
    def initialize(self):
        pass

    def draw(self, img, x, y, width, height):
        pass

    def clear(self, x, y, width, height):
        pass

    def dispose(self):
        pass

    def clear_all(self):
        pass


class UeberzugMethod(ImageDisplayMethod):
    def __init__(self):
        self.is_initialized = False
        self.process = None
        self.identifiers = []

    def initialize(self):
        try:
            if self.is_initialized and self.process.poll() is None and not self.process.stdin.closed:
                return
            self.process = subprocess.Popen(shlex.split("ueberzug layer --silent"),
                                            stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
            self.is_initialized = True
        except Exception as e:
            raise DrawException(e)

    def dispose(self):
        try:
            self.clear_all()
            if self.is_initialized and self.process.poll() is None:
                timer_killer = threading.Timer(1, self.process.kill, [])
                try:
                    self.process.terminate()
                    timer_killer.start()
                    self.process.communicate()
                finally:
                    timer_killer.cancel()
        except Exception as e:
            raise DrawException(e)

    def __run_command__(self, action, identifier, **kwargs):
        try:
            self.initialize()
            command = kwargs.copy()
            command.update({"action": action, "identifier": identifier})
            line = json.dumps(command) + "\n"
            self.process.stdin.write(line)
            self.process.stdin.flush()
            if action == "add":
                if identifier not in self.identifiers:
                    self.identifiers.append(identifier)
            elif action == "remove":
                if identifier in self.identifiers:
                    self.identifiers.remove(identifier)
        except Exception as e:
            raise DrawException(e)

    def draw(self, img, x, y, width, height):
        identifier = "{}:{}:{}:{}".format(x, y, width, height)
        self.__run_command__("add", identifier, x=x, y=y, width=width, height=height, path=img)

    def clear(self, x, y, width, height):
        identifier = "{}:{}:{}:{}".format(x, y, width, height)
        self.__run_command__("remove", identifier)

    def clear_all(self):
        for identifier in self.identifiers:
            self.__run_command__("remove", identifier)


class W3mimgdisplayMethod(ImageDisplayMethod):
    __W3MIMGDISPLAY_PATHS__ = [
        '/usr/lib/w3m/w3mimgdisplay',
        '/usr/libexec/w3m/w3mimgdisplay',
        '/usr/lib64/w3m/w3mimgdisplay',
        '/usr/libexec64/w3m/w3mimgdisplay',
        '/usr/local/libexec/w3m/w3mimgdisplay',
    ]

    def __find_w3mimgdisplay_executable__(self):
        path = configuration.get_w3mimgdisplay()
        if path:
            return path
        else:
            for path in self.__W3MIMGDISPLAY_PATHS__:
                if os.path.exists(path):
                    return path

    def __init__(self):
        self.is_initialized = False
        self.process = None
        self.binary_path = None

    def initialize(self):
        try:
            self.binary_path = None
            self.binary_path = self.__find_w3mimgdisplay_executable__()
            self.process = subprocess.Popen(shlex.split(self.binary_path),
                                            stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
            self.is_initialized = True
        except Exception as e:
            raise DrawException(e)

    def __get_font_size__(self):
        if self.binary_path is None:
            self.binary_path = self.__find_w3mimgdisplay_executable__()
        farg = struct.pack("HHHH", 0, 0, 0, 0)
        fd_stdout = sys.stdout.fileno()
        fretint = fcntl.ioctl(fd_stdout, termios.TIOCGWINSZ, farg)
        rows, cols, xpixels, ypixels = struct.unpack("HHHH", fretint)
        if xpixels == 0 and ypixels == 0:
            process = subprocess.Popen(shlex.split(self.binary_path + " -test"), stdout=subprocess.PIPE,
                                       universal_newlines=True)
            output, _ = process.communicate()
            output = output.split()
            xpixels, ypixels = int(output[0]), int(output[1])
            # Add offset
            xpixels += 2
            ypixels += 2
        return (xpixels // cols), (ypixels // rows)

    def __get_input__(self, img, x, y, max_width, max_height):
        fontw, fonth = self.__get_font_size__()
        max_width_pixels = max_width * fontw
        max_height_pixels = max_height * fonth
        cmd = "5;{}\n".format(img)
        # self.process.stdin.write(cmd)
        # self.process.stdin.flush()
        # output = self.process.stdout.readline().split()
        #
        # width = int(output[0])
        # height = int(output[1])
        #
        # if width > max_width_pixels:
        #     height = (height * max_width_pixels) // width
        #     width = max_width_pixels
        # if height > max_height_pixels:
        #     width = (width * max_height_pixels) // height
        #     height = max_height_pixels

        width = max_width_pixels
        height = max_height_pixels
        x = int((x - 0.2) * fontw)
        y = y * fonth

        return "0;1;{};{};{};{};;;;;{}\n4;\n4;\n".format(x, y, width, height, img)

    def dispose(self):
        try:
            if self.is_initialized and self.process and self.process.poll() is None:
                self.process.kill()
        except Exception as e:
            raise DrawException(e)

    def draw(self, img, x, y, width, height):
        try:
            if not self.is_initialized or self.process.poll() is not None:
                self.initialize()
            input_gen = self.__get_input__(img, x, y, width, height)

            from time import sleep
            sleep(2. / 1000)

            self.process.stdin.write(input_gen)
            self.process.stdin.flush()
        except Exception as e:
            raise DrawException(e)

    def clear(self, x, y, width, height):
        try:
            if not self.is_initialized or self.process.poll() is not None:
                self.initialize()

            fontw, fonth = self.__get_font_size__()

            x = int((x - 0.2) * fontw)
            y = y * fonth
            w = int((width + 0.4) * fontw)
            h = height * fonth + 1
            cmd = "6;{};{};{};{};\n4;\n3;\n".format(x, y, w, h)

            self.process.stdin.write(cmd)
            self.process.stdin.flush()
        except Exception as e:
            raise DrawException(e)

    def clear_all(self):
        w, h = os.get_terminal_size()
        self.clear(0, 0, w, h)


__CURRENT__ = None


__METHODS__ = {
    "w3mimgdisplay": W3mimgdisplayMethod,
    "ueberzug": UeberzugMethod
}


def __find_render_method__():
    method = configuration.get_render_method()
    if method in __METHODS__:
        return __METHODS__[method]
    else:
        return ImageDisplayMethod  # Dummy


def get_render_method():
    global __CURRENT__
    if __CURRENT__:
        return __CURRENT__
    method = __find_render_method__()
    __CURRENT__ = method()
    return __CURRENT__


def update_render_method():
    global __CURRENT__
    if __CURRENT__:
        __CURRENT__.dispose()
    __CURRENT__ = get_render_method()
    __CURRENT__.initialize()


update_render_method()
