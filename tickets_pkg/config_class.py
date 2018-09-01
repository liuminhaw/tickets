"""
Program:
    Class for reading .ini file
Author:
    haw
Version:
    0.0.0
"""

import sys
import configparser
from tickets_pkg import logging_class as logcl
from tickets_pkg import identifier
# import logging_class as logcl

logger = logcl.PersonalLog('config_class')

class Config():

    def __init__(self, candidates):
        """
        Input:
            candidates - ini config files list
        Error Code:
            1 - No config ini file found
            3 - CONFIG section not exist
            5 - DEFAULT section not exist

            11 - Some needed key not exist in ini files

            21 - Time interval config error
            22 - Web driver config error
            23 - No section read error
            24 - Personal ID config error
            25 - Date config error
            26 - Train number config error
            27 - Ticket quantity config error
            28 - Puyoma type config error
        """

        self.WEB_DRIVER = 'web driver'
        self.TIME_INTERVAL = 'time interval'
        self.ID = 'person id'
        self.DATE = 'date'
        self.FROM_STATION = 'from station'
        self.TO_STATION = 'to station'
        self.TRAIN_NO = 'train number'
        self.QUANTITY = 'quantity'
        self.TRAIN_TYPE = 'puyoma'

        # Get config information
        self._config = configparser.ConfigParser()
        self._config_found = self._config.read(candidates)

        # Make sure ini file exist
        if len(self._config_found) == 0:
            logger.warning('No config file found')
            sys.exit(1)

        # Check config file format
        self._check()

    def web_driver(self):
        config_section = self._read_section('DRIVER')
        return self._read_key(config_section, self.WEB_DRIVER)

    def time_interval(self):
        config_section = self._read_section('DRIVER')
        return self._read_key(config_section, self.TIME_INTERVAL)

    def target_sections(self):
        config_section = self._read_section('CONFIG')
        sections = []

        for section in config_section:
            sections.append(config_section[section])

        return sections

    def id(self, section):
        config_section = self._read_section(section)
        return self._read_key(config_section, self.ID)

    def date(self, section):
        config_section = self._read_section(section)
        return self._read_key(config_section, self.DATE)

    def from_station(self, section):
        config_section = self._read_section(section)
        return self._read_key(config_section, self.FROM_STATION)

    def to_station(self, section):
        config_section = self._read_section(section)
        return self._read_key(config_section, self.TO_STATION)

    def train_number(self, section):
        config_section = self._read_section(section)
        return self._read_key(config_section, self.TRAIN_NO)

    def quantity(self, section):
        config_section = self._read_section(section)
        return self._read_key(config_section, self.QUANTITY)

    # def is_puyoma(self, section):
    #     config_section = self._read_section(section)
    #     return self._read_key(config_section, self.TRAIN_TYPE)

    def _check(self):

        # Valid web driver
        if not identifier.webdriver_check(self.web_driver()):
            logger.warning('Config web driver not supported type.')
            sys.exit(22)

        # Valid time interval
        if not identifier.time_interval_check(self.time_interval()):
            logger.warning('Config time interval format error.')
            sys.exit(21)

        # Valid list of sections in CONFIG
        if not identifier.section_exist_check(self.target_sections()):
            logger.warning('No section set to be read in CONFIG.')
            sys.exit(23)

        # Each section check
        for section in self.target_sections():
            # Valid personal id
            if not identifier.id_check(self.id(section)):
                logger.warning('Invalid ID in section {}'.format(section))
                sys.exit(24)

            # Valid date value
            if not identifier.date_check(self.date(section)):
                logger.warning('Invalid date in section {}'.format(section))
                sys.exit(25)

            # Valid train number
            if not identifier.train_number_check(self.train_number(section)):
                logger.warning('Invalid train number in section {}'.format(section))
                sys.exit(26)

            # Valid quantity
            if not identifier.quantity_check(self.quantity(section)):
                logger.warning('Invalid quantity in section {}'.format(section))
                sys.exit(27)

            # Valid puyoma
            # if not identifier.puyoma_check(self.is_puyoma(section)):
            #     logger.warning('Invalid puyoma type choice in section {}'.format(section))
            #     sys.exit(28)


    def _read_section(self, name):
        """
        Read section in .ini files and return the read object
        Input:
            name - section name
        Return:
            Configuration section object
        """
        try:
            section = self._config[name]
        except:
            logger.warning('Cannot find {} section in .ini files.'.format(name))
            sys.exit(3)
        else:
            return section

    def _read_key(self, section, key):
        """
        Input:
            section - Config file section
            key - ini file option key
        Return:
            Value of the key
        """
        value = section.get(key)
        if value is None:
            logger.warning('No {} key exist in ini files.'.format(key))
            sys.exit(11)
        else:
            return value


if __name__ == '__main__':
    config = Config('train_tickets.ini')

    print(config.web_driver())
    print(config.target_sections())

    print(config.id('INFO01'))
    print(config.date('INFO01'))
    print(config.from_station('INFO01'))
    print(config.to_station('INFO01'))
    print(config.train_number('INFO01'))
    print(config.quantity('INFO01'))
    print(config.is_puyoma('INFO01'))
