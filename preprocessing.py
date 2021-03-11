import argparse
import itertools
import pandas as pd

categories = {
        'Professional consultancies/law firms/self-employed consultants': (
            'Professional consultancies',
            'Law firms',
            'Self-employed consultants'
        ),
        'In-house lobbyists and trade/professional associations': (
            'Companies & groups',
            'Trade and business organisations',
            'Trade unions and professional associations',
            'Other in house lobbyists'
        ),
        'Non-governmental organisations': (
            'Non-governmental organisations, platforms and networks and similar',
        ),
        'Think tanks, research and academic institutions': (
            'Think tanks and research institutions',
            'Academic institutions'
        ),
        'Organisations representing churches and religious communities': (
            'Organisations representing churches and religious communities',
        ),
        'Organisations representing local, regional and municipal authorities, other public or mixed entities, etc.': (
            'Regional structures',
            'Other sub-national public authorities',
            'Transnational associations and networks of public regional or other sub-national authorities',
            'Other public or mixed entities, created by law whose purpose is to act in the public interest'
        )
    }


def get_top_level_categories():
    return tuple(categories.keys())


def get_low_level_categories(category):
    return tuple(categories[category])


def get_businesses():
    return tuple(['a', 'b'])


def get_countries():
    return tuple(['a', 'b'])


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
