from bs4 import BeautifulSoup
import requests
import json


site = "https://www.vegrecipesofindia.com/"
recipe = 'Palak Paneer Recipe | 2 Variations'

# websites tried:
#   https://www.ambitiouskitchen.com/
#   https://www.bonappetit.com/


recipes = ['Slow Cooker Chicken Tortilla Soup', 'Healthy Chicken Pot Pie Soup', 'Flourless Peanut Butter Oatmeal Chocolate Chip Cookies', 'Vegan White Bean & Roasted Butternut Squash Soup']

# recipes tried:
#   Slow Cooker Chicken Tortilla Soup
#   Healthy Chicken Pot Pie Soup
#   Flourless Peanut Butter Oatmeal Chocolate Chip Cookies
#   Vegan White Bean & Roasted Butternut Squash Soup


# Get initial page HTML
def get_html (url):
    result = requests.get(url).text
    page = BeautifulSoup(result, "html.parser")
    return page

# Find recipe and navigate
def find_recipe (url, recipe):
    page = get_html(url)
    recipe_search = page.find("a", href=True, text=recipe)
    next_url = recipe_search['href']
    return next_url     
        

# Open page and pull recipe info
def get_recipe (url, recipe):
    next_url = find_recipe(url, recipe)
    try:
        recipe_page = BeautifulSoup(requests.get(next_url).text, "html.parser")
    except:
        new_site = ''
        if site[-1] == '/':
            new_site = site.strip('/')
        full_url = new_site + next_url
        recipe_page = BeautifulSoup(requests.get(full_url).text, "html.parser")
    
    recipe = recipe_page.find("script", type="application/ld+json")
    json_info = json.loads(recipe.contents[0])
    return json_info


# Print recipe info to console
def show_recipe(url, recipe):
    json_info = get_recipe(url, recipe)
    try:
        print('Recipe Name: ' + json_info['name'])
        print("\nIngredients:\n")
        for ing in json_info['recipeIngredient']:
            print (ing)
        print("\nInstructions:\n")
        try:
            for ins in json_info['recipeInstructions']:
                print(ins['text'])
        except:
            for ins in json_info['HowToStep']:
                print(ins['text'])
    except:
        #list of dicts in json info
        to_search = json_info['@graph'] 

        #grab right dict and make new dict
        recipe_dict = {}
        for item in to_search:
            if item['@type'] == 'Recipe':
                recipe_dict = item

        # Print recipe info to console
        print('Recipe Name: ' + recipe_dict['name'])
        print("\nIngredients:\n")
        for ing in recipe_dict['recipeIngredient']:
            print (ing)
        print("\nInstructions:\n")
        try:
            for ins in json_info['recipeInstructions']:
                print(ins['text'])
        except:
            for ins in json_info['HowToStep']:
                print(ins['text'])

# try all recipes
# for recipe in recipes:
#     show_recipe(site, recipe)

# call code with the currently filled in recipe
show_recipe(site, recipe)
