import argparse
import pandas as pd

min_year = 2012
max_year = 2021
year_column_name = 'year'
main_cat_column_name = 'main_cat'
sub_cat_column_name = 'sub_cat'

organisation_name_str = 'organisation name'
country_head_office_str = 'country head office'
lobbying_costs_str = 'lobbying costs'
ep_passes_str = 'EP passes'
lobbyists_fte_str = 'lobbyists (FTE)'
num_meetings_str = '# of meetings'
registered_date_str = 'registered date'

columns = {
    organisation_name_str: str,
    country_head_office_str: str,
    lobbying_costs_str: str,  # Preprocess this into something of an integer/float/number
    ep_passes_str: int,
    lobbyists_fte_str: float,
    num_meetings_str: int,
    registered_date_str: str
}

main_categories = {
    1: 'Professional consultancies/law firms/self-employed consultants',
    2: 'In-house lobbyists and trade/professional associations',
    3: 'Non-governmental organisations',
    4: 'Think tanks, research and academic institutions',
    5: 'Organisations representing churches and religious communities',
    6: 'Organisations representing local, regional and municipal authorities, other public or mixed entities, etc.'
}

sub_categories = {
    1: {
        1: 'Professional consultancies',
        2: 'Law firms',
        3: 'Self-employed consultants'
    },
    2: {
        1: 'Companies & groups',
        2: 'Trade and business organisations',
        3: 'Trade unions and professional associations',
        4: 'Other in house lobbyists'
    },
    3: {
        1: 'Non-governmental organisations, platforms and networks and similar'
    },
    4: {
        1: 'Think tanks and research institutions',
        2: 'Academic institutions'
    },
    5: {
        1: 'Organisations representing churches and religious communities'
    },
    6: {
        1: 'Regional structures',
        2: 'Other sub-national public authorities'
    }
}

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

num_categories = len(main_categories.keys())


def read_files(columns):
    dataframes = []
    dataframes_cat = []
    for i in range(min_year, max_year + 1):
        #print(i)
        year_string = str(i)
        file_name = './data/' + year_string + '/all/' + 'all_' + year_string + '.csv'
        print('Reading: ', file_name)
        df = pd.read_csv(file_name, dtype=columns)
        df[year_column_name] = i
        dataframes.append(df)

        for j in range(1, num_categories + 1):
            main_cat_str = main_categories[j]
            sub_cat_dict = sub_categories[j]
            for key in sub_cat_dict:
                file_name = './data/' + year_string + '/category/' + str(j) + '/' + str(key) + '.csv'
                print('Reading: ', file_name)
                df = pd.read_csv(file_name, dtype=columns)
                df[year_column_name] = i
                df[main_cat_column_name] = j
                df[sub_cat_column_name] = key
                dataframes_cat.append(df)

    return dataframes, dataframes_cat


def generate_category_data():
    dataframes_all, dataframes_cat = read_files(columns)
    dataframe_all = pd.concat(dataframes_all)
    dataframe_cat = pd.concat(dataframes_cat)
    dataframe_all = dataframe_all.sort_values(by=[organisation_name_str, year_column_name])
    dataframe_cat = dataframe_cat.sort_values(by=[organisation_name_str, year_column_name])
    return dataframe_all, dataframe_cat


def search_rows_with_column_name(df, column_name, column_value):
    df = df.loc[df[column_name] == column_value]
    country_head_office = df[country_head_office_str].tolist()
    lobbying_costs = df[lobbying_costs_str].tolist()
    ep_passes = df[ep_passes_str].tolist()
    lobbyists_fte = df[lobbyists_fte_str].tolist()
    num_meetings = df[num_meetings_str].tolist()
    registered_date = df[registered_date_str].tolist()
    year = df[year_column_name].tolist()
    result = {country_head_office_str: country_head_office, lobbying_costs_str: lobbying_costs, ep_passes_str: ep_passes,
              lobbyists_fte_str: lobbyists_fte, num_meetings_str: num_meetings, registered_date_str: registered_date}
    return result


def get_organisation_information(df, company_name):
   return search_rows_with_column_name(df, organisation_name_str, company_name)


def get_top_level_categories():
    return tuple(categories.keys())


def get_low_level_categories(category):
    return tuple(categories[category])


def get_businesses():



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
