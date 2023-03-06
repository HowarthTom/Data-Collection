import unittest
import os
import sys
sys.path.append('../')
from scraper.saver import Saver

class SaverTestcase(unittest.TestCase):

    def setUp(self):
        self.item_dict = {
            "Title": "THE_LAST_OF_US",
            "Tomatometer": 96,
            "Audience Score": 90,
            "Synopsis": "Joel and Ellie must survive ruthless killers and monsters on a trek across America after an outbreak.",
            "TV Network": "HBO",
            "Premiere Date": "Jan 15, 2023",
            "Genre": "Action",
            "Img": "https://resizing.flixster.com/T-YbkLxt3WvVPB2ZLnHUT8nYb68=/206x305/v2/https://resizing.flixster.com/2TwYzc7hklVW2s4fN1ypuyYWMj0=/ems.cHJkLWVtcy1hc3NldHMvdHZzZXJpZXMvYjBiZTZiODMtODQ1OC00MDY3LTkzNTItZjZlMzQ5ZGM1MzEwLmpwZw==",
            "Timestamp": "06-Mar-2023 (15:34:08.470630)",
            "ID": "846bdd65-d825-406f-8a36-895b1be8e152"
        }
        self.title = self.item_dict['Title']
        self.file_path = os.path.abspath(f'../raw_data/{self.title}')
        self.file_path_dict = os.path.abspath(f'../raw_data/{self.title}/data.json')
        self.file_path_img = os.path.abspath(f'../raw_data/{self.title}/{self.title}.jpg')
        save = Saver(self.item_dict)
        save.save()

    def test_save(self):
        self.assertTrue(os.path.exists(self.file_path))
        self.assertTrue(os.path.exists(self.file_path_dict))
        self.assertTrue(os.path.exists(self.file_path_img))
