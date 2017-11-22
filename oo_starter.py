#!/usr/bin/env python

# Import
# Built in Modules
import logging
import pprint

# Custom Modules
from m_house import House
from m_house import CsvParser


# Configure Logging
import logging
logger = logging.getLogger(__name__)

def main():
    # house1 = House('data_mini.csv')
    # # logger.info('house1.id = {}'.format(house1.id))
    # logger.info('house1.get_all = {}'.format(house1.get_all()))

    # house1.set_address("1 Main St, Boston, MA 12345")
    # logger.info('house1.get_address = {}'.format(house1.get_address()))
    # logger.info('house1.get_all = {}'.format(house1.get_all()))

    logger.info('Creating the parser')
    c = CsvParser('data.csv')

    # logger.info('Printing the data')
    # c.print_csv()

    # Generate a list of houses
    # First, split the data
    logger.info('Splitting the data')
    split_csv = c.split()

    # Now, populate the list of hosues
    houses = []
    for csv in split_csv:
        houses.append(House(csv))

    # Finally, print out the house info
    for house in houses:
        logger.info('house_details = <{}>'.format(house.get_all()))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO) # INFO or DEBUG
    logger.info('Logging Initialized')
    main()