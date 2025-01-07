### The `onepw` module for simple 1Password usage

See [PyPi](https://pypi.org/project/onepw/) for documentation
generated from the source code of the module.

### To install and use the module

This module implements a very limited 1Password integration for Python
using 1Password CLI:

 - https://developer.1password.com/docs/cli/get-started/

To use the module, install the 1Password CLI tool `op` version 2:

 - https://1password.com/downloads/command-line/

(or install it with a package tool, e.g., HomeBrew on a Mac.)

#### Class OnePW

Use class to create a 1Password session

Example where a 1Password session is created and a password is fetched:

```python
op = OnePW()
pw = op.get("Google", field="password")
```

#### Method <a id="get"></a>`get`

*Get a field from a 1Password entry*

The signature of `get`:

```python
get(self, title: str, field: str = 'password') -> str
```

Get a field from the 1Password entry `title`.

 - `title`: The title of the entry

 - `field`: The field to get from the entry (default `"password"`)

 - `return`: The value of the field in the entry

#### Method <a id="add"></a>`add`

*Add a new entry to 1Password*

The signature of `add`:

```python
add(self, title: str, username: str, password: str, email: str | None = None, url: str | None = None)
```

Add a new entry to 1Password with the provided values.

 - `title`: The title of the entry

 - `username`: The username added to the entry

 - `password`: The password added to the entry

 - `email`: The email address added to the entry (default `None`)

 - `url`: The URL added to the entry (default `None`)

