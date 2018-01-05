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
    # newton = create_dataset('data_newton.csv')
    # natick = create_dataset('data_natick.csv')
    # wayland = create_dataset('data_wayland.csv')
    # arlington = create_dataset('data_arlington.csv')

    # Create Dataset Dictionary
    dataset_dict = {
        # 'lexington': create_dataset('data_lexington.csv'),
        # 'belmont': create_dataset('data_belmont.csv'),
        # 'weston': create_dataset('data_weston.csv'),
        # 'newton': create_dataset('data_newton.csv'),
        # 'wayland': create_dataset('data_wayland.csv'),
        # 'arlington': create_dataset('data_arlington.csv'),
        'arlington 3 Year': create_dataset('redfin_arlington_3yr.csv'),
        # 'wellesley': create_dataset('data_wellesley.csv'),
        # 'needham': create_dataset('data_needham.csv'),
        # 'bedford': create_dataset('data_bedford.csv'),
        # 'natick': create_dataset('data_natick.csv'),
        # 'lincoln': create_dataset('data_lincoln.csv'),
        # 'burlington': create_dataset('data_burlington.csv'),
        # 'watertown': create_dataset('data_watertown.csv'),
                    }

    # Set some filters
    for dataset in dataset_dict.values():
        dataset.filters['beds'] = 3
        dataset.filters['baths'] = 2
        # dataset.filters['year'] = 2017
        dataset.apply_filters()

    # # Dataset percentiles
    # logging.info('Percentiles')
    # for dataset in dataset_dict.values():
        # dataset.print_percentile_prices()

    # Create Analysis object
    insight = Analysis(dataset_dict)

    # Analyze the data
    # logger.info('time_chart: months')
    # insight.time_chart('month', 1, 12)

    logger.info('time_chart: years')
    # insight.time_chart('year', 1994, 2017)
    insight.time_chart_percentile('year', 2015, 2017)
    insight.time_chart_percentile('month', 1, 12)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO) # INFO or DEBUG
    logger.info('Logging Initialized')
    main()