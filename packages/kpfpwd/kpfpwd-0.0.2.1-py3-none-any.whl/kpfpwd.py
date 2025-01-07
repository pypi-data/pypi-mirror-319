#!/usr/bin/python3

__version__ = "0.0.2.1"

from pykeepass import PyKeePass
from argparse import ArgumentParser
import os
from appdirs import user_cache_dir, user_config_dir
from configparser import ConfigParser
import subprocess
import sys
from pathlib import Path
import re
import pyotp
import getpass

def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "-V", "--version", action="version", version=f"{__version__}"
    )
    parser.add_argument("-c", "--conffile",
        default=os.path.join(user_config_dir('kpfpwd'), 'config'),
        help="Configuration file")
    parser.add_argument("-f", "--dbfile", help="KeePass DB file")
    parser.add_argument("-p", "--pwdeval", help="KeePass DB password evaluation")
    parser.add_argument("-F", "--keyfile", help="KeePass DB key file")
    parser.add_argument("-t", "--tag",
        default='password',
        help="Tag name")
    parser.add_argument("-o", "--otp", action="store_true",
        default=False,
        help="Generate OTP")
    parser.add_argument("-C", "--copy",
        default=False,
        action="store_true",
        help="Copy to clipboard/paste buffer")
    parser.add_argument("-d", "--debug",
        default=False,
        action="store_true",
        help="Debug")
    parser.add_argument("query", help="Entry to be queried")
    return parser.parse_args()

def main():
    home = str(Path.home())
    args = parse_args()

    confparser = ConfigParser(allow_no_value=True)
    confparser.read(args.conffile)

    dbfile=args.dbfile
    if not dbfile:
        dbfile=confparser.get('DEFAULT', 'dbfile', fallback=None)
    # Replace ~ in path beginning with user home dir:
    dbfile = dbfile.replace('~', home)
    pwdeval=args.pwdeval
    if not pwdeval:
        pwdeval=confparser.get('DEFAULT', 'pwdeval', fallback=None)
    keyfile=args.keyfile
    if not keyfile:
        keyfile=confparser.get('DEFAULT', 'keyfile', fallback=None)
    if keyfile:
        # Replace ~ in path beginning with user home dir:
        keyfile = keyfile.replace('~', home)
    # Read master password from config file:
    master_pass=confparser.get('DEFAULT', 'master_pass', fallback=None)
    # .. or run pwdeval to get it:
    if not master_pass:
        if pwdeval:
            try:
                master_pass = subprocess.check_output(
                    pwdeval,
                    shell=True,
                    universal_newlines=True
                    )
            except subprocess.CalledProcessError as ex:
                print('Error evaluating command for password: %s' % ex)
                sys.exit(1)
    # .. or as final fallback, prompt user for it:
        else:
            master_pass = getpass.getpass('KeePass DB password: ')
    # remove trailing newline:
    master_pass = master_pass.rstrip('\n')
    
    kp = PyKeePass(
        filename=dbfile, password=master_pass, keyfile=keyfile
    )
    group = None
    pieces = args.query.split('/')
    entry_title = pieces[-1];
    # Find group that corresponds to query path:
    if len(pieces) > 1:
        group_titles = pieces[0:-1]
        if args.debug: print(f'{group_titles=}')
        for group_title in group_titles:
            if args.debug: print(f'{group_title=}')
            if group_title:
                group = kp.find_groups(name=group_title,
                    group = group,
                    first=True)
                if not group:
                    if args.debug: print('%s not found' % group_title)
                    sys.exit(1)
                if args.debug: print(f'{group=}')

    # Find entry:
    entry=kp.find_entries(title=entry_title, group=group, first=True)
    if not entry:
        print('%s not found' % entry_title)
        sys.exit(1)
    if args.debug: print(f'{entry=}');

    result=None
    # Set a sane default tag if not user specified:
    if args.otp:
        result=entry.otp;
        if re.match(r'^otpauth:', result):
            result = pyotp.parse_uri(result).now()
        else: # assume the field has TOTP secret
            result = pyotp.TOTP(result).now()
    else:
        '''
        match args.tag:
            case 'password':
                result = entry.password
            case 'username':
                result = entry.username
            case 'url'
                result = entry.url
            case 'notes'
                result = entry.notes
            case 'title'
                result = entry.title
        '''
        pattern = re.compile('^string[:/]')
        if args.tag == 'password':
            result = entry.password
        elif args.tag == 'username':
            result = entry.username
        elif args.tag == 'url':
            result = entry.url
        elif args.tag == 'notes':
            result = entry.notes
        elif args.tag == 'title':
            result = entry.title
        elif re.match(r'^string[:/]', args.tag):
            prop_string = re.findall('string[:/](.*)', args.tag)[0]
            result = entry.get_custom_property(prop_string)
    if args.copy:
        # Screen:
        # test sessions: screen -ls
        # copy contents to reg:
        # readreg [reg] [file]
        # Tmux:
        if not os.system('tmux has-session'):
          os.system(f'tmux set-buffer \'{result}\'');
    else: # print to stdout:
        print(result)

if __name__ == "__main__":
    main()
