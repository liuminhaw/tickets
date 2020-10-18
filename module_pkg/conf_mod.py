# -*- coding: UTF-8 -*-

# Standard library imports
import configparser
import os
import re

class Config():
    """
    Class for configuration (ini file)
    """

    def __init__(self, candidates):
        """
        Input:
            candidates - ini config files list
        """
        # self.HOME = str(pathlib.Path.home())

        # Sections
        self._genaral= 'GENERAL'
        self._driver = 'DRIVER'
        self._account = 'ACCOUNT'

        # Keys
        self._login_link = 'login-link'
        self._booking_link = 'booking-link'
        self._vision_cred = 'vision-cred'

        self._driver_count = 'driver-count'
        self._headless = 'headless'
        self._execution_delta = 'execution-delta'
        self._submit_time_sleep = 'submit-time-sleep'
        self._submit_time_offset = 'submit-time-offset'
        self._driver_time_sleep = 'driver-time-sleep'

        self._user = 'user'
        self._password = 'password'

        self._submit_time = 'submit-time'
        self._date = 'date'
        self._section = 'section'
        self._time = 'time'
        self._court = 'court'

        # Default value
        self._vision_cred_dflt = 'credential.json'

        self._driver_count_dflt = '1'
        self._headless_dflt = 'False'
        self._execution_delta_dflt = '3'
        self._submit_time_sleep_dflt = '0.3'
        self._submit_time_offset_dflt = '0.2'
        self._driver_time_sleep_dflt = '0.2'

        # Get config information
        self.candidates = candidates
        self._config = configparser.ConfigParser()
        self._config_found = self._config.read(self.candidates)

        # Make sure ini file exist
        if len(self._config_found) == 0:
            raise ConfigNotFoundError(ConfigError)

    def login_link(self):
        """
        Return config login-link option in GENERAL section
        """
        return self._read_value(self._genaral, self._login_link)

    def booking_link(self):
        """
        Return config login-link option in GENERAL section
        """
        return self._read_value(self._genaral, self._booking_link)

    def vision_cred(self):
        """
        Return config vision api credential setting in GENERAL section
        Default setting: VISION_CRED_DFLT
        """
        cred = self._read_value(self._genaral, self._vision_cred, fallback_val=self._vision_cred_dflt)
        if not os.path.isfile(cred):
            raise MissingFileError(cred)

        return cred

    def driver_count(self):
        """
        Return config driver-count value in DRIVER section
        """
        _count = int(self._read_value(self._driver, self._driver_count,
            fallback_val=self._driver_count_dflt))
        if _count < 1 or _count > 4:
            raise OptionFormatError(self._driver, _count)

        return _count

    def execution_delta(self):
        """
        Return config execution-delta value in DRIVER section
        """
        _delta_time = int(self._read_value(self._driver, self._execution_delta,
            fallback_val=self._execution_delta_dflt))
        if _delta_time < 0:
            raise OptionFormatError(self._driver, _delta_time)

        return _delta_time

    def submit_time_sleep(self):
        """
        Return config submit-time-sleep value in DRIVER section
        """
        _time_sleep = float(self._read_value(self._driver, self._submit_time_sleep,
            fallback_val=self._submit_time_sleep_dflt))
        if _time_sleep < 0:
            raise OptionFormatError(self._driver, _time_sleep)

        return _time_sleep

    def submit_time_offset(self):
        """
        Return config submit-time-offset value in DRIVER section
        """
        _time_sleep = float(self._read_value(self._driver, self._submit_time_offset,
            fallback_val=self._submit_time_offset_dflt))
        if _time_sleep < 0:
            raise OptionFormatError(self._driver, _time_sleep)

        return _time_sleep

    def driver_time_sleep(self):
        """
        Return config driver-time-sleep value in DRIVER section
        """
        _time_sleep = float(self._read_value(self._driver, self._driver_time_sleep,
            fallback_val=self._driver_time_sleep_dflt))
        if _time_sleep < 0:
            raise OptionFormatError(self._driver, _time_sleep)

        return _time_sleep

    def headless(self):
        """
        Return config headless value in DRIVER section
        """
        _headless_mode = self._read_value(self._driver, self._headless, fallback_val=self._headless_dflt)
        self._validate('True|False', self._headless, _headless_mode)

        return _headless_mode == 'True'

    def login_user(self):
        """
        Return config user option in ACCOUNT section
        """
        return self._read_value(self._account, self._user)

    def login_password(self):
        """
        Return config password option in ACCOUNT section
        """
        return self._read_value(self._account, self._password)

    def submit_time(self, section_name):
        """
        Return config SUBMIT_TIME option in section_name section
        """
        _submit_time = self._read_value(section_name, self._submit_time)
        self._validate(r'\d{4}/\d{2}/\d{2}-\d{2}:\d{2}:\d{2}', self._submit_time, _submit_time)

        return _submit_time

    def date(self, section_name):
        """
        Return config DATE option in section_name section
        """
        _date = self._read_value(section_name, self._date)
        self._validate(r'\d{4}/\d{2}/\d{2}', self._date, _date)

        return _date

    def section(self, section_name):
        """
        Return config SECTION option in section_name section
        """
        _section = self._read_value(section_name, self._section)
        self._validate('morning|evening|night', self._section, _section)

        if _section == 'morning':
            return '1'
        if _section == 'evening':
            return '2'
        if _section == 'night':
            return '3'
        raise OptionFormatError(self._section, _section)

    def time(self, section_name):
        """
        Return config TIME option in section_name section
        """
        _time = self._read_value(section_name, self._time)
        self._validate(r'[0-2]\d:00~[0-2]\d:00', self._time, _time)

        return _time

    def court(self, section_name):
        """
        Return config COURT option in section_name section
        """
        _court = self._read_value(section_name, self._court)
        self._validate('羽[0-9]|羽10', self._court, _court)

        return _court


    @classmethod
    def _validate(cls, pattern, key, value):
        """
        Test to make sure there is value for all options
        Input:
            pattern: regular expression object
            key: string - config option key
            value: string - config option value
        """
        _re_pattern = re.compile(r'{}'.format(pattern))

        if _re_pattern.fullmatch(value) is None:
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
class ConfigError(Exception):
    """
    Base class of config exception
    """


class ConfigNotFoundError(ConfigError):
    """
    Raised if not finding ini file
    """

class MissingFileError(ConfigError):
    """
    Raised if file not find
    """
    def __init__(self, file):
        ConfigError.__init__(self)
        self.message = 'File {} not found'.format(file)

class NoSectionError(ConfigError):
    """
    Raised by configparser.NoSectionError
    """
    def __init__(self, section):
        ConfigError.__init__(self)
        self.message = '{} section not found'.format(section)

class NoOptionError(ConfigError):
    """
    Raised by configparser.NoOptionError
    """
    def __init__(self, option):
        ConfigError.__init__(self)
        self.message = '{} option not found'.format(option)

class OptionFormatError(ConfigError):
    """
    Raised if option is in wrong format
    """
    def __init__(self, option, value):
        ConfigError.__init__(self)
        self.message = '{} wrong format: {}'.format(option, value)
