import pandas as pd

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

# print(get_organisation_information(df_all, '“Great Silk Way” International Youth Union'))
# print(get_organisation_information(df_cat, '“Great Silk Way” International Youth Union'))