import pandas as pd
import country_converter as coco


class DataLoader:
    """
    A class to load preprocessed data from a file and then make it available for fast access to other processes.
    """

    def __init__(self, file='data/data_cat.csv'):
        self.data = pd.read_csv(file)
        self.columns = ['organisation name', 'country head office', 'lobbying costs', 'EP passes', 'lobbyists (FTE)',
                        '# of meetings', 'registered date', 'begin_int', 'end_int', 'year', 'main_cat', 'sub_cat']
        self.main_categories_lst = ['Professional consultancies/law firms/self-employed consultants',
                                    'In-house lobbyists and trade/professional associations',
                                    'Non-governmental organisations',
                                    'Think tanks, research and academic institutions',
                                    'Organisations representing churches and religious communities',
                                    'Organisations representing local, regional and municipal authorities, other public or mixed entities, etc.']
        self.sub_categories_lst = ['Professional consultancies', 'Law firms', 'Self-employed consultants',
                                   'Companies & groups', 'Trade and business organisations',
                                   'Trade unions and professional associations', 'Other in house lobbyists',
                                   'Non-governmental organisations, platforms and networks and similar',
                                   'Think tanks and research institutions', 'Academic institutions',
                                   'Organisations representing churches and religious communities',
                                   'Regional structures', 'Other sub-national public authorities']
        self.organisations_lst = self.load_organisations()
        self.countries_lst = self.load_countries()

    def load_organisations(self):
        """
        This method will load all distinct organisations in the dataset into a list.
        :return: A list of all organisations.
        """
        organisations = self.data['organisation name']
        organisations = organisations.drop_duplicates().to_list()
        organisations.sort()
        return organisations

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

    def get_organisations(self):
        """
        This method gets all the organisations in the dataset.
        :return: A list of dictionaries with a key label and a key value that both have as value the name of an
        origanisation.
        """
        organisations = []
        for organisation in self.organisations_lst:
            organisation_dict = dict(label=organisation, value=organisation)
            organisations.append(organisation_dict)
        return organisations

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

    def get_sub_categories_data(self, categories):
        """
        This method gets all available data about a list of categories.
        :param categories: The categories that we want data about.
        :return: The rows in the dataset that contain one of these categories.
        """
        if categories:
            categories_data = self.data[self.data['sub_cat'].isin(categories)]
            return categories_data
        else:
            return pd.DataFrame(columns=self.columns)

    def get_organisations_data(self, organisations):
        """
        This method gets all available data about a list of organisations.
        :param organisations: The organisations that we want data about.
        :return: The rows in the dataset that contain one of these organisations.
        """
        if organisations:
            organisations_data = self.data[self.data['organisation name'].isin(organisations)]
            return organisations_data
        else:
            return pd.DataFrame(columns=self.columns)

    def get_country_amount_of_organisations(self):
        """
        This method gets all the country names and transforms them to their respective ISO 3 code, together with the
        amount of organisations per country
        """
        countries_organisations_amount = []

        for country in self.countries_lst:
            df_country = self.get_countries_data([country])
            countries_organisations_amount.append(len(df_country))

        iso3_codes = coco.convert(names=self.countries_lst, to='ISO3')
        return iso3_codes, countries_organisations_amount, self.countries_lst
