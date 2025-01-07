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


R"""The `onepw` module for simple 1Password usage

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
version = "1.6"

# On a Mac, the 1Password `op` tool is installed in "/usr/local/bin/"
# or "/opt/homebrew/bin/" (with HomeBrew)
op_path = ""	# We guess full path not necessary (test: `shutil.which()`)
op_cmd = op_path + "op"


class OnePWError(Exception):
    """Any error in the 1Password session"""
    def __init__(self, errmsg: str):
        self.errmsg = errmsg


class OnePW:
    """A Python class for a 1Password session

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

    """


    def __init__(self, account: str | None = None, op_pw: str | None = None):
        """Instantiate a 1Password session

        Create a 1Password session to be ready to `get` fields from
        1Password entries or to `add` entries to 1Password.

        `account` -- (default `None`)

        `op_pw` -- (default `None`)

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
        if op_pw:
            res = subprocess.run(
                cmd, input=op_pw, text=True, capture_output=True)
        else:
            res = subprocess.run(
                cmd, text=True, capture_output=True)
        if res.returncode == 145:
            errmsg = "1Password authentication failed"
            raise OnePWError(errmsg)
        elif res.returncode == 1:
            errmsg = "\nDo a first sign in with command line 'op':\n" + \
                "  op signin <signinaddress> <emailaddress> <secretkey>" + \
                "\nSee 1Password Preferences -> Accounts for the arguments\n"
            raise OnePWError(errmsg)
        elif res.returncode != 0:
            errmsg = f"1Password signin failed (error-code: {res.returncode})"
            raise OnePWError(errmsg)

        # Save session token (empty if 1Password 8 CLI integration enabled)
        self.session_token = res.stdout.rstrip()


    def get(self, title: str, field: str = "password") -> str:
        """Get a field from a 1Password entry

        Get a field from the 1Password entry `title`.

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
        value = res.stdout.rstrip()	# = json.loads(res.stdout.rstrip())["fields"]
        if not value:
            errmsg = f"No '{field}' in 1Password for '{title}'"
            raise OnePWError(errmsg)

        # Return the value
        return value


    def add(
            self, title: str, username: str, password: str,
            email: str | None = None, url: str | None = None):
        """Add a new entry to 1Password

        Add a new entry to 1Password with the provided values.

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


def _print_sig(cmd: str):
    from inspect import signature
    method = getattr(OnePW, cmd)
    print(f"{method.__name__}{str(signature(method))}")


def _print_doc(cmd: str | list | None = None, prog: str = "onepw"):
    if type(cmd) is str:
        method = getattr(OnePW, cmd)
        print(f"\n\033[1mMethod '{cmd}'\033[0m:\n")
        _print_sig(cmd)
        print("\n" + method.__doc__.strip() + "\n")
    else:
        print(f"\n\033[1mModule 'onepw'\033[0m:\n")
        print(__doc__.strip() + "\n")
        print(f"\033[1mClass 'OnePW'\033[0m:\n")
        print(OnePW.__doc__.strip() + "\n")
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
        "-L", nargs='?', const=True, choices=cmds, default=argparse.SUPPRESS,
        help=argparse.SUPPRESS)
    parser.add_argument(
        "--op-pw", metavar="PASSWORD", default=None,
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
        else:
            _print_sig(args.L)
        return

    # If we have a password without a value in arguments, we ask for it
    if "password" in args:
        if not args.password:
            from getpass import getpass
            args.password = getpass()

    # Starte the 1Password session and bind methods to the commands
    kw = vars(args)
    op_pw = kw.pop("op_pw")
    op = OnePW(op_pw = op_pw)
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
