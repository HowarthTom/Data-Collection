import os
import json
import requests

class Saver:
    '''
    This class creates a local folder for each TV show and saves the dictionary and img data inside

    Parameters:
    ----------
    item_dict: dict
        The dictionary used to store all of the information for a particular TV show

    
    Attributes:
    ----------
    item_dict: dict
        The dictionary used to store all of the information for a particular TV show
    img: str
        The TV show's poster img url
    title: str
        The TV show's title
    file_path: str
        The location in the directory where the files will be saved 

    
    Methods:
    -------
    save_item_dict()
        Creates the folder for the TV show if it does not already exist and saves the dictionary in the folder as a JSON file
    save_img()
        Reads the content of the poster img url and saves it in the folder as a JPG file
    save()
        Calls the other methods 
    '''
    def __init__(self, item_dict):
        self.item_dict = item_dict
        self.img = self.item_dict['Img']
        self.title = self.item_dict['Title']
        self.file_path = os.path.abspath(f'../raw_data/{self.title}')

    def save_item_dict(self):
        if not os.path.exists(self.file_path):
            os.makedirs(self.file_path)
        with open(f'{self.file_path}/data.json', 'w') as fp:
            json.dump(obj=self.item_dict, indent=4, fp=fp)

    def save_img(self):
        img_data = requests.get(self.img).content
        with open(f'{self.file_path}/{self.item_dict["Title"]}.jpg', 'wb') as handler:
            handler.write(img_data)

    def save(self):
        Saver.save_item_dict(self)
        Saver.save_img(self)
        print(f'{self.title} scraped successfully')


if __name__ == '__main__':
    test_item = {'Title': 'THE_LAST_OF_US', 'Tomatometer': '96%', 'Audience Score': '90%', 'Synopsis': 'Joel and Ellie must survive ruthless killers and monsters on a trek across America after an outbreak.', 'TV Network': 'HBO', 'Premiere Date': 'Jan 15, 2023', 'Genre': 'Action', 'Img': 'https://resizing.flixster.com/T-YbkLxt3WvVPB2ZLnHUT8nYb68=/206x305/v2/https://resizing.flixster.com/2TwYzc7hklVW2s4fN1ypuyYWMj0=/ems.cHJkLWVtcy1hc3NldHMvdHZzZXJpZXMvYjBiZTZiODMtODQ1OC00MDY3LTkzNTItZjZlMzQ5ZGM1MzEwLmpwZw==', 'Timestamp': '02-Mar-2023 (13:40:22.150968)', 'ID': 'cf5a5ea2-cae7-4f91-9968-677821b80ff7'}
    save = Saver(test_item)
    save.save()