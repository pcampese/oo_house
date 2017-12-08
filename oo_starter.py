#!/usr/bin/env python

# Import
# Built in Modules
import logging
import locale   # For currency display

# Custom Modules
from m_house import House
from m_house import CsvParser
from m_house import Dataset
from m_house import Analysis


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
    c = CsvParser('data_newton.csv')

    # logger.info('Printing the data')
    # c.print()

    # Generate a list of houses
    # First, split the data
    logger.info('Splitting the data')
    split_csv = c.split()

    # Now, populate the list of hosues
    houses = []
    for csv in split_csv:
        houses.append(House(csv))

    # Create a Dataset
    logger.info('Creating the dataset')
    dataset = Dataset(houses)

    # Calculate some stuff from the dataset
    dataset.print_average_price()
    dataset.print_median_price()

    insight = Analysis(dataset)
    insight.history_chart(1994, 2017)

    # # 2017
    # logger.info('2017')
    # dataset.clear_filters()
    # dataset.filters['year'] = 2017
    # dataset.apply_filters()
    # dataset.print_average_price()
    # dataset.print_median_price()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO) # INFO or DEBUG
    logger.info('Logging Initialized')
    main()