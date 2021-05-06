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
        self.columns = ['organisation name', 'country head office', 'lobbying costs', 'EP passes', 'lobbyists (FTE)',
                        '# of meetings', 'registered date', 'begin_int', 'end_int', 'year', 'main_cat', 'sub_cat']
        self.main_categories_lst = self.load_main_categories()
        self.sub_categories_lst = self.load_sub_categories()
        self.businesses_lst = self.load_businesses()
        self.countries_lst = self.load_countries()

    def load_main_categories(self):
        """
        This method loads all main categories.
        :return: A list containing all main categories.
        """
        main_categories = self.main_categories.keys()
        list(main_categories).sort()
        return main_categories

    def load_sub_categories(self):
        """
        This method gets all sub categories.
        :return: A list containing all sub categories.
        """
        sub_categories = []
        for lst in self.sub_categories.values():
            for sub_category in lst.keys():
                sub_categories.append(sub_category)
        return sub_categories

    def load_businesses(self):
        """
        This method will load all distinct businesses in the dataset into a list.
        :return: A list of all businesses.
        """
        businesses = self.data['organisation name']
        businesses = businesses.drop_duplicates().to_list()
        businesses.sort()
        return businesses

    def load_countries(self):
        """
        This method will load all distinct countries in the dataset into a list.
        :return: A list of all countries.
        """
        countries = self.data['country head office']
        countries = countries.dropna()
        countries = countries.drop_duplicates().to_list()

        # Some names were written wrong, so some hard coded solution to rename those countries.
        countries[countries.index('Afganistan')] = 'Afghanistan'
        countries.remove('Netherlands Antilles')
        countries[countries.index('Gibralter')] = 'Gibraltar'
        countries.sort()

        return countries

    def get_main_categories(self):
        """
        This method gets all main categories.
        :return: A list of all main categories.
        """
        categories = []
        for category in self.main_categories_lst:
            category_dict = dict(label=category, value=category)
            categories.append(category_dict)
        return categories

    def get_sub_categories(self):
        """
        This method gets all sub categories.
        :return: A list of all sub categories.
        """
        sub_categories = []
        for sub_category in self.sub_categories_lst:
            sub_category_dict = dict(label=sub_category, value=sub_category)
            sub_categories.append(sub_category_dict)
        return sub_categories

    def get_sub_categories_for_main(self, category):
        """
        This method gets all sub categories for a specific main category.
        :param category: The main category.
        :return: A tuple of all categories that fall under this main category.
        """
        id = self.main_categories[category]
        sub_categories_lst = self.sub_categories[id].keys()
        sub_categories = []
        for sub_category in sub_categories_lst:
            sub_category_dict = dict(label=sub_category, value=sub_category)
            sub_categories.append(sub_category_dict)

        return sub_categories

    def get_businesses(self):
        """
        This method gets all the businesses in the dataset.
        :return: A tuple of all distinct businesses.
        """
        businesses = []
        for business in self.businesses_lst:
            business_dict = dict(label=business, value=business)
            businesses.append(business_dict)
        return businesses

    def get_countries(self):
        """
        This method gets all the countries in the dataset.
        :return: A dictionary of all distinct countries with key = value.
        """
        countries = []
        for country in self.countries_lst:
            country_dict = dict(label=country, value=country)
            countries.append(country_dict)
        return countries

    def get_country_data(self, country):
        """
        This method returns all available data about a specific country.
        :param country: The country that we want data about.
        :return: The rows in the dataset that contain the country.
        """
        country_data = self.data[self.data['country head office'] == country]
        return country_data

    def get_business_data(self, business):
        """
        This method gets all available data about a specific business.
        :param business: The business that we want data about.
        :return: The rows in the dataset that contain the business.
        """
        business_data = self.data[self.data['organisation name'] == business]
        return business_data

    def get_countries_data(self, countries):
        """
        This method gets all available data about a list of countries.
        :param countries: The countries that we want data about.
        :return: The rows in the dataset that contain one of these countries.
        """
        if countries:
            countries_data = self.data[self.data['country head office'].isin(countries)]
            return countries_data
        else:
            return pd.DataFrame(columns=self.columns)

    def get_categories_data(self, categories):
        """
        This method gets all available data about a list of categories.
        :param categories: The categories that we want data about.
        :return: The rows in the dataset that contain one of these categories.
        """
        category_ids = map(lambda cat: self.main_categories[cat], categories)
        categories_data = self.data[self.data['sub_cat'].isin(category_ids)]
        return categories_data

    def get_businesses_data(self, businesses):
        """
        This method gets all available data about a list of businesses.
        :param businesses: The businesses that we want data about.
        :return: The rows in the dataset that contain one of these businesses.
        """
        businesses_data = self.data[self.data['organisation name'].isin(businesses)]
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
        data = self.data[(self.data['main_cat'] == category_nr) & (self.data['sub_cat'] == subcategory_nr)]

        return data

    def get_country_amount_of_companies(self):
        """
        This method gets all the country names and transforms them to their respective ISO 3 code, together with the amount of
        organisations per country
        """
        countries_bussines_amount = []

        for country in self.countries_lst:
            df_country = self.get_country_data(country)
            countries_bussines_amount.append(len(df_country))

        iso3_codes = coco.convert(names=self.countries_lst, to='ISO3')
        return iso3_codes, countries_bussines_amount
