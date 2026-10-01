# aws-browser
Open the aws console in a browser, using CLI credentials

## Installation
This package is available on PyPI. Using [uv](https://docs.astral.sh/uv/) is recommended, but pipx and pip
work as well.

Run it directly without installing (uv downloads and caches it for you):
```shell
uvx aws-browser
```

Install it as a persistent tool:
```shell
uv tool install aws-browser
pipx install aws-browser
pip install aws-browser
```

Or to install from source:

```shell
uv tool install git+https://github.com/WeAreCloudar/aws-browser.git
pipx install git+https://github.com/WeAreCloudar/aws-browser.git
```

## Usage
Run `aws-browser` with your AWS CLI credentials available (through your environment, a profile, or a
tool like `aws-vault`). Without any options it opens the AWS console in your default browser.

```shell
aws-browser [options]
```

To see all options run `aws-browser --help`.

### Selecting a browser
Open the console in the default browser:
```shell
aws-browser
```

Open the console in a specific browser:
```shell
aws-browser --browser firefox
```

Print the sign-in link instead of opening a browser:
```shell
aws-browser --stdout
```

### Using Firefox container tabs
This tool pairs very well with Firefox multi-account containers. To use that:

1. Install the [Firefox Multi-Account Containers](https://addons.mozilla.org/en-US/firefox/addon/multi-account-containers/) and [Open external links in a container]https://addons.mozilla.org/en-US/firefox/addon/open-url-in-container/ extensions.
2. Run one of the following commands.

```shell
# Use the account/role as the container name
aws-browser --browser firefox --container
# Pick the container yourself
aws-browser --browser firefox --container --container-name myProfileName
# get the container name from the  AWS_VAULT environment variable
aws-browser --browser firefox --container --container-name-from-vault
```


## Development
We use [uv](https://docs.astral.sh/uv/) to manage this project.

1. Clone this repository
2. Run `uv sync` to create the virtual environment and install all dependencies (including dev tools)
3. Run commands inside the environment with `uv run`, e.g. `uv run aws-browser --help`

uv automatically creates the virtual environment in the `.venv` folder inside the project. To use it in your
editor (for example the "Python: Select interpreter" command in Visual Studio Code), point to `.venv`.

### Linting and formatting
We use [Ruff](https://docs.astral.sh/ruff/) via pre-commit. Run all checks with:
```shell
uvx pre-commit run --all-files
```

### Releasing a new version to PyPI
Releases are automated with [release-please](https://github.com/googleapis/release-please).
Commits on `main` must follow the [Conventional Commits](https://www.conventionalcommits.org/) spec
(e.g. `feat:`, `fix:`, `chore:`), since release-please uses them to determine the next version and to
build the changelog.

release-please opens (and keeps updating) a release pull request that bumps the version in
`pyproject.toml` and updates the changelog. Merging that pull request tags the commit, creates the
GitHub release, and publishes the new version to PyPI automatically.

Publishing to PyPI uses [trusted publishing](https://docs.pypi.org/trusted-publishers/) (OIDC), so
no API token is stored in the repository. This requires a one-time setup on PyPI: add a trusted
publisher for the project pointing at this repository with workflow `release-please.yaml`.
