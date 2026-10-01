from argparse import ArgumentParser
from importlib.metadata import version
from os import environ

from .aws import _get_session, get_console_url, get_normalized_caller_identifier
from .browser import container_url, list_supported_browsers, open_in_browser
from .constants import CONTAINER_SUFFIX


def run():
    parser = ArgumentParser()
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {version('aws-browser')}",
        help="show the program version and exit",
    )
    parser.add_argument("--browser", help="browser to open", choices=list_supported_browsers())
    parser.add_argument("--stdout", help="print link to stdout", action="store_true")
    parser.add_argument("--container", help="Force the use of a container", action="store_true")
    parser.add_argument(
        "--container-name-from-vault",
        help="Use the AWS_VAULT environment variable as the container name",
        action="store_true",
    )
    parser.add_argument("--container-name", help="container name to use")

    args = parser.parse_args()

    browser: str | None = args.browser
    container: bool | None = args.container
    container_name: str | None = args.container_name
    container_name_from_vault: bool | None = args.container_name_from_vault
    stdout: bool | None = args.stdout

    # we can continue, in every case, except when _name and _from_vault are both set
    # this translates to a NAND (see the truth table below)
    #  N | V | continue
    # ---|---|---
    #  0 | 0 | 1
    #  0 | 1 | 1
    #  1 | 0 | 1
    #  1 | 1 | 0
    assert not (container_name and container_name_from_vault), "You can only specify one --container-name option"

    if browser and browser.endswith(CONTAINER_SUFFIX):
        container = True
        browser = browser[: -len(CONTAINER_SUFFIX)]

    session = _get_session()
    url = get_console_url(session=session)

    if container:
        if container_name_from_vault:
            container_name = environ["AWS_VAULT"]
        if not container_name:
            container_name = get_normalized_caller_identifier(session=session)
        url = container_url(url, container_name)
    if stdout:
        print(url)
    else:
        open_in_browser(url, browser)


if __name__ == "__main__":
    run()
