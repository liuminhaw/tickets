# -*- coding: UTF-8 -*-

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
        self.VISION_CRED = 'vision-cred'

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

    def vision_cred(self):
        """
        Return config vision api credential setting in GENERAL section
        """
        return self._read_value(self.GENERAL, self.VISION_CRED)

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
        _date = self._read_value(section_name, self.DATE)
        self._validate('\d{4}/\d{2}/\d{2}', self.DATE, _date)

        return _date

    def section(self, section_name):
        """
        Return config SECTION option in section_name section
        """
        _section = self._read_value(section_name, self.SECTION) 
        self._validate('morning|evening|night', self.SECTION, _section)

        return _section

    def time(self, section_name):
        """
        Return config TIME option in section_name section
        """
        _time = self._read_value(section_name, self.TIME)
        self._validate('[0-2]\d:00~[0-2]\d:00', self.TIME, _time)

        return _time

    def court(self, section_name):
        """
        Return config COURT option in section_name section
        """
        _court = self._read_value(section_name, self.COURT)
        self._validate('羽[0-9]|羽10', self.COURT, _court)

        return _court


    def _validate(self, pattern, key, value):
        """
        Test to make sure there is value for all options
        Input:
            pattern: regular expression object
            key: string - config option key
            value: string - config option value
        """
        _re_pattern = re.compile(r'{}'.format(pattern))

        if _re_pattern.fullmatch(value) == None:
            raise OptionFormatError(key, value)

    
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