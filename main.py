# -*- coding: utf-8 -*-
import os

import pandas as pd
import matplotlib.pyplot as plt

# define and initialize dataset files path
usa_cities_demographics_filepath = 'datasets/usa_cities_demographics.csv'
global_land_temperature_filepath = 'datasets/global_land_temperatures_city.csv'

# store the generated figures in below mention directory
figures_dir = 'figures'

# Check if `figures` directory does not exist then create it.
if not os.path.exists(figures_dir):
    os.mkdir(figures_dir)


# =============================================================================
# This function read the csv file using pandas and return the dataframe object
# if file exists, otherwise it will raise `FileNotFoundError` error
# =============================================================================
def get_csv_dataframe(filepath, delimiter):
    """
    This function will check if the target file does not exist, then it will
    raise `FileNotFoundError`. If file exists, it will read the CSV file and 
    return dataframe for target csv file.
    :param delimiter: it is used as separator for while text based data from 
        a file like csv/text.
    :param filepath: file path where it is located in memory.
    :return: return the dataframe object for target csv file.
    """
    # Make sure if the file path does not exist, then it will
    # throw error `FileNotFoundError`
    if not os.path.exists(filepath):
        raise FileNotFoundError

    # read csv file using pandas and return the pandas dataframe object
    return pd.read_csv(filepath, delimiter=delimiter, encoding='utf8')

# =============================================================================
# Visualisation 1: By using Line Plot Show the Average Temperature
# =============================================================================


def show_avg_temperature_line_plot():
    """
    This function reads the data from dataset 
    "global_land_temperatures_city.csv", extract the temperature data for the
    United States of America and filtered records for specific U.S. cities 
    (New York, Los Angeles, San Francisco, Miami, Chicago, Las Vegas) and 
    filtered dataset for year 2012. This function clean the dataset by 
    removing the records with missing values. Then sort the dataframe by 
    `Date` column.  After data extraction, transformation and cleaning this
    function show the Average Temperature comparison between the specific 
    U.S. cities (listed below) for year 2012 using the Line Plot. This 
    function will also store the plot figure/image in the specified directory
    `figures`.
    :return: None
    """

    # call function get_csv_dataframe()
    df_temp = get_csv_dataframe(
        global_land_temperature_filepath, delimiter=',')

    cities = [
        "New York",
        "Los Angeles",
        "San Francisco",
        "Miami",
        "Chicago",
        "Las Vegas",
    ]

    # Extract temperature data for the United States
    df_usa_temp = df_temp[df_temp["Country"] == "United States"]

    # Filter temperature data for specific cities only
    df_usa_temp = df_usa_temp[df_usa_temp.City.isin(cities)]

    # Clean dataset remove entries with missing values
    df_usa_temp = df_usa_temp.dropna()

    # Add new column `Date` for storing dates from `dt` column.
    # Convert `dt` column that contains string dates to pandas datetime
    df_usa_temp['Date'] = pd.to_datetime(df_usa_temp['dt'])

    # extract year from date column named `dt`
    df_usa_temp['Year'] = df_usa_temp['Date'].dt.year

    # keep records for year 2012 only.
    df_usa_temp = df_usa_temp[df_usa_temp['Year'] == 2012]

    # Sort dataframe records by date
    df_usa_temp = df_usa_temp.sort_values(by='Date')

    # create new figure with and set size width is 10, height is 7 inches.
    # The `dpi` parameter shows dots per inch or resolution for the figure
    plt.figure(figsize=(10, 7), dpi=144)

    # make new dataframes for specific cities listed above
    new_york_df = df_usa_temp[df_usa_temp['City'] == 'New York']
    los_angeles_df = df_usa_temp[(df_usa_temp['City'] == 'Los Angeles')]
    san_francisco = df_usa_temp[(df_usa_temp['City'] == 'San Francisco')]
    miami_df = df_usa_temp[(df_usa_temp['City'] == 'Miami')]
    las_vegas_df = df_usa_temp[(df_usa_temp['City'] == 'Las Vegas')]

    # Draw plot for showing New York average temperature for year 2012
    plt.plot(new_york_df['Date'], new_york_df['AverageTemperature'],
             linestyle='-',
             marker='o',
             markersize=4,
             label="New York",
             alpha=0.7)

    # Draw plot for showing Los Angeles average temperature for year 2012
    plt.plot(los_angeles_df['Date'], los_angeles_df['AverageTemperature'],
             linestyle='-',
             marker='o',
             markersize=4,
             label="Los Angeles",
             alpha=0.7)

    # Draw plot for showing San Francisco average temperature for year 2012
    plt.plot(san_francisco['Date'], san_francisco['AverageTemperature'],
             linestyle='-',
             marker='o',
             markersize=4,
             label="San Francisco",
             alpha=0.7)

    # Draw plot for showing Miami average temperature for year 2012
    plt.plot(miami_df['Date'], miami_df['AverageTemperature'],
             linestyle='-',
             marker='o',
             markersize=4,
             label="Miami",
             alpha=0.7)

    # Draw plot for showing Las Vegas average temperature for year 2012
    plt.plot(las_vegas_df['Date'], las_vegas_df['AverageTemperature'],
             linestyle='-',
             marker='o',
             markersize=4,
             label="Las Vegas",
             alpha=0.7)

    # plot title
    title = 'Average Temperature Comparison of USA Cities for Year 2012'

    # Set plot title
    plt.title(title)

    # set xlabel value for x-axis
    plt.xlabel('Date (yyyy-mm)')

    # set ylabel value for x-axis
    plt.ylabel(f'Average Temperature (°C)')

    # plot legend and set its location to Upper Right Corner
    plt.legend(loc='upper right')

    # Save the plot image to specified path
    plt.savefig(f"{figures_dir}/{title.replace(' ', '_')}")

    # show the plot
    plt.show()


# =============================================================================
# Visualisation 2: By using Histogram Plot Show Population Percentage
# =============================================================================

def show_population_histogram_plot():
    """
    This function draw histogram plot and in which show the population
    percentage (%) of top 7 USA States with highest population. Firstly, 
    extract the data from dataset "usa_cities_demographics.csv". Clean the 
    dataset and remove the rows having missing values. Then remove the 
    duplicate records based on columns `City` and `State`. Calculate the sum
    of total population by apply `groupby` function on column `State`. Then 
    Calculate percentage for each state population over total population. 
    After reading, cleaning and transform the data, then this function draw 
    the histogram plot and show top 7 USA states population with percentage 
    in histogram plot and we can analyze the different state population 
    conveniently.
    :return: None
    """
    # get dataframe object by calling the function get_csv_dataframe
    usa_cities_demographics_df = get_csv_dataframe(
        usa_cities_demographics_filepath, delimiter=";")

    # Clean dataset for removing the records with missing values
    usa_cities_demographics_df = usa_cities_demographics_df.dropna()

    # Drop duplicates based on columns `city` and `state` combinations
    usa_cities_demographics_df = \
        usa_cities_demographics_df.drop_duplicates(subset=['City', 'State'])

    # calculate the total population for each USA state.
    usa_states_population_df = usa_cities_demographics_df.groupby('State')[
        'Total Population'].sum()

    # sort the states based on total population
    sorted_population_df = usa_states_population_df.sort_values(
        ascending=False)

    # extract the first/top 7 state names from `sorted_population_df`
    selected_state_names = list(sorted_population_df.keys())[:7]

    # extract the first/top 7 states population from `sorted_population_df`
    selected_states_population = sorted_population_df.values.tolist()[:7]

    # calculate the sum population of all of USA states
    total_pop = usa_cities_demographics_df['Total Population'].sum()

    # Calculate each state population percentage and store in list
    state_pop_percentages = [round((state_pop / total_pop) * 100, 2)
                             for state_pop in selected_states_population]

    # create new figure with and set size width is 10, height is 7 inches.
    # The `dpi` parameter shows dots per inch or resolution for the figure
    plt.figure(figsize=(8, 6), dpi=144)

    # draw histogram plot and set appropriate parameters
    n, bins, patches = plt.hist(selected_state_names,
                                bins=len(selected_state_names),
                                weights=state_pop_percentages,
                                edgecolor='black')

    # Show population percentage for each state in its corresponding bin.
    # Calculate the relative frequency's (%) for each bin
    bin_widths = [bins[i + 1] - bins[i] for i in range(len(bins) - 1)]

    # Set the y-axis limits based on the maximum percentage(%)
    max_percentage = max(state_pop_percentages)

    # Add buffer for the y-axis
    plt.ylim(0, max_percentage + 5)

    # Iterate over the range for add percentage labels to the bins
    for i in range(len(patches)):
        # calculate width of the corresponding bin/bar
        width = patches[i].get_x() + patches[i].get_width() / 2

        # calculate height of the corresponding bin/bar
        height = patches[i].get_height()

        # set the total percentage value of a state to its corresponding bin
        plt.annotate("{}%".format(
            state_pop_percentages[i]),
            (width, height),
            ha='center',
            va='bottom')

    # define the title of plot
    title = "USA Top 7 States with Highest Population"

    # set the plot title
    plt.title(title)

    # set xlabel for x-axis
    plt.xlabel("U.S.A. States")

    # set ylabel for y-axis
    plt.ylabel("Population Percentage(%)")

    # set plot legend
    plt.legend()

    # save the plot image to specified path `figures`
    plt.savefig(f"{figures_dir}/{title.replace(' ', '_')}")

    # show the plot
    plt.show()


# =============================================================================
# Visualisation 3: By using Bar Plot Show Gender Distribution Analysis
# =============================================================================
def gender_distribution_bar_plot():
    """
    This function shows the gender distribution for the top 7 USA cities that 
    are most populated. First, this function read the dataset csv file using 
    pandas, then drop duplicates based on columns `City` and `State`. Clean 
    the dataset, then convert the population to millions based on gender. 
    Sort the dataset based on `Total Population`. Then extract top 20 highest
    population cities names, their total population of male & female. After 
    data extraction and transformation, draw the bar plot and show the gender 
    distribution analysis using bar plot.
    :return: None
    """
    # get dataframe object by calling the function get_csv_dataframe(..).
    usa_cities_demographics_df = get_csv_dataframe(
        usa_cities_demographics_filepath, delimiter=";")

    # Drop duplicate city/state combinations
    usa_cities_demographics_df = \
        usa_cities_demographics_df.drop_duplicates(subset=['City', 'State'])

    # convert male population to millions
    usa_cities_demographics_df['Male Population'] = \
        round(usa_cities_demographics_df['Male Population'] / 1000000, 2)

    # convert female population to millions
    usa_cities_demographics_df['Female Population'] = \
        round(usa_cities_demographics_df['Female Population'] / 1000000, 2)

    # sort dataframe records based on total population
    sorted_population_df = usa_cities_demographics_df.sort_values(
        'Total Population', ascending=False)

    # extract first/top 20 city names
    top_cities_names = sorted_population_df['City'].values.tolist()[:20]

    # extract first/top 20 cities male population
    top_cities_male_pop = \
        sorted_population_df['Male Population'].values.tolist()[:20]

    # extract first/top 20 cities female population
    top_cities_female_pop = \
        sorted_population_df['Female Population'].values.tolist()[:20]

    # create new figure with and set size width is 10 & height is 7 inches.
    # The `dpi` parameter shows dots per inch or resolution for the figure
    plt.figure(figsize=(8, 7), dpi=144)

    # draw the bar plot and show male population and set color, width and
    # alpha attribute values
    plt.bar(top_cities_names, top_cities_male_pop,
            color='blue', width=0.5, alpha=0.7)

    # draw the bar plot to show female population and set color, width
    # and alpha attribute values
    plt.bar(top_cities_names, top_cities_female_pop,
            color='green', width=0.5, alpha=0.5)

    # define tile for plot
    title = "Gender Distribution Analysis For Top 20 Most Populated Cities"

    # set plot title
    plt.title(title)

    # use xticks function and set rotation angle value to 25.
    # It will rotate the x-axis labels to 25 angle.
    plt.xticks(rotation=25)

    # set xlabel for x-axis
    plt.xlabel("Cities (U.S.A)")

    # set xlabel for y-axis
    plt.ylabel("Population (Millions)")

    # set the plot legend and set loc parameter to Upper Right
    plt.legend(labels=['Male', 'Female'], loc='upper right')

    # Save the plot image to `figures` directory/
    plt.savefig(f"{figures_dir}/{title.replace(' ', '_')}")

    # show the plot
    plt.show()


"""
__main__: It is the entry point in python script.
"""
if __name__ == "__main__":
    # call the function show_avg_temperature_with_line_plot(), it will show
    # average temperature for USA states
    show_avg_temperature_line_plot()

    # call function show_population_histogram_plot(), it will show USA
    # states population with hist plot
    show_population_histogram_plot()

    # call function show_avg_temperature_line_plot(), it will show
    # gender distribution using bar plot
    gender_distribution_bar_plot()
