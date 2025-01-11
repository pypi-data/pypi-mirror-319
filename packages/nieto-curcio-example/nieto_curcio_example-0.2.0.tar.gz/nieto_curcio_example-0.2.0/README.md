uv run -- python -m src.nieto_curcio_example.main

uv run -- python -m nieto_curcio_example.main

uv run nieto_curcio_example

source .venv/bin/activate
python -m nieto_curcio_example.main

## Building

uv build

This command creates the `dist/` folder:
```sh
dist
├── nieto_curcio_example-0.1.0-py3-none-any.whl
└── nieto_curcio_example-0.1.0.tar.gz
```

## Publishing

uv publish

https://docs.astral.sh/uv/guides/publish/#preparing-your-project-for-packaging:

"""
If you have internal packages that you do not want to be published, you can mark them as private:


```toml
[project]
classifiers = ["Private :: Do Not Upload"]
This setting makes PyPI reject your uploaded package from publishing. It does not affect security or privacy settings on alternative registries.
```

We also recommend only generating per-project tokens: Without a PyPI token matching the project, it can't be accidentally published.
"""


Set a PyPI token with --token or UV_PUBLISH_TOKEN, or set a username with --username or UV_PUBLISH_USERNAME and password with --password or UV_PUBLISH_PASSWORD.

export $(cat .env | xargs)
echo $UV_PUBLISH_PASSWORD