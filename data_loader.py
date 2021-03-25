import pandas as pd
from preprocessing import string_to_int_subcategory, string_to_int_category


class DataLoader:
    """
    A class to load preprocessed data from a file and then make it available for fast access to other processes.
    """
    def __init__(self, file='data/data_cat.csv'):
        self.data = pd.read_csv(file)
        self.categories = {
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
        self.top_level_categories = self.categories.keys()
        self.businesses = self.load_businesses()
        self.countries = self.load_countries()

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

    def get_top_level_categories(self):
        """
        This method gets all top level categories.
        :return: A tuple containing all top level categories.
        """
        return tuple(self.top_level_categories)

    def get_low_level_categories(self, category):
        """
        This method gets all low level categories for a specific top level category.
        :param category: The top level category.
        :return: A tuple of all categories that fall under this top level category.
        """
        return tuple(self.categories[category])

    def get_businesses(self):
        """
        This method gets all the businesses in the dataset.
        :return: A tuple of all distinct businesses.
        """
        return tuple(self.businesses)

    def get_countries(self):
        """
        This method gets all the countries in the dataset.
        :return: A tuple of all distinct countries.
        """
        return tuple(self.countries)

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

    def get_businesses_data(self, businesses):
        """
        This method gets all available data about a list of businesses.
        :param businesses: The businesses that we want data about.
        :return: The rows in the dataset that contain one of these businesses.
        """
        businesses_data = self.data.loc[self.data['organisation name'].isin(businesses)]
        businesses_data = businesses_data.groupby(['organisation name'], as_index=False).idxmax()
        return businesses_data

    def get_subcategory_data(self, category,subcategory):
        """
        This method gets all available data about a list of subcategories.
        :param businesses: The subcategory that we want data about.
        :return: The rows in the dataset that contain one of these subcategories.
        """
        category_nr = string_to_int_category[category]
        subcategory_nr = string_to_int_subcategory[subcategory]
        category_data = self.data.loc[self.data['main_cat'] == category_nr]   
        subcategory_data = category_data.loc[category_data['sub_cat'] == subcategory_nr]
        
        return subcategory_data


