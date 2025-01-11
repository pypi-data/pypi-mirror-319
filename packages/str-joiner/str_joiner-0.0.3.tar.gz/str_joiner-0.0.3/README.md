# String joiner

Small tool to simplify string building.

## Description

Have you ever thought it would be nice to have `join` working as generator-function decorator? So you found one. Write 
your generator, put `StrJoiner` on top, simple as that.

## Example

```python
from str_joiner import StrJoiner

@StrJoiner()
def make_url(username, host, port = 443, path = None):
    yield 'https://'
    yield username
    yield '@'
    yield host
    yield ':'
    yield port  # str() will be used implicitly
    yield path  # will exclude if None

assert make_url('user', '127.0.0.1') == 'https://user@127.0.0.1:443'
```

## Install

```shell
pip install str_joiner
```

## Contributing

We'd love you to contribute! 👋
Checkout the [contributing guide](CONTRIBUTING.md) for help on how to help us out!
