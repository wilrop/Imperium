import pandas as pd

min_year = 2012
max_year = 2021

columns = {
        'organisation name': str,
        'country head office': str,
        'lobbying costs': str,  # Preprocess this into something of an integer/float/number
        'EP passes': int,
        'lobbyists (FTE)': float,
        '# of meetings': int,
        'registered date': str
    }

def read_files(columns):
    dataframes = []
    for i in range(min_year, max_year + 1):
        #print(i)
        year_string = str(i)
        file_name = './data/' + year_string + '/all/' + 'all_' + year_string + '.csv'
        print('Reading: ', file_name)
        df = pd.read_csv(file_name, dtype=columns)
        df['year'] = i
        dataframes.append(df)
    return dataframes

def main():
    dataframes = read_files(columns)
    categories_dataframe = pd.concat(dataframes)
    categories_dataframe = categories_dataframe.sort_values(by=['organisation name', 'year'])
    print(categories_dataframe)

if __name__ == "__main__":
    print('Starting Categories')
    main()