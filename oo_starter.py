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
from m_house import Redfin

# Configure Logging
import logging
logger = logging.getLogger(__name__)

def create_dataset(redfin_csv):
    logger.info('-- Creating dataset --')

    logger.info('--> Creating the parser')
    c = CsvParser(redfin_csv)

    # Generate a list of houses
    # First, split the data
    logger.info('--> Splitting the data')
    split_csv = c.split()

    # Now, populate the list of houses
    logger.info('--> Populating houses')
    houses = []
    for csv in split_csv:
        houses.append(House(csv))

    # Create a Dataset
    logger.info('--> Creating the dataset')
    dataset = Dataset(houses)

    return dataset


def main():
    # Create Datasets
    dataset = create_dataset('data_newton.csv')
    dataset2 = create_dataset('data_natick.csv')
    dataset3 = create_dataset('data_leominster.csv')

    # Create Dataset Dictionary
    dataset_dict = {'newton': dataset,
                    'natick': dataset2,
                    'leominster': dataset3}

    # Create Analysis object
    insight = Analysis(dataset_dict)

    # Analyze the data
    logger.info('time_chart: months')
    insight.time_chart('month', 1, 12)

    logger.info('time_chart: years')
    insight.time_chart('year', 1994, 2017)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO) # INFO or DEBUG
    logger.info('Logging Initialized')
    main()