# Publishing a package with Astral UV

Installing Astral UV:
```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Initialize a package:
```sh
uv init --package some-package
```

Folder structure:
```sh
some-package/
├── pyproject.toml
├── README.md
└── src
    └── some_package
        └── __init__.py
```

Then run `uv build`:
```sh
uv build

# Building source distribution...
# Building wheel from source distribution...
# Successfully built dist/some_package-0.1.0.tar.gz
# Successfully built dist/some_package-0.1.0-py3-none-any.whl
```

We can install from build in a python virtual env, then import it and call main function:
```sh
cd dist
python -m venv venv
source venv/bin/activate
pip install some_package-0.1.0-py3-none-any.whl
python -c "import some_package; some_package.main()"
# Hello from some-package!
```

The next step is publish. To publish we must create an account on `PyPI` and setup a API token, it may require the account to have 2FA as well to setup the API token. Also, notice the package name `some-package` for this example may already exists conflict and throw an error during publish, to workaround this we can create another name so in the output example below we published ``

The API token will be the value we'll provide as `password` in the command below, also notice we use `__token__` as username since we configured an API token:
```sh
uv publish some-random-250109-package

# warning: `uv publish` is experimental and may change without warning
# Enter username ('__token__' if using a token): __token__
# Enter password: 
# Publishing 2 files https://upload.pypi.org/legacy/
# Uploading some_random_250109_package-0.1.0-py3-none-any.whl (1.6KiB)
# Uploading some_random_250109_package-0.1.0.tar.gz (682.0B)
```

We successfully published a package
After that the package should be available in this link - `https://pypi.org/project/some_random_<DATE>_package/`


It is also possible to configure the username and password from the CLI or from environment variables:

- From CLI:
```sh
uv publish --username __token__ --password <PASSWORD>
```

- From environemnt variables:
```sh
export UV_PUBLISH_USERNAME="__token__"
export UV_PUBLISH_PASSWORD="<PASSWORD>"
uv publish
```

Please see publish relevant docs - https://docs.astral.sh/uv/guides/publish

## Building telliot-feeds and DVM with Astral UV

We can test how the build of telliot-feeds and DVM would work before publishing to PyPI:

1- Building telliot-feeds:

Clone telliot-feeds
```sh
mkdir telliot-feeds-with-uv
cd telliot-feeds-with-uv
git clone https://github.com/fetchoracle/telliot-feeds.git .
```
Build telliot-feeds:
```sh
uv build

# ...
# adding 'telliot_feeds/utils/source_utils.py'
# adding 'telliot_feeds/utils/stake_info.py'
# adding 'telliot_feeds/utils/stdev_calculator.py'
# adding 'telliot_feeds-0.2.1.dist-info/LICENSE'
# adding 'telliot_feeds-0.2.1.dist-info/METADATA'
# adding 'telliot_feeds-0.2.1.dist-info/WHEEL'
# adding 'telliot_feeds-0.2.1.dist-info/entry_points.txt'
# adding 'telliot_feeds-0.2.1.dist-info/top_level.txt'
# adding 'telliot_feeds-0.2.1.dist-info/RECORD'
# removing build/bdist.linux-x86_64/wheel
# Successfully built dist/telliot_feeds-0.2.1.tar.gz
# Successfully built dist/telliot_feeds-0.2.1-py3-none-any.whl
```

Installing telliot-feeds from build:
```sh
python -m venv venv
source venv/bin/activate
cp .env.example .env
pip install dist/telliot_feeds-0.2.1-py3-none-any.whl
telliot --help

# Usage: telliot [OPTIONS] COMMAND [ARGS]...

#   Telliot command line interface

# Options:
#   --test-config  Runs command with test configuration (developer use only)
#   --help         Show this message and exit.

# Commands:
#   account           Create, find, and manage accounts.
#   ampleforth        Report values to Tellor oracle if certain conditions...
#   catalog           Browse and search the query catalog.
#   conditional       Report values to Tellor oracle if certain conditions...
#   config            Manage Telliot configuration.
#   integrations      Commands for Tellor Protocol integrations.
#   liquity           Report values to Tellor oracle if certain conditions...
#   query             Decode query data, query responses, & build custom...
#   report            Report values to Tellor oracle
#   request-withdraw  Request withdraw of tokens from oracle
#   settle            Settle a derivative pool in DIVA Protocol.
#   stake             Deposit tokens to oracle
#   withdraw          Withdraw of tokens from oracle
```

2- Building DVM:

We can do the same with DVM, we'll be installing in the same `venv` created for `telliot-feeds-with-uv`:
```sh
mkdir DVM-with-uv
cd DVM-with-uv
git clone https://github.com/fetchoracle/https://github.com/fetchoracle/disputable-values-monitor.git .
uv build
pip install dist/disputable_values_monitor-2.0.4-py3-none-any.whl
cli --help

# Usage: cli [OPTIONS]

#   CLI dashboard to display recent values reported to Tellor oracles.

# Options:
#   -av, --all-values               if set, get alerts for all values
#   -a, --account-name TEXT         the name of a ChainedAccount to dispute with
#   -w, --wait INTEGER              how long to wait between checks
#   -d, --is-disputing              enable auto-disputing on chain
#   -c, --confidence-threshold FLOAT
#                                   set general confidence percentage threshold
#                                   for monitoring only
#   --initial_block_offset INTEGER  the number of blocks to look back when first
#                                   starting the DVM
#   --help                          Show this message and exit.
```

### Thoughts about Astral UV

Astral UV is a "new" tool compared to `poetry` for example since its release was on Feb 2024, but my initial experience with `uv` is really good since it is way more faster than other tools, simple to use and well compatible with python built-in structure in terms virtual environment management and `pyproject.toml` configuration, it makes things simple and faster. It also help us to publish packages to Python Package Index (PyPI). For example it has increased its popularity in terms of Github stars more than poetry is less than a year, please see link below, it is a tool that deserves attention:

https://star-history.com/#astral-sh/uv&python-poetry/poetry&Date
