import argparse
import pandas as pd


def preprocess(data):
    columns = {
        'organisation name': str,
        'country head office': str,
        'lobbying costs': str,  # Preprocess this into something of an integer/float/number
        'EP passes': int,
        'lobbyists (FTE)': float,
        '# of meetings': int,
        'registered date': str
    }
    recent_file = f'{data}/2021/all/all_2021.csv'
    df = pd.read_csv(recent_file, dtype=columns)
    print("DUPLICATES")
    print(df.duplicated)
    print(df.size)
    print("DUPLICATES DONE")
    print(df.dtypes)
    print(df.iloc[0])
    return df


if __name__ == "__main__":
    print('Starting the preprocessing of the data')

    # Starting the parser for the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', default='data', help='The folder containing the data')
    args = parser.parse_args()

    data = args.data

    preprocess(data)

    print('Completed successfully')
