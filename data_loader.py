import argparse
import pandas as pd


class DataLoader:
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
        print(self.businesses)

    def load_businesses(self):
        all_businesses = self.data['organisation name']
        return all_businesses.drop_duplicates().to_list()

    def get_top_level_categories(self):
        return tuple(self.top_level_categories)

    def get_low_level_categories(self, category):
        return tuple(self.categories[category])

    def get_businesses(self):
        return tuple(self.businesses)

    def get_countries(self):
        return tuple([0, 1])

DataLoader()