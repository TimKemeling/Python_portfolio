# python portfolio projects

These projects were made to showcase some of my python skills.
All of these projects were made with Python 3.9 and some of its libraries. 
I will note down all main libraries (and their version) with each project.

## Table of contents
[Recipe Pull](#recipe-pull)
[Stock Pull](#stock-pull)
[Coin Pull](#coin-pull)


### Recipe Pull

One of the things I like doing in my free time is cooking. The thing is, many recipes on the internet come with a long story that I
normally don't feel like reading. This is why I set out to make this program. The aim was to take a website and a recipe and have the 
program return a recipe to me without the stories. I quickly found out this was a slightly harder challenge than I thought it would be.
Eventually I got the program to work, albeit not how I initially thought it would.

The program runs only on certain websites and on recent recipes due to only using a basic HTML parsing library and not a browser shell.
I am leaving the program as is for now. I may later revise it to use a more advanced form of webscraping.

#### Libraries used
    * Beautiful soup 4.11.1
    * Requests 2.28.2
    * json

#### General working

The program is initialised from the command line with a recipe and website filled in the code. It takes those values and adds them together to create a URL that will contain the recipe.
It then opens that URL with the requests Library and pulls the HTML from the page. Once the HTML is read Beautiful soup finds the part of the page
that contains the recipe*. At this point it parses the recipe and makes it legible using the JSON library. After a little formatting the program
prints the ingredients and the instructions to the console.

*To make recipes visible on google most webpages use a very similar format.

##### Console snapshot
[recipe_pull](./recipe_pull_screenshot.png)


### Stock Pull

This project was a job posting I found on Upwork. I didn't apply for the job, but it seemed like a good practise project.
The posting asked to scrape the top 10 trending stocks from a website called stockwits.com and return the data to them.
The data didn't need to be cleaned according to the job post, it just needed to be sent trough. I decided to export the data
to a csv file with date and time stamp so it would be easy to import somewhere else.

This program was a little fickle and didn't always return the info, but after putting in a 2 second sleep, the program runs faster 
and does not show any problems after running it a few times.

#### Libraries used
    * Selenium 4.7.2
    * Pandas 1.5.2
    * Datetime

#### General working

Selenium opens a webdriver and navigates to the webpage, at which point the program sleeps for 2 seconds to let the page load.
After the 2 seconds pass the webdriver finds each cell and puts the data from each cell in a list. Python then loops trough this list
and separates the different stocks from each other. This data is then put into a python dictionary with the correct headings 
for each piece of data. Pandas pulls this into a dataframe, and converts it into a csv file with a date and time from the Datetime library.

##### Stock pull output
[Stock_Pull_csv](./stocks-15-03_13-06.csv)


### Coin Pull

The Coin Pull project was something I came up with after doing a project on a stock website. I wanted to use a page with a larger dataset and landed on coinmarketcap.com. Through Covid I became interested in the crypto markets and this seemed like a fun project to try my newfound skills on.

There was a number of challenges I encountered in this project. Like the stocks project, coinmarketcap uses a dynamic table that updates every 
few seconds or so. This proved to be a bit tricky to start with and next to that there was also a lot more data to work with. 
I initially tried to pull the data from each row of the table separately but that proved to be a bit tricky and very slow. 
After a little research I found out about pandas' .read_HTML function. This function takes HTML code and pulls all tables that are in there 
and saves them. This is what I used to get most of the data in the final product. 

However, the table has a few columns that have multiple
datapoints in them. These datapoints did not translate well into the dataframe in pandas, so I had to scrape those few columns separately. 
This made the program a little slower than I would like. 


#### Libraries used
    * Selenium 4.7.2
    * Pandas 1.5.2
    * Datetime

#### General working

selenium opens a webdriver and navigates to the page. Once the page is opened it scrolls down to the bottom to expose and load the whole table.
once the whole table is loaded, a number of functions run to scrape the columns that did not look right and to note the color of some of the numbers to be later converted into positive or negative values. Pfter this pandas pulls the table from the HTML code.

With the scraped data and table the program then formats all the columns to have the data separated where needed, or replaced by separately scraped data entirely after which the whole dataframe got exported to a csv file with date and time stamp.

##### Coin Pull Output
[Coin_pull_csv](coinprices-15-03_12-56.csv)