import argparse
import pandas as pd


def preprocess(file):
    df = pd.read_csv(file)


if __name__ == "__main__":
    print('Starting the preprocessing of the data')

    # Starting the parser for the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', default='data.csv', help='The file containing the data')
    args = parser.parse_args()

    file = args.file

    preprocess(file)

    print('Completed successfully')
