# aws-browser
Open the aws console in a browser, using CLI credentials

## Installation
This package is available on pypi, you can use on of these commands to install (pipx is recommended)
```shell
pipx install aws-browser
pip install aws-browser
```

Or to install from source, you can use one of these commands:

```shell
pipx install git+https://github.com/WeAreCloudar/aws-browser.git
pipx install git+ssh://git@github.com:WeAreCloudar/aws-browser.git
```

## Development
We use poetry to manage this project

1. Clone this repository
2. Run `poetry install`
3. Activate the virtualenvironment with `poetry shell` (you can also use `poetry run $command`)

### Releasing a new version to pypi
1. Edit pyproject.toml to update the version number
3. Commit the version number bump
5. Tag the commit with the version number `git tag x.y.z`
6. Push to GitHub with `git push --tags`, this will create a new release in pypi and GitHub


### Using poetry in Visual Studio Code
If you want to use poetry in Visual Studio Code, it works best if the virtual environment is created
inside the project folder. Once the virtual environment is created, you can run the "Python: Select
interpreter" command in Visual Studio Code, and point to the `.venv` folder.

```shell
poetry config virtualenvs.in-project true
```
If you already created the virtual environment, you have to recreate it
```shell
# from within the project folder
poetry env remove $(poetry env list)
poetry install
```
