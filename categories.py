import pandas as pd

min_year = 2012
max_year = 2021
year_column_name = 'year'

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

def read_files(columns):
    dataframes = []
    for i in range(min_year, max_year + 1):
        #print(i)
        year_string = str(i)
        file_name = './data/' + year_string + '/all/' + 'all_' + year_string + '.csv'
        print('Reading: ', file_name)
        df = pd.read_csv(file_name, dtype=columns)
        df[year_column_name] = i
        dataframes.append(df)
    return dataframes

def generate_category_data():
    dataframes = read_files(columns)
    categories_dataframe = pd.concat(dataframes)
    categories_dataframe = categories_dataframe.sort_values(by=[organisation_name_str, year_column_name])
    return categories_dataframe

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

if __name__ == "__main__":
    print('Starting Categories')
    df = generate_category_data()
    print(get_organisation_information(df, '“Great Silk Way” International Youth Union'))