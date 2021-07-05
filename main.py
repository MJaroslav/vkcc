from vkcc.vkcc import App
import sys
from vkcc.vk import VK


def main():
    if "--clear-cache" in sys.argv:
        VK.clear_cache()
    app = App()
    app.run()


if __name__ == "__main__":
    main()
