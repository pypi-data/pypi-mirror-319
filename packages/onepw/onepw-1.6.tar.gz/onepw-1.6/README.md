### The `onepw` module for simple 1Password usage

See [PyPi](https://pypi.org/project/onepw/) for documentation
generated from the source code of the module.

### To install and use the module

This module implements a very limited 1Password integration for Python
using 1Password CLI:

 - https://developer.1password.com/docs/cli/get-started/

To use the module, install the 1Password CLI tool `op` version 2:

 - https://1password.com/downloads/command-line/

(or install it with a package tool, e.g., HomeBrew on a Mac).

Install the module and the console script `onepw` with `pip`:

```bash
pip install onepw
```

#### Class OnePW

A Python class for a 1Password session

When an instance of this class is created, a 1Password session is
created.  With this session you can perform 1Password CLI
commands. The following methods for such commands are available

 - `get`: get a field from a 1Password entry

 - `add`: add an entry to 1Password

This is an example where a 1Password session is created and the
password from the `"Google"` entry in 1Password is fetched:

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

### To use the module as a console script

usage: onepw [-h] [-V] [--doc [{get,add}]] [--op-pw PASSWORD] {get,add} ...

perform 1Password CLI commands

##### positional arguments

Name | Description
---- | -----------
`{get,add}` | the command to perform
`get` | get the value of a field from an entry in 1Password
`add` | add an entry to 1Password

##### options

Name | Description
---- | -----------
`-h, --help` | show this help message and exit
`-V, --version` | show program's version number and exit
`--doc [{get,add}]` | print documentation of module or specific command
`--op-pw PASSWORD` | the 1Password secret password (be careful using this)

use 'onepw {get,add} -h' to show help message for a specific command

#### Command <a id="cli-get"></a>`get`

usage: onepw get [-h] --title TITLE [--field FIELD]

##### options

Name | Description
---- | -----------
`-h, --help` | show this help message and exit
`--title TITLE` | the title of the entry to get the value from
`--field FIELD` | the field of the entry to get the value from (default
`'password'

#### Command <a id="cli-add"></a>`add`

usage: onepw add [-h] --title TITLE --username USERNAME [--password PASSWORD]
`[--email EMAIL] [--url URL]

##### options

Name | Description
---- | -----------
`-h, --help` | show this help message and exit
`--title TITLE` | the title of the new entry
`--username USERNAME` | the user name in the new entry
`--password PASSWORD` | the password in the new entry ('onepw add' will ask for
`the password if it is not provided)
`--email EMAIL` | the email address in the new entry (default None)
`--url URL` | the URL in the new entry (default None)

