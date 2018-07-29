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
        """

        self.ID = 'person id'
        self.DATE = 'date'
        self.FROM_STATION = 'from station'
        self.TO_STATION = 'to station'
        self.TRAIN_NO = 'train number'
        self.QUANTITY = 'quantity'

        # Get config information
        self._config = configparser.ConfigParser()
        self._config_found = self._config.read(candidates)

        # Make sure ini file exist
        if len(self._config_found) == 0:
            logger.warning('No config file found')
            sys.exit(1)

        # Set default directory
        # try:
        #     self._config.set(self.DEFAULT_SEC, self.DIRECTORY, os.path.join(HOME,self.DEFAULT_DIR))
        # except NoSectionError:
        #     logger.warning('Cannot find {} section in ini files.'.format(self.DEFAULT_SEC))
        #     sys.exit(5)

        # Write directory option setting to file
        # self._write_file()

        # Set section
        # try:
        #     self._config_section = self._config[self.CONFIG_SEC]
        # except KeyError:
        #     logger.warning('Cannot find {} section in ini files.'.format(self.CONFIG_SEC))
        #     sys.exit(3)


    # def useragent(self):
    #     user_agent = agentcl.UserAgent().random_computer()
    #
    #     if len(user_agent) != 0:
    #         self._config.set(self.CONFIG_SEC, self.USERAGENT, user_agent)
    #         self._write_file()
    #         return user_agent
    #     else:
    #         return self._user_agent

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
            logger.warning('Cannot find {} section in .ini files.')
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

    # def _write_file(self):
    #     """
    #     Write config settings to file
    #     """
    #     for file in self._config_found:
    #         with open(file, 'w') as config_file:
    #             self._config.write(config_file)


if __name__ == '__main__':
    config = Config('.train_tickets.ini')

    print(config.id('INFO01'))
    print(config.date('INFO01'))
    print(config.from_station('INFO01'))
    print(config.to_station('INFO01'))
    print(config.train_number('INFO01'))
    print(config.quantity('INFO01'))
