from argparse import ArgumentParser
from os import environ
from typing import Optional

from .aws import get_normalized_caller_identifier, get_console_url, _get_session
from .browser import open_in_browser, list_supported_browsers, container_url
from .constants import CONTAINER_SUFFIX


def run():
    parser = ArgumentParser()
    parser.add_argument("--browser", help="browser to open", choices=list_supported_browsers())
    parser.add_argument("--stdout", help="print link to stdout", action="store_true")
    parser.add_argument("--container", help="Force the use of a container", action="store_true")
    parser.add_argument(
        "--container-name-from-vault",
        help="Use the AWS_VAULT environment variable as the container name",
        action="store_true",
    )
    parser.add_argument("--container-name", help=f"container name to use")

    args = parser.parse_args()

    browser: Optional[str] = args.browser
    container: Optional[bool] = args.container
    container_name: Optional[str] = args.container_name
    container_name_from_vault: Optional[bool] = args.container_name_from_vault
    stdout: Optional[bool] = args.stdout

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
