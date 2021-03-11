import pandas as pd

min_year = 2012
max_year = 2021
year_column_name = 'year'
main_cat_column_name = 'main_cat'
sub_cat_column_name = 'sub_cat'
begin_interval_name = 'begin_int'
end_interval_name = 'end_int'

organisation_name_str = 'organisation name'
country_head_office_str = 'country head office'
lobbying_costs_str = 'lobbying costs'
ep_passes_str = 'EP passes'
lobbyists_fte_str = 'lobbyists (FTE)'
num_meetings_str = '# of meetings'
registered_date_str = 'registered date'

all_file_name = './data/' + 'data_all.csv'
cat_file_name = './data/' + 'data_cat.csv'

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

num_categories = len(main_categories.keys())

def generate_interval(string_interval):
    string_interval = string_interval.replace(",","")
    string_interval = string_interval.replace(" ","")
    start_interval, end_interval = 0,0

    if string_interval.startswith('<'):
        end_interval = int(string_interval[1:])
    elif string_interval.startswith('>'):
        begin_interval = int(string_interval[1:])
        end_interval = begin_interval
    elif string_interval == 'nofigureavailable':
        pass
    elif '-' in string_interval:
        string_interval = string_interval.split('-')
        start_interval = int(string_interval[0])
        end_interval = int(string_interval[1])
    elif string_interval.isdigit():
        start_interval = int(string_interval)
        end_interval = int(string_interval)
    else:
        print(string_interval)


    return start_interval, end_interval

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
                df[begin_interval_name] = 0
                df[end_interval_name] = 0
                for index, row in df.iterrows():
                    lobby_cost_str = row[lobbying_costs_str]
                    begin_int, end_int = generate_interval(lobby_cost_str)
                    df[begin_interval_name][index] = begin_int
                    df[end_interval_name][index] = end_int
                    # row[begin_interval_name] = begin_int
                    # row[end_interval_name] = end_int
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

if __name__ == "__main__":
    print('Starting')
    df_all, df_cat = generate_category_data()
    
    df_all.to_csv(all_file_name, index=False)
    df_cat.to_csv(cat_file_name, index=False)

    # print(generate_interval('< 9,999'))

