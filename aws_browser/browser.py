import urllib.parse
import webbrowser

from .constants import CONTAINER_SUFFIX


def open_in_browser(url: str, browser=None) -> None:
    browser = webbrowser.get(browser)
    browser.open_new_tab(url)


def container_url(url: str, container_name: str) -> str:
    return f"ext+container:name={container_name}&url={urllib.parse.quote(url)}"


def list_supported_browsers():
    return {"firefox", f"firefox{CONTAINER_SUFFIX}", "google-chrome", "safari"}
