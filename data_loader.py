import itertools
import pandas as pd
import country_converter as coco
import numpy as np
from preprocessing import string_to_int_subcategory, string_to_int_category


class DataLoader:
    """
    A class to load preprocessed data from a file and then make it available for fast access to other processes.
    """

    def __init__(self, file='data/data_cat.csv'):
        self.data = pd.read_csv(file)
        self.main_categories = {
            'Professional consultancies/law firms/self-employed consultants': 1,
            'In-house lobbyists and trade/professional associations': 2,
            'Non-governmental organisations': 3,
            'Think tanks, research and academic institutions': 4,
            'Organisations representing churches and religious communities': 5,
            'Organisations representing local, regional and municipal authorities, other public or mixed entities, etc.': 6
        }

        self.sub_categories = {
            1: {
                'Professional consultancies': 1,
                'Law firms': 2,
                'Self-employed consultants': 3
            },
            2: {
                'Companies & groups': 1,
                'Trade and business organisations': 2,
                'Trade unions and professional associations': 3,
                'Other in house lobbyists': 4
            },
            3: {
                'Non-governmental organisations, platforms and networks and similar': 1
            },
            4: {
                'Think tanks and research institutions': 1,
                'Academic institutions': 2
            },
            5: {
                'Organisations representing churches and religious communities': 1
            },
            6: {
                'Regional structures': 1,
                'Other sub-national public authorities': 2
            }
        }

        self.main_categories_lst = self.load_main_categories()
        self.sub_categories_lst = self.load_sub_categories()
        self.businesses_lst = self.load_businesses()
        self.countries_lst = self.load_countries()

    def load_main_categories(self):
        """
        This method loads all main categories.
        :return: A list containing all main categories.
        """
        return self.main_categories.keys()

    def load_sub_categories(self):
        """
        This method gets all sub categories.
        :return: A list containing all sub categories.
        """
        sub_categories = []
        for lst in self.sub_categories.values():
            sub_categories.append(lst.keys())
        return sub_categories

    def load_businesses(self):
        """
        This method will load all distinct businesses in the dataset into a list.
        :return: A list of all businesses.
        """
        all_businesses = self.data['organisation name']
        return all_businesses.drop_duplicates().to_list()

    def load_countries(self):
        """
        This method will load all distinct countries in the dataset into a list.
        :return: A list of all countries.
        """
        all_countries = self.data['country head office']
        return all_countries.drop_duplicates().to_list()

    def get_main_categories(self):
        """
        This method gets all main categories.
        :return: A tuple of all main categories.
        """
        return tuple(self.main_categories_lst)

    def get_sub_categories(self):
        """
        This method gets all sub categories.
        :return: A tuple of all sub categories.
        """
        return tuple(self.sub_categories_lst)

    def get_sub_categories_for_main(self, category):
        """
        This method gets all sub categories for a specific main category.
        :param category: The main category.
        :return: A tuple of all categories that fall under this main category.
        """
        id = self.main_categories[category]
        return tuple(self.sub_categories[id].keys())

    def get_businesses(self):
        """
        This method gets all the businesses in the dataset.
        :return: A tuple of all distinct businesses.
        """
        return tuple(self.businesses_lst)

    def get_countries(self):
        """
        This method gets all the countries in the dataset.
        :return: A tuple of all distinct countries.
        """
        return tuple(self.countries_lst)

    def get_country_data(self, country):
        """
        This method returns all available data about a specific country.
        :param country: The country that we want data about.
        :return: The rows in the dataset that contain the country.
        """
        country_data = self.data.loc[self.data['country head office'] == country]
        return country_data

    def get_business_data(self, business):
        """
        This method gets all available data about a specific business.
        :param business: The business that we want data about.
        :return: The rows in the dataset that contain the business.
        """
        business_data = self.data.loc[self.data['organisation name'] == business]
        return business_data

    def get_countries_data(self, countries):
        """
        This method gets all available data about a list of countries.
        :param countries: The countries that we want data about.
        :return: The rows in the dataset that contain one of these countries.
        """
        countries_data = self.data.loc[self.data['country head office'].isin(countries)]
        countries_data = countries_data.groupby(['country head office'], as_index=False).idxmax()
        return countries_data

    def get_categories_data(self, categories):
        """
        This method gets all available data about a list of categories.
        :param categories: The categories that we want data about.
        :return: The rows in the dataset that contain one of these categories.
        """
        category_ids = map(lambda cat: self.main_categories[cat], categories)
        categories_data = self.data.loc[self.data['sub_cat'].isin(category_ids)]
        categories_data = categories_data.groupby(['sub_cat'], as_index=False).idxmax()
        return categories_data

    def get_businesses_data(self, businesses):
        """
        This method gets all available data about a list of businesses.
        :param businesses: The businesses that we want data about.
        :return: The rows in the dataset that contain one of these businesses.
        """
        businesses_data = self.data.loc[self.data['organisation name'].isin(businesses)]
        businesses_data = businesses_data.groupby(['organisation name'], as_index=False).idxmax()
        return businesses_data

    def get_subcategory_data(self, category, subcategory):
        """
        This method gets all available data about a list of subcategories.
        :param category: The main category.
        :param subcategory: The sub category.
        :return: The rows in the dataset that contain one of these subcategories.
        """
        category_nr = string_to_int_category[category]
        subcategory_nr = string_to_int_subcategory[subcategory]
        category_data = self.data.loc[self.data['main_cat'] == category_nr]
        subcategory_data = category_data.loc[category_data['sub_cat'] == subcategory_nr]

        return subcategory_data

    def get_country_amount_of_companies(self):
        """
        This method gets all the country names and transforms them to their respective ISO 3 code, together with the amount of
        organisations per country
        """
        countries = list(self.get_countries())
        countries_iso = []
        countries_bussines_amount = []

        # Some names were writting wrong, so some hard coded solution to rename those countries.
        countries[countries.index('Afganistan')] = 'Afghanistan'
        countries.remove('Netherlands Antilles')
        countries[countries.index('Gibralter')] = 'Gibraltar'
        countries = [country for country in countries if str(country) != 'nan']

        for country in countries:
            df_country = self.get_country_data(country)
            countries_bussines_amount.append(len(df_country))

        iso3_codes = coco.convert(names=countries, to='ISO3')
        return iso3_codes, countries_bussines_amount
