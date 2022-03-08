import subprocess
import sys
import urllib.parse
import webbrowser

from .constants import CONTAINER_SUFFIX

_BROWSERS_NO_CONTAINERS = {"google-chrome", "safari", "msedge"}
_BROWSERS_WITH_CONTAINERS = {"firefox"}
_ALL_BROWSERS = _BROWSERS_NO_CONTAINERS.union(_BROWSERS_WITH_CONTAINERS)


def open_in_browser(url: str, browser=None) -> None:
    browser = webbrowser.get(browser)
    browser.open_new_tab(url)


def container_url(url: str, container_name: str) -> str:
    return f"ext+container:name={container_name}&url={urllib.parse.quote(url)}"


def list_supported_browsers():
    return _ALL_BROWSERS.union((f"{x}{CONTAINER_SUFFIX}" for x in _BROWSERS_WITH_CONTAINERS))


def add_browsers_from_registry():
    if sys.platform[:3] != "win":
        return

    # not available on mac/linux
    import winreg

    # these should all come after the default browser list
    for name in _ALL_BROWSERS:
        try:
            webbrowser.get(name)
            # already registered by default discovery
            continue
        except webbrowser.Error:
            # not found
            pass

        try:
            key_name = rf"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\{name}.exe"
            with winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE, key_name) as key:
                exe = winreg.QueryValueEx(key, "")[0]
            webbrowser.register(name, None, webbrowser.BackgroundBrowser(exe))
        except OSError:
            # does not exist
            continue


add_browsers_from_registry()
