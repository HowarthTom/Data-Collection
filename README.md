# Data Collection Pipeline

This project uses various webscraping and html parsing tools such as selenium, chromedriver, beatifulsoup to collect and analyse data from the rottentomatoes website.

## Milestone 1 - Choosing a website 

* Rotten Tomatoes was chosen for this project as it contains lots of different forms of data (movie/show info, images, links to other pages), which is updated and changed on a regular basis. 
* This provides the challenge of making a webscraper that both targets specific data and adapts to change. 
* Furthermore, the data collected from this website can be used to provide some interesting and useful information to the user, such as ranking by critic and audience scores simultaneously.

## Milestone 2 - Creating the scraper class and methods

* The scraper class contains several essential methods
    - The constructor (__init__()), initialises chromedriver and class parameters, opens rotten tomatoes link.
    - Accept cookies method.
    - Selection method, navigates to either the TV shows or Movies page.
    - Data loading method, loads the desired amount of data to scrape.
    - Get img data method
    - Get tabular data method, scrapes the desired data.
        - This is split across two methods, to scrape additional data that requires further web navigation.
    - Save data method, saves the data locally as a JSON file and JPG image.

* These methods ensure the scraper class can handle website navigation without any errors, and collect data for both movies and tv shows within the same class.