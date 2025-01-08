# cabina

[![Codecov](https://img.shields.io/codecov/c/github/tsv1/cabina/main.svg?style=flat-square)](https://codecov.io/gh/tsv1/cabina)
[![PyPI](https://img.shields.io/pypi/v/cabina.svg?style=flat-square)](https://pypi.python.org/pypi/cabina/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/cabina?style=flat-square)](https://pypi.python.org/pypi/cabina/)
[![Python Version](https://img.shields.io/pypi/pyversions/cabina.svg?style=flat-square)](https://pypi.python.org/pypi/cabina/)

**cabina** is a Python library that simplifies building hierarchical, environment-driven configurations. It provides:

- **Simple class-based configurations**  
- **Automatic environment variable parsing**  
- **Type-safe defaults**  
- **Computed values**  
- **Flexible customization**  

## Installation

```sh
pip3 install cabina
```

## Quick Start

Here’s a minimal example showing how cabina handles environment variables, defaults, and computed properties:

```python
import cabina
from cabina import computed, env

class Config(cabina.Config):
    class Main(cabina.Section):
        API_HOST: str = env.str("API_HOST", default="localhost")
        API_PORT: int = env.int("API_PORT", default=8080)

        @computed
        def API_URL(cls) -> str:
            return f"http://{cls.API_HOST}:{cls.API_PORT}"

# Usage
assert Config.Main.API_URL == "http://localhost:8080"
assert Config["Main"]["API_URL"] == "http://localhost:8080"

# Print
print(Config)
# class <Config>:
#     class <Main>:
#         API_HOST = 'localhost'
#         API_PORT = 8080
#         API_URL = 'http://localhost:8080'
```

## Recipes

Below are some common patterns and features you can use with **cabina**:

- [Root Section](#root-section)  
- [Computed Values](#computed-values)  
- [Default Values](#default-values)  
- [Raw Values](#raw-values)  
- [Custom Parsers](#custom-parsers)  
- [JSON Parser](#json-parser)  
- [Lazy Env](#lazy-env)  
- [Env Vars Prefix](#env-vars-prefix)  
- [Inheritance](#inheritance)

### Root Section

You can use **cabina** for simple, flat configurations by inheriting `cabina.Section` in your main config:

```sh
export API_HOST=localhost
export API_PORT=8080
```

```python
import cabina
from cabina import env

class Config(cabina.Config, cabina.Section):  # Note the inheritance
    API_HOST = env.str("API_HOST")
    API_PORT = env.int("API_PORT")

assert Config.API_HOST == "localhost"
assert Config.API_PORT == 8080
```

### Computed Values

You can define dynamic or derived config values via the `@computed` decorator:

```sh
export API_HOST=localhost
export API_PORT=8080
```

```python
import cabina
from cabina import computed, env

class Config(cabina.Config, cabina.Section):
    API_HOST: str = env.str("API_HOST")
    API_PORT: int = env.int("API_PORT")

    @computed
    def API_URL(cls) -> str:
        return f"http://{cls.API_HOST}:{cls.API_PORT}"

assert Config.API_URL == "http://localhost:8080"
```

### Default Values

Provide a default if an environment variable isn’t set:

```sh
export API_HOST=127.0.0.1
```

```python
import cabina
from cabina import env

class Config(cabina.Config, cabina.Section):
    API_HOST = env.str("API_HOST", default="localhost")
    API_PORT = env.int("API_PORT", default=8080)

assert Config.API_HOST == "127.0.0.1"
assert Config.API_PORT == 8080
```

### Raw Values

Get the raw, unprocessed string from an environment variable — even if it includes leading/trailing spaces:

```sh
export DEBUG=" yes"
```

```python
import cabina
from cabina import env

class Config(cabina.Config, cabina.Section):
    DEBUG_RAW = env.raw("DEBUG")  # Same as env("DEBUG") without processing
    DEBUG_STR = env.str("DEBUG")  # Strips whitespace

assert Config.DEBUG_RAW == " yes"   # The raw value includes whitespace
assert Config.DEBUG_STR == "yes"    # Whitespace is stripped
```

### Custom Parsers

Use custom parsing functions to handle special formats. For instance, parse a duration string with `pytimeparse`:

```sh
export HTTP_TIMEOUT=10s
```

```python
import cabina
from cabina import env
from pytimeparse import parse as parse_duration

class Config(cabina.Config, cabina.Section):
    HTTP_TIMEOUT: int = env("HTTP_TIMEOUT", parser=parse_duration)

assert Config.HTTP_TIMEOUT == 10
```

### JSON Parser

Easily load JSON data from an environment variable:

```sh
export IMAGE_SETTINGS='{"AllowedContentTypes": ["image/png", "image/jpeg"]}'
```

```python
import json
import cabina
from cabina import env

class Config(cabina.Config, cabina.Section):
    IMAGE_SETTINGS = env("IMAGE_SETTINGS", parser=json.loads)

assert Config.IMAGE_SETTINGS == {
    "AllowedContentTypes": ["image/png", "image/jpeg"]
}
```

### Lazy Env

Defer parsing environment variables until their first access. This can be useful if some variables may not exist at import time:

```sh
export DEBUG=yes
export API_PORT=80a  # Contains an invalid int "80a"
```

```python
import cabina
from cabina import lazy_env

class Config(cabina.Config, cabina.Section):
    DEBUG = lazy_env.bool("DEBUG")
    API_HOST = lazy_env.str("API_HOST")  # Only fetched upon attribute access
    API_PORT = lazy_env.int("API_PORT")

# Attempt to fetch all at once
Config.prefetch()
# Raises ConfigEnvError with:
# - Config.API_HOST: 'API_HOST' does not exist
# - Config.API_PORT: Failed to parse '80a' as int
```

### Env Vars Prefix

Use a prefix for all your environment variables to avoid collisions:

```sh
export APP_HOST=localhost
export APP_PORT=8080
```

```python
import cabina

env = cabina.Environment(prefix="APP_")

class Config(cabina.Config, cabina.Section):
    API_HOST = env.str("HOST")  # 'APP_HOST' will be used
    API_PORT = env.int("PORT")  # 'APP_PORT' will be used

assert Config.API_HOST == "localhost"
assert Config.API_PORT == 8080
```

### Inheritance

Create a base configuration and extend it for local or specialized use cases:

```python
import cabina

class Config(cabina.Config, cabina.Section):
    DEBUG = False

    class Api(cabina.Section):
        API_HOST = "app.dev"
        API_PORT = 5000

class ConfigLocal(Config):
    DEBUG = True

    class Api(Config.Api):
        API_HOST = "localhost"

assert ConfigLocal.DEBUG is True
assert ConfigLocal.Api.API_HOST == "localhost"
assert ConfigLocal.Api.API_PORT == 5000
```

## Contributing

Contributions, bug reports, and feature requests are welcome! Feel free to open an [issue](https://github.com/tsv1/cabina/issues) or submit a pull request.
