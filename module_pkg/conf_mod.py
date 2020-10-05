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
        self.DRIVER = 'DRIVER'
        self.ACCOUNT = 'ACCOUNT'

        # Keys
        self.LOGIN_LINK = 'login-link'
        self.BOOKING_LINK = 'booking-link'
        self.VISION_CRED = 'vision-cred'

        self.DRIVER_COUNT = 'driver-count'
        self.HEADLESS = 'headless'
        self.EXECUTION_DELTA = 'execution-delta'
        self.SUBMIT_TIME_SLEEP = 'submit-time-sleep'
        self.SUBMIT_TIME_OFFSET = 'submit-time-offset'
        self.DRIVER_TIME_SLEEP = 'driver-time-sleep'

        self.USER = 'user'
        self.PASSWORD = 'password'

        self.SUBMIT_TIME = 'submit-time'
        self.DATE = 'date'
        self.SECTION = 'section'
        self.TIME = 'time'
        self.COURT = 'court'

        # Default value
        self.VISION_CRED_DFLT = 'credential.json'
        
        self.DRIVER_COUNT_DFLT = '1'
        self.HEADLESS_DFLT = 'False'
        self.EXECUTION_DELTA_DFLT = '3'
        self.SUBMIT_TIME_SLEEP_DFLT = '0.3'
        self.SUBMIT_TIME_OFFSET_DFLT = '0.2'
        self.DRIVER_TIME_SLEEP_DFLT = '0.2'

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
        Default setting: VISION_CRED_DFLT
        """
        cred = self._read_value(self.GENERAL, self.VISION_CRED, fallback_val=self.VISION_CRED_DFLT)
        if not os.path.isfile(cred):
            raise MissingFileError(cred)

        return cred 

    def driver_count(self):
        """
        Return config driver-count value in DRIVER section
        """
        _count = int(self._read_value(self.DRIVER, self.DRIVER_COUNT, 
            fallback_val=self.DRIVER_COUNT_DFLT))
        if _count < 1 or _count > 4:
            raise OptionFormatError(self.DRIVER, _count)

        return _count

    def execution_delta(self):
        """
        Return config execution-delta value in DRIVER section
        """
        _delta_time = int(self._read_value(self.DRIVER, self.EXECUTION_DELTA,
            fallback_val=self.EXECUTION_DELTA_DFLT))
        if _delta_time < 0:
            raise OptionFormatError(self.DRIVER, _delta_time)

        return _delta_time

    def submit_time_sleep(self):
        """
        Return config submit-time-sleep value in DRIVER section
        """
        _time_sleep = float(self._read_value(self.DRIVER, self.SUBMIT_TIME_SLEEP,
            fallback_val=self.SUBMIT_TIME_SLEEP_DFLT))
        if _time_sleep < 0:
            raise OptionFormatError(self.DRIVER, _time_sleep)

        return _time_sleep

    def submit_time_offset(self):
        """
        Return config submit-time-offset value in DRIVER section
        """
        _time_sleep = float(self._read_value(self.DRIVER, self.SUBMIT_TIME_OFFSET,
            fallback_val=self.SUBMIT_TIME_OFFSET_DFLT))
        if _time_sleep < 0:
            raise OptionFormatError(self.DRIVER, _time_sleep)

        return _time_sleep

    def driver_time_sleep(self):
        """
        Return config driver-time-sleep value in DRIVER section
        """
        _time_sleep = float(self._read_value(self.DRIVER, self.DRIVER_TIME_SLEEP,
            fallback_val=self.DRIVER_TIME_SLEEP_DFLT))
        if _time_sleep < 0:
            raise OptionFormatError(self.DRIVER, _time_sleep)

        return _time_sleep

    def headless(self):
        """
        Return config headless value in DRIVER section
        """
        _headless_mode = self._read_value(self.DRIVER, self.HEADLESS, fallback_val=self.HEADLESS_DFLT)
        self._validate('True|False', self.HEADLESS, _headless_mode)

        if _headless_mode == 'True':
            return True
        else:
            return False

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

    def submit_time(self, section_name):
        """
        Return config SUBMIT_TIME option in section_name section
        """
        _submit_time = self._read_value(section_name, self.SUBMIT_TIME)
        self._validate(r'\d{4}/\d{2}/\d{2}-\d{2}:\d{2}:\d{2}', self.SUBMIT_TIME, _submit_time)

        return _submit_time

    def date(self, section_name):
        """
        Return config DATE option in section_name section
        """
        _date = self._read_value(section_name, self.DATE)
        self._validate(r'\d{4}/\d{2}/\d{2}', self.DATE, _date)

        return _date

    def section(self, section_name):
        """
        Return config SECTION option in section_name section
        """
        _section = self._read_value(section_name, self.SECTION) 
        self._validate('morning|evening|night', self.SECTION, _section)

        if _section == 'morning':
            return '1'
        elif _section == 'evening':
            return '2'
        elif _section == 'night':
            return '3'
        else:
            raise OptionFormatError(self.SECTION, _section)

    def time(self, section_name):
        """
        Return config TIME option in section_name section
        """
        _time = self._read_value(section_name, self.TIME)
        self._validate(r'[0-2]\d:00~[0-2]\d:00', self.TIME, _time)

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

    
    def _read_value(self, section, key, fallback_val=None):
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
            if fallback_val is None:
                _config_value = self._config.get(section, key)
            else:
                _config_value = self._config.get(section, key, fallback=fallback_val)
        except configparser.NoSectionError as err:
            raise NoSectionError(section) from err
        except configparser.NoOptionError as err:
            raise NoOptionError(key) from err
        else:
            return _config_value


# Exceptions
class configError(Exception):
    """
    Base class of config exception
    """
    

class ConfigNotFoundError(configError):
    """
    Raised if not finding ini file
    """

class MissingFileError(configError):
    """
    Raised if file not find
    """
    def __init__(self, file):
        configError.__init__(self)
        self.message = 'File {} not found'.format(file)

class NoSectionError(configError):
    """
    Raised by configparser.NoSectionError
    """
    def __init__(self, section):
        configError.__init__(self)
        self.message = '{} section not found'.format(section)

class NoOptionError(configError):
    """
    Raised by configparser.NoOptionError
    """
    def __init__(self, option):
        configError.__init__(self)
        self.message = '{} option not found'.format(option)

class OptionFormatError(configError):
    """
    Raised if option is in wrong format
    """
    def __init__(self, option, value):
        configError.__init__(self)
        self.message = '{} wrong format: {}'.format(option, value)