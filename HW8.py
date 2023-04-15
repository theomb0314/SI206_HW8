# Your name: 
# Your student id:
# Your email:
# List who you have worked with on this homework:

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def load_rest_data(db):
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    """
    conn = sqlite3.connect(db)
    c = conn.cursor()
    
    # Get restaurant data
    c.execute('''SELECT r.name, c.category, b.building, r.rating
                 FROM restaurants r
                 JOIN categories c ON r.category_id = c.id
                 JOIN buildings b ON r.building_id = b.id''')
    
    # Create nested dictionary
    rest_data = {}
    for row in c.fetchall():
        rest_name, category, building, rating = row
        rest_data[rest_name] = {'category': category, 'building': building, 'rating': rating}
    
    conn.close()
    return rest_data
    pass

def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """

    dbc = load_rest_data(db)
    category_counts = {}

    for restaurant in dbc:
        category = dbc[restaurant]['category']
        category_counts[category] = category_counts.get(category, 0) + 1

    # Create bar chart
    fig, ax = plt.subplots()
    colors = ['yellow', 'hotpink'] * ((len(category_counts) // 2) + 1)
    bars = ax.bar(category_counts.keys(), category_counts.values(), color=colors)

    ax.set_xlabel('Restaurant Categories')
    ax.set_ylabel('Count')
    ax.set_title('Restaurant Categories and Counts')
    plt.xticks(rotation=90)

    # Set dark mode
    plt.style.use('dark_background')

    # Add bar totals
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', color='white')

    plt.show()
    return category_counts
    pass

def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    dbc = load_rest_data(db)
    restaurant_names = []

    # Loop through each restaurant in the database
    for restaurant, values in dbc.items():
        # Check if the restaurant is in the specified building and add it to the list if it is
        if values['building'] == building_num:
            restaurant_names.append(restaurant)

    # Sort the list of restaurant names by their rating from highest to lowest
    restaurant_names.sort(key=lambda x: dbc[x]['rating'], reverse=True)

    return restaurant_names
    pass

#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    pass

#Try calling your functions here
def main():
    restaurant_data = load_rest_data("South_U_Restaurants.db")
    print(restaurant_data)
    category_counts = plot_rest_categories("South_U_Restaurants.db")
    building_num = '1101'
    restaurant_list = find_rest_in_building(building_num, "South_U_Restaurants.db")
    print(f"Restaurants in building {building_num}: {restaurant_list}")

    pass

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    # def test_get_highest_rating(self):
    #     highest_rating = get_highest_rating('South_U_Restaurants.db')
    #     self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
