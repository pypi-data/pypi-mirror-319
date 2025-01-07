# django-filer-optimizer [![PyPi license](https://img.shields.io/pypi/l/django-filer-optimizer.svg)](https://pypi.python.org/pypi/django-filer-optimizer)

[![PyPi status](https://img.shields.io/pypi/status/django-filer-optimizer.svg)](https://pypi.python.org/pypi/django-filer-optimizer)
[![PyPi version](https://img.shields.io/pypi/v/django-filer-optimizer.svg)](https://pypi.python.org/pypi/django-filer-optimizer)
[![PyPi python version](https://img.shields.io/pypi/pyversions/django-filer-optimizer.svg)](https://pypi.python.org/pypi/django-filer-optimizer)
[![PyPi downloads](https://img.shields.io/pypi/dm/django-filer-optimizer.svg)](https://pypi.python.org/pypi/django-filer-optimizer)
[![PyPi downloads](https://img.shields.io/pypi/dw/django-filer-optimizer.svg)](https://pypi.python.org/pypi/django-filer-optimizer)
[![PyPi downloads](https://img.shields.io/pypi/dd/django-filer-optimizer.svg)](https://pypi.python.org/pypi/django-filer-optimizer)

## GitHub ![GitHub release](https://img.shields.io/github/tag/DLRSP/django-filer-optimizer.svg) ![GitHub release](https://img.shields.io/github/release/DLRSP/django-filer-optimizer.svg)

## Test [![codecov.io](https://codecov.io/github/DLRSP/django-filer-optimizer/coverage.svg?branch=main)](https://codecov.io/github/DLRSP/django-filer-optimizer?branch=main) [![pre-commit.ci status](https://results.pre-commit.ci/badge/github/DLRSP/django-filer-optimizer/main.svg)](https://results.pre-commit.ci/latest/github/DLRSP/django-filer-optimizer/main) [![gitthub.com](https://github.com/DLRSP/django-filer-optimizer/actions/workflows/ci.yaml/badge.svg)](https://github.com/DLRSP/django-filer-optimizer/actions/workflows/ci.yaml)

## Check Demo Project
* Check the demo repo on [GitHub](https://github.com/DLRSP/example/tree/django-filer-optimizer)

## Requirements
-   Python 3.8+ supported.
-   Django 3.2+ supported.

## Setup
1. Install from **pip**:
    ```shell
    pip install django-filer-optimizer
    ```
2. Modify `settings.py` by adding the app to `INSTALLED_APPS`:
    ```python
    INSTALLED_APPS = [
        # ...
        "filer_optimizer",
        # ...
    ]
    ```
3. Modify `settings.py` by adding the config `THUMBNAIL_DEFAULT_STORAGE`:
    ```python
    # See: https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-STORAGES
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
    }
    THUMBNAIL_DEFAULT_STORAGE = STORAGES["default"]["BACKEND"]
    ```

## Run Example Project

```shell
git clone --depth=50 --branch=django-filer-optimizer https://github.com/DLRSP/example.git DLRSP/example
cd DLRSP/example
python manage.py runserver
```

Now browser the app @ http://127.0.0.1:8000
