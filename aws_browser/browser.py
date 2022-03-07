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


class StartBackgroundBrowser(webbrowser.BackgroundBrowser):
    """
    The same as BackgroundBrowser, but we use "start {name} ..." instead of "{name} ..."
    """

    def open(self, url, new=0, autoraise=True):
        cmdline = ["start", self.name] + [arg.replace("%s", url) for arg in self.args]
        sys.audit("webbrowser.open", url)
        try:
            if sys.platform[:3] == "win":
                p = subprocess.Popen(cmdline)
            else:
                p = subprocess.Popen(cmdline, close_fds=True, start_new_session=True)
            return p.poll() is None
        except OSError:
            return False


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
            key = rf"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\{name}.exe"
            winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE, key)
        except OSError:
            # does not exist
            continue

        webbrowser.register(name, StartBackgroundBrowser)


add_browsers_from_registry()
