# -*- conding: UTF-8 -*-

# Standard library imports
import configparser
import os
import re

class Config():

    def __init__(self, candidates):
        """
        Input:
            candidates - ini config files list
        """
        # self.HOME = str(pathlib.Path.home())

        # Sections 
        self.GENERAL= 'GENERAL'
        self.ACCOUNT = 'ACCOUNT'

        # Keys
        self.LOGIN_LINK = 'login-link'
        self.BOOKING_LINK = 'booking-link'

        self.USER = 'user'
        self.PASSWORD = 'password'

        self.DATE = 'date'
        self.SECTION = 'section'
        self.TIME = 'time'
        self.COURT = 'court'

        # Get config information
        self.candidates = candidates
        self._config = configparser.ConfigParser()
        self._config_found = self._config.read(self.candidates)

        # Make sure ini file exist
        if len(self._config_found) == 0:
            raise ConfigNotFoundError(configError)

    def login_link(self):
        """
        Return config login-link option in GENERAL section
        """
        return self._read_value(self.GENERAL, self.LOGIN_LINK)

    def booking_link(self):
        """
        Return config login-link option in GENERAL section
        """
        return self._read_value(self.GENERAL, self.BOOKING_LINK)

    def login_user(self):
        """
        Return config user option in ACCOUNT section
        """
        return self._read_value(self.ACCOUNT, self.USER)

    def login_password(self):
        """
        Return config password option in ACCOUNT section
        """
        return self._read_value(self.ACCOUNT, self.PASSWORD)

    def date(self, section_name):
        """
        Return config DATE option in section_name section
        """
        return self._read_value(section_name, self.DATE)

    def section(self, section_name):
        """
        Return config SECTION option in section_name section
        """
        return self._read_value(section_name, self.SECTION)

    def time(self, section_name):
        """
        Return config TIME option in section_name section
        """
        return self._read_value(section_name, self.TIME)

    def court(self, section_name):
        """
        Return config COURT option in section_name section
        """
        return self._read_value(section_name, self.COURT)


    def validate(self):
        """
        Test to make sure there is value for all options
        """
        _re_pattern = re.compile(r'REGEX-PATTERN')

        self._regex_test(_re_pattern, value, NAMED_KEY)

    
    def _read_value(self, section, key):
        """
        Get the value of key inside section
        Input:
            section - config file section
            key - config file option
        Return:
            key value
        Error:
            NoSectionError - Section not found
            NoOptionError - Option not found
        """
        try:
            _config_value = self._config.get(section, key)
        except configparser.NoSectionError:
            raise NoSectionError(section)
        except configparser.NoOptionError:
            raise NoOptionError(key)
        else:
            return _config_value


    def _regex_test(self, pattern , value, key):
        """
        Test regex matching
        Input:
            pattern: regular expression object
            value: string - config option value
            key: string - config option key
        """
        if pattern.fullmatch(value) == None:
            raise OptionFormatError(key, value)



# Exceptions
class configError(Exception):
    """
    Base class of config exception
    """
    pass

class ConfigNotFoundError(configError):
    """
    Raised if not finding ini file
    """
    pass

class NoSectionError(configError):
    """
    Raised by configparser.NoSectionError
    """
    def __init__(self, section):
        self.message = '{} section not found'.format(section)

class NoOptionError(configError):
    """
    Raised by configparser.NoOptionError
    """
    def __init__(self, option):
        self.message = '{} option not found'.format(option)

class OptionFormatError(configError):
    """
    Raised if option is in wrong format
    """
    def __init__(self, option, value):
        self.message = '{} wrong format: {}'.format(option, value)