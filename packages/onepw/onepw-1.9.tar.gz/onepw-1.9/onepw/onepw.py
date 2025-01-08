#!/usr/bin/env python3

###############################################################################
#
# Copyright (c) 2022-2025, Anders Andersen, UiT The Arctic University
# of Norway. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# - Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
# - Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the
#   distribution.
#
# - Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived
#   from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
###############################################################################


R"""The `onepw` Python module for 1Password integration

The `onepw` Python module implements a limited *1Password* integration
using *1Password CLI*:

 - https://developer.1password.com/docs/cli

To use the module, install the *1Password CLI* tool `op`:

 - https://1password.com/downloads/command-line/

(or install it with a package tool, e.g., *HomeBrew* on a Mac).

The `onepw` module is available from my software repository and from
PyPi:

 - https://www.pg12.org/software

 - https://pypi.org/project/onepw/

It is best to install the module and the companion console script
`onepw` with `pip`:

```bash
pip install onepw
```

It is recommended to integrated the *1Password CLI* tool with the
*1Password* desktop app (to use the desktop app to sign in to
*1Password*).  See Step 2 here for details:

 - https://developer.1password.com/docs/cli/get-started/

Other similar Python modules, with more or different functionality,
are available. The obvious first choice is the SDKs from *1Password*:

 - https://developer.1password.com/docs/sdks/

Their Python SDK is in active development and should be considered
when integratiing *1Password* with Python:

 - https://github.com/1Password/onepassword-sdk-python

Another option is to use the `keyring` module with the third-party
backend *OnePassword Keyring*:

 - https://pypi.org/project/keyring/

 - https://pypi.org/project/onepassword-keyring/

One downside of this approach is that when *OnePassword Keyring* is
installed, it replaces the default backend of the `keyring` module.  I
prefer that the default behavior of `keyring` is unchanged (using the
system keychain/keyring) and use a specific module (like `onepw`) for
*1Password* integration in Python.

"""


# Use subprocess to perform the command line operations
import subprocess


# The 1Password command line program `op` uses JSON
import json


# Use `shutil.which()` to verify that the 1Password CLI is installed
import shutil


# When adding entries to 1Password, store it in a temporary file first
import tempfile


# Current version of module
version = "1.9"


# On a Mac, the 1Password `op` tool is installed in "/usr/local/bin/"
# or "/opt/homebrew/bin/" (with HomeBrew)
op_path = ""	# We guess full path is not necessary (test: `shutil.which()`)
op_cmd = op_path + "op"


class OnePWError(Exception):
    """Any error in the 1Password session"""
    def __init__(self, errmsg: str):
        self.errmsg = errmsg


class OnePW:
    """A Python class for 1Password sessions

    When an instance of this class is created, a *1Password* session
    is started.  With this session you can perform *1Password CLI*
    commands. The following methods for such commands are available:

     - `get`: get a field from a 1Password entry

     - `add`: add an entry to 1Password
    
    In the following example, a *1Password* session is created and the
    password from the `"Google"` entry in 1Password is fetched:

    ```python
    op = OnePW()
    pw = op.get("Google", field="password")
    ```

    """


    def __init__(self, account: str | None = None, pw: str | None = None):
        """Instantiate a 1Password session

        When a *1Password* session is instantiated you are signed in
        to *1Password*. If the *1Password CLI* tool is integrated with
        the *1Password* desktop app, the desktop app is used to sign
        in to *1Password*. Otherwise, the password has to be provided,
        either as the argument `pw` (usually not recommended) or
        prompted for.

        `account` -- The account to sign in to (usually, not needed;
        default `None`)

        `pw` -- (usually, not needed; default `None`)

        """

        # Save for error messages
        self._last = "__init__"

        # Verify that the 1Password command `op` is installed
        if not shutil.which(op_cmd):
            errmsg = "\nInstall (and initialize) the 'op' command from " + \
                "1Password:\n" + \
                "  https://1password.com/downloads/command-line\n"
            raise OnePWError(errmsg)
        
        # Login (new session)
        if account:
            cmd =  [op_cmd, "signin", "--account", account, "--raw"]
        else:
            cmd =  [op_cmd, "signin", "--raw"]
        if pw:
            res = subprocess.run(
                cmd, input=pw, text=True, capture_output=True)
        else:
            res = subprocess.run(
                cmd, text=True, capture_output=True)
        if res.returncode != 0:
            errmsg = "1Password signin failed (error-code: " + \
                f"{res.returncode})\n  {res.stderr.strip()}"
            raise OnePWError(errmsg)

        # Save session token (empty if 1Password 8 CLI integration enabled)
        self.session_token = res.stdout.rstrip()


    def get(self, title: str, field: str = "password") -> str:
        """Get a field from a 1Password entry

        Get a field from the 1Password entry with the title
        `title`. The default field is `"password"`, but any other
        fields like `"username"`, `"email"` or `"url"` are possible.
        The method raises a `OnePWError` exception if an entry with
        the given title and/or field is not found.

        `title` -- The title of the entry

        `field` -- The field to get from the entry (default `"password"`)

        `return` -- The value of the field in the entry

        """

        # Save for error messages
        self._last = "get"
        
        # Get entry for item from 1Password
        res = subprocess.run(
            [op_cmd, "--session", self.session_token,
             "item", "get", title, "--reveal", "--fields", field],
            text=True, capture_output=True)
        if res.returncode != 0:
            errmsg = f"Fetching {field} for '{title}' from 1Password failed"
            raise OnePWError(errmsg)

        # Decode the entry
        value = res.stdout.rstrip()
        if not value:
            errmsg = f"No '{field}' in 1Password for '{title}'"
            raise OnePWError(errmsg)

        # Return the value
        return value


    def add(
            self, title: str, username: str, password: str,
            email: str | None = None, url: str | None = None):
        """Add a new entry to 1Password

        Add a new entry to 1Password with the provided values. A
        title, username and password are required. The method raises a
        `OnePWError` exception if adding the entry fails.

        `title` -- The title of the entry

        `username` -- The username added to the entry

        `password` -- The password added to the entry

        `email` -- The email address added to the entry (default `None`)
        
        `url` -- The URL added to the entry (default `None`)

        """

        # Save for error messages
        self._last = "add"
        
        # Get template for new entry
        res = subprocess.run(
            [op_cmd, "--session", self.session_token,
             "item", "template", "get", "Login"],
            text=True, capture_output=True)
        if res.returncode != 0:
            errmsg = "Fetching template for 'Login' from 1Password failed"
            raise OnePWError(errmsg)

        # Fill in the form with username and password
        try:
            template = json.loads(res.stdout.rstrip())
            for field in template["fields"]:
                if field["id"] == "username":
                    field["value"] = username
                elif field["id"] == "password":
                    field["value"] = password
        except KeyError:
            errmsg = "Error in 1Password template?"
            raise OnePWError(errmsg)
        except:
            errmsg = "Unable to parse template output from 1Password"
            raise OnePWError(errmsg)

        # Add email if provided
        if email:
            template["fields"].append(
                {"id": "email", "label": "email", "purpose": "EMAIL",
                 "value": email, "type": "STRING"})

        # Add entry to 1Password via a temp json file
        with tempfile.NamedTemporaryFile(mode="w") as tmp:

            # Dump the json to a temp file
            json.dump(template, tmp)
            tmp.seek(0) # Go back to beginning of file

            # Create the `op` command
            cmd = [op_cmd, "--session", self.session_token,
                   "item", "create", "--template", tmp.name,
                   "--title", f"{title}"]
            if url:
                cmd.append("--url")        
                cmd.append(f"{url}")        

            # Actually add entry to 1Password
            res = subprocess.run(cmd, text=True, capture_output=True)

        # Did it go OK?
        if res.returncode != 0:
            errmsg = f"Adding entry in 1Password for '{title}' failed"
            raise OnePWError(errmsg)


def d2na(kw: dict, sep: str = " ", pre: str = "--", asg: str = " ") -> str:
    """Convert dictionary to string representation of named arguments

    A simple help function converting a dictionary to a string
    representation of arguments.  It is possible to modify the
    separator `sep`, the pre-string before the name `pre`, and the
    asignment string `asg`.  The default values are matching command
    line arguments.

    `sep` -- Separator between each name/value pair (`sep`, default
    " ", but ", " is an alternative for named arguments to Python
    functions)

    `pre` -- A string added before the name of each argument (default
    "--", but '"' is an alternative for named arguments to Python
    functions)

    `asg` -- The string for assignment of the value to the named
    argument (default " ", but "=" is an alternative for named
    arguments to Python functions)

    """
    na_str_list = []
    for k in kw:
        na_str_list.append(f"{pre}{k}{asg}{repr(kw[k])}")
    return sep.join(na_str_list)


def _print_sig(cmd: str, name: str | None = None):
    """Print the method signature

    Print the method signature of the method named `cmd` in the
    `OnePW` class.

    `cmd` -- Name of the method to print the signature of

    """
    from inspect import signature
    method = getattr(OnePW, cmd)
    if not name: name = method.__name__
    print(f"{name}{str(signature(method))}")


def _print_doc(cmd: str | list | None = None, prog: str = "onepw"):
    """Print the documentation of a single method or a list of methods

    Print the method documentation of the method named `cmd` in the
    `OnePW` class. If `cmd` is a list of method names, print the
    documention of the module, the `OnePW` class, and all the
    methods. If `cmd` is `None`, only print the documention of the
    module and the `OnePW` class.

    `cmd` -- Name of a method, a list of method names, or `None` for
    no specific method

    """

    # Print documention for a single method
    if type(cmd) is str:
        method = getattr(OnePW, cmd)
        print(f"\n\033[1mMethod '{cmd}'\033[0m:\n")
        _print_sig(cmd)
        print("\n" + method.__doc__.strip() + "\n")

    # Print documention for the module
    else:

        # Print the module documention
        print(f"\n\033[1mModule 'onepw'\033[0m:\n")
        print(__doc__.strip() + "\n")

        # Print the class `OnePW` documention
        print(f"\033[1mClass 'OnePW'\033[0m:\n")
        _print_sig("__init__", "OnePW")
        print("\n" + OnePW.__doc__.strip() + "\n")
        init_doc_lines = OnePW.__init__.__doc__.strip().splitlines()[2:]
        print("\n".join(init_doc_lines) + "\n")

        # Print information about the list of methods
        if type(cmd) is list:
            print(f"\033[1mClass 'OnePW' methods\033[0m:\n")
            for c in cmd:
                print(f"\033[1m{c}\033[0m: {prog} --doc {c}\n")

    
def main():
    """Run module as a program

    Run the module as a program with these possible commands:

    - `get`: get the value of a field in an entry in 1Password (default
      field is password)

    - `add`: add an entry in 1Password

    """

    # Need `argv`, `stderr` and `exit`
    import sys

    # The commands implemented
    cmds = ["get", "add"]
    cmdchoices = "{" + ",".join(cmds) + "}"
    
    # A trick for a late binding of args.func (after the creation of
    # the 1Password session)
    method_dict = {}  # Will be populated with a method for each command
    get_func = lambda **kw: method_dict["get"](**kw)
    add_func = lambda **kw: method_dict["add"](**kw)
    
    # Create overall argument parser
    import argparse
    parser = argparse.ArgumentParser(
        description="perform 1Password CLI commands",
        epilog=f"use '%(prog)s {cmdchoices} -h' " + \
          "to show help message for a specific command")
    parser.add_argument(
        "-V", "--version", action="version",
        version=f"%(prog)s " + version)
    parser.add_argument(
        "--doc", nargs='?', const=True, choices=cmds,
        default=argparse.SUPPRESS, 
        help="print documentation of module or specific command")
    parser.add_argument(
        "-D", action="store_true", default=argparse.SUPPRESS, 
        help=argparse.SUPPRESS)
    parser.add_argument(
        "-L", nargs='?', const=True, choices=cmds + ["OnePW"],
        default=argparse.SUPPRESS,
        help=argparse.SUPPRESS)
    parser.add_argument(
        "--account", default=None,
        help="the 1Password account (usually, not necessary)")
    parser.add_argument(
        "--pw", metavar="PASSWORD", default=None,
        help="the 1Password secret password (be careful using this)")
    subparsers = parser.add_subparsers(
        help="the command to perform")

    # Create argument parser for the `get` command
    parser_get = subparsers.add_parser(
        "get",
        help="get the value of a field from an entry in 1Password")
    parser_get.add_argument(
        "--title", required=True,
        help="the title of the entry to get the value from")
    parser_get.add_argument(
        "--field", default="password",
        help="the field of the entry to get the value from " + \
          "(default 'password'")
    parser_get.set_defaults(func=get_func)

    # Create argument parser for the `add` command
    parser_add = subparsers.add_parser(
        "add", help='add an entry to 1Password')
    parser_add.add_argument(
        "--title", required=True,
        help="the title of the new entry")
    parser_add.add_argument(
        "--username", required=True,
        help="the user name in the new entry")
    parser_add.add_argument(
        "--password",
        help="the password in the new entry " + \
          "('%(prog)s' will ask for the password if it is not provided)")
    parser_add.add_argument(
        "--email", default=None,
        help="the email address in the new entry (default None)")
    parser_add.add_argument(
        "--url", default=None,
        help="the URL in the new entry (default None)")
    parser_add.set_defaults(func=add_func)

    # Parse arguments
    args = parser.parse_args()

    # Print documentation?
    if "doc" in args:
        if args.doc == True:
            _print_doc(cmds, sys.argv[0])
        else:
            _print_doc(args.doc)
        return

    # Print alternative (non-documented) documentation?
    if "D" in args:
        _print_doc()
        return

    # Print list of commands (non-documented)?
    if "L" in args:
        if args.L == True:
            print("\n".join(cmds))
        elif args.L == "OnePW":
            _print_sig("__init__", args.L)
        else:
            _print_sig(args.L)
        return

    # If we have a password without a value in arguments, we ask for it
    if "password" in args:
        if not args.password:
            from getpass import getpass
            args.password = getpass()

    # Starte the 1Password session
    kw = vars(args)
    account = kw.pop("account")
    pw = kw.pop("pw")
    try:
        op = OnePW(account = account, pw = pw)
    except OnePWError as e:
        print(
            f">>> {sys.argv[0]}: Unable to sign in to 1Password:\n" + \
            f"--> {e.errmsg}", file = sys.stderr)
        sys.exit(1)

    # Bind methods to the commands
    for m in cmds:
        method_dict[m] = getattr(op, m)

    # Perform command
    func = kw.pop("func")
    try:
        res = func(**kw)
    except OnePWError as e:
        print(
            f">>> {sys.argv[0]}: Unable to do '{op._last}' command:\n" + \
            f"  {op._last} {d2na(kw)}\n" + \
            f"--> {e.errmsg}", file = sys.stderr)
        sys.exit(1)

    # Print result, if any
    if res: print(res)


# Execute this module as a program
if __name__ == '__main__':
    main()
