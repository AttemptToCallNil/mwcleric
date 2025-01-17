from os import path, getenv

from .errors import InvalidUserFile


class AuthCredentials(object):
    username = None
    password = None
    
    def __init__(self, username=None, password=None, user_file=None):
        """
        Stores username and password for future use with a WikiClient.
        Specify either user_file or both username and password.
        
        If using a file, files can be either located in the same directory as the code,
        or in the config directory of the user. If files in both locations exist,
        files in the former location will trump those in the latter.

        :param username: Username, this must include an @ if using a bot password
        :param password: Password, this is the actual value of the password, not the "name" of a "bot password"
        :param user_file: Either a file or a system variable as a nicknamed account to look for
        """
        if username and password:
            self.username = username
            self.password = password
        elif user_file:
            pwd_file = 'password_{}.txt'.format(user_file.lower())
            usr_file = 'username_{}.txt'.format(user_file.lower())
            if path.exists(pwd_file) and path.exists(usr_file):
                self.password = open(pwd_file).read().strip()
                self.username = open(usr_file).read().strip()
                return
            pwd_path = path.join(path.expanduser('~'), '.config', 'mwcleric', pwd_file)
            usr_path = path.join(path.expanduser('~'), '.config', 'mwcleric', usr_file)
            if path.exists(pwd_path) and path.exists(usr_path):
                self.password = open(pwd_path).read().strip()
                self.username = open(usr_path).read().strip()
                return
            pwd_key = 'WIKI_PASSWORD_{}'.format(user_file.upper())
            usr_key = 'WIKI_USERNAME_{}'.format(user_file.upper())
            pwd = getenv(pwd_key, None)
            usr = getenv(usr_key, None)
            if not pwd or not usr:
                raise InvalidUserFile
            self.password = pwd
            self.username = usr
