# kpfpwd

CLI tool to fetch passwords from KeePass databases. It is an 
alternative to `pass` utility, but with KeePass database backend 
instead of GPG encrypted files.

There are two implementations: Perl and Python. Python is the default 
implementation.

# Installation

## Binary

Check out the [git repository](https://gitlab.com/aelmahmoudy/kpfpwd).

## From PyPI (for Python implementation)

```shell
# Recommended
pipx install kpfpwd

# alternative
pip3 install --user kpfpwd
```

# Quickstart

Fetching GitHub account info, which is stored in an entry titled `github`

```shell
# Get password:
$ kpfpwd --dbfile ~/passwords.kdbx github

# Get username:
$ kpfpwd --dbfile ~/passwords.kdbx --tag username github

# Generate OTP:
$ kpfpwd --dbfile ~/passwords.kdbx --otp github
```

# Usage

Just run `kpfpwd --help`. You'll get it:

<!-- KPFPWD_HELP -->
```
usage: kpfpwd [-h] [-V] [-c CONFFILE] [-f DBFILE] [-p PWDEVAL] [-F KEYFILE]
              [-e ESCAPE] [-t TAG] [-o] [-C] [-d]
              query

positional arguments:
  query                 Entry to be queried

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  -c CONFFILE, --conffile CONFFILE
                        Configuration file
  -f DBFILE, --dbfile DBFILE
                        KeePass DB file
  -p PWDEVAL, --pwdeval PWDEVAL
                        KeePass DB password evaluation
  -F KEYFILE, --keyfile KEYFILE
                        KeePass DB key file
  -t TAG, --tag TAG     Tag name
  -o, --otp             Generate OTP
  -C, --copy            Copy to clipboard/paste buffer
  -d, --debug           Debug
```
<!-- PKP_HELP_END -->

# Configuration

Default configuration file is `$XDG_CONFIG_DIR/kpfpwd/config`, it 
supports the configuration of the following keys: `dbfile` `pwdeval` 
`keyfile`. An example configuration file:

```conf
[DEFAULT]
dbfile = ~/passwords.kdbx
pwdeval=gpg --no-tty -q -d ~/passwords-kdbx.gpg
```

