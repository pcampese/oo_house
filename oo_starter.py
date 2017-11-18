#!/usr/bin/env python

# Import
# Built in Modules
import logging

# Custom Modules
from m_house import House
from m_house import read_csv
from m_house import read_csv2

# Configure Logging
import logging
logger = logging.getLogger(__name__)

def main():
    house1 = House(1)
    # logger.info('house1.id = {}'.format(house1.id))
    logger.info('house1.get_all = {}'.format(house1.get_all()))

    house1.set_address("1 Main St, Boston, MA 12345")
    logger.info('house1.get_address = {}'.format(house1.get_address()))
    logger.info('house1.get_all = {}'.format(house1.get_all()))

    # Read the csv file
    read_csv2('data.csv')

    # logger.info('Adding tricks to dog1...')
    # dog1.add_trick('jump')
    # dog1.add_trick("sleep")
    # logger.info('dog1.tricks = {}'.format(dog1.tricks))

    # # Make a bunch of dogs!
    # logger.info('Making a bunch of dogs!')
    # dog_list = []
    # for i in xrange(4):
        # dog_name = 'dog{}'.format(i)
        # dog_list.append(Dog(dog_name))

    # for d in dog_list:
        # logger.info('{}.name = {}'.format(d, d.name))

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG) # INFO or DEBUG
    logger.info('Logging Initialized')
    main()