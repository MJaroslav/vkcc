from vkcc.core.vkccapp import VKCCApp
from vkcc.ext import VK
import sys


def main():
    if "--clear-cache" in sys.argv:
        VK.clear_cache()
    app = VKCCApp()
    app.run()
