import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

cities = ('Chicago', 'New York City', 'Washington')
months = ('January', 'February', 'March', 'April', 'May', 'June')
week = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')

print('-'*40)
print('Hello! Let\'s explore some US bikeshare data!')
print('-'*40)

# get user input for city (Chicago, New York City, Washington). HINT: Use a while loop to handle invalid inputs
def get_filters():
    global city, month, day #needed in other function load_data(). Alternative coding should be done.

    # start request for user input for city:
    while True:
        city = input('Please enter the city name for which you want to see data: Chicago, New York City or Washington.\n').title()
        if city in cities:
            break
        else:
            print(">>>> That\'s not a valid city name. Please try again.")

    # start request for filter only by month, only by day, by both or for all data (in this order):
    while True:
        user_input = input("\nDo you want to filter the data by month, day, both or not at all? Type 'none' if you don\'t want a filter:\n" ).lower()

        # if user wants a filter only by month:
        if user_input == 'month':
            day = 'all'
            while True:
                month = input('\nWhich month? January, February, March, April, May or June:\n').title()
                if month in months:
                    break
                else:
                    print("\n>>>> That\'s not a valid month. Please try again.")
            break

        # if user wants a filter only by day:
        elif user_input == 'day':
            month = 'all'
            while True:
                day = input('\nWhich day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday:\n').title()
                if day in week:
                    break
                else:
                    print("\n>>>> That\'s not a valid day. Please try again.")
            break

        # if user wants a filter by month and day. First, the request for month input starts, if successful, request for day input starts:
        elif user_input == 'both':
            while True:
                month = input('\nWhich month? January, February, March, April, May or June:\n').title()
                if month in months:
                #if month input is existing, request for day input starts:
                    day = input('\nWhich day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday:\n').title()
                    if day in week:
                        break
                    #if user's day input doesn't exists:
                    else:
                        print("\n>>>> That\'s not a valid day. Please restart the selection.")
                #if user's month input doesn't exists:
                else:
                    print("\n>>>> That\'s not a valid month. Please try again.")
            break

        # if user wants all data (all months and all days):
        elif user_input == 'none':
            month = 'all'
            day = 'all'
            break

        # if user did an input different than month, day, both, none:
        else:
            print("\n>>>> That\'s not a valid entry. Please try again.")
    print('-'*40)

    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel, depending on the input selection from users:

    if user selected only month: display statistics for most common day and hour
    if user selected only day: display statistics for most common hour
    if user selected both month and day: display statistics for most common hour
    if user selected all: display statistics for most common month, day and hour

    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month, corresponding count and percentage:
    if month == 'all':
        most_common_month = df['month'].mode()[0]
        most_common_month_count = df['month'].value_counts()[most_common_month]
        most_common_month_pct = (most_common_month_count / len(df) * 100).round(2)
        print('Most common month: {} ---- Count: {} ({}%)'.format(most_common_month, most_common_month_count, most_common_month_pct))

    # display the most common day of week, corresponding count and percentage:
    if day == 'all':
        most_common_day = df['day_of_week'].mode()[0]
        most_common_day_count = df['day_of_week'].value_counts()[most_common_day]
        most_common_day_pct = (most_common_day_count / len(df) * 100).round(2)
        print('Most common day: {} ---- Count: {} ({}%)'.format(most_common_day, most_common_day_count, most_common_day_pct))

    # display the most common start hour, corresponding count and percentage:
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    most_common_hour_count = df['hour'].value_counts()[most_common_hour]
    most_common_hour_pct = (most_common_hour_count / len(df) * 100).round(2)
    print('Most common hour: {} ---- Count: {} ({}%)'.format(most_common_hour, most_common_hour_count, most_common_hour_pct))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station, corresponding count and percentage:
    popular_start_station = df['Start Station'].mode()[0]
    popular_start_station_count = df['Start Station'].value_counts()[popular_start_station]
    popular_start_station_pct = (popular_start_station_count / len(df) * 100).round(2)
    print('Most popular start station: {} ---- Count: {} ({}%)'.format(popular_start_station, popular_start_station_count, popular_start_station_pct))

    # display most commonly used end station, corresponding count and percentage:
    popular_end_station = df['End Station'].mode()[0]
    popular_end_station_count = df['End Station'].value_counts()[popular_end_station]
    popular_end_station_pct = (popular_end_station_count / len(df) * 100).round(2)
    print('Most popular end station: {} ---- Count: {} ({}%)'.format(popular_end_station, popular_end_station_count, popular_end_station_pct))

    # display most frequent combination of start station and end station trip and corresponding count:
    popular_combination = (df['Start Station']+' to '+df['End Station']).mode()[0]
    popular_combination_count = (df['Start Station']+' to '+df['End Station']).value_counts()[popular_combination]
    popular_combination_pct = (popular_combination_count / len(df) * 100).round(2)
    print('Most popular trip: {} ---- Count: {} ({}%)'.format(popular_combination, popular_combination_count, popular_combination_pct))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time in minutes (not seconds) and count of trips:
    total_travel_time = df['Trip Duration'].sum() // 60
    total_travel_count = len(df)
    print('Total trip duration in min: {} ---- Count trips: {}'.format(total_travel_time, total_travel_count))

    # display mean travel time in minutes (not seconds):
    mean_travel_time = df['Trip Duration'].mean() / 60
    print('Average trip duration in min:', round(mean_travel_time,2))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types and separate count of NaN:
    user_type = df['User Type'].value_counts()
    count_NaN_type = df['User Type'].isnull().sum()
    print('Count of user type:\n', user_type)
    print('Missing user type information in {} case(s).'.format(count_NaN_type))

    # Display percentage allocation of user types (incl. NaN):
    user_type_pct = df['User Type'].value_counts(normalize=True, dropna = False).multiply(100).round(2)
    print('\nPercentage allocation of user type (%):\n', user_type_pct)

    # Display counts of gender and separate count of NaN:
    if 'Gender' not in df:
        print('\nNo gender information available for {}.'.format(city))
    else:
        gender_count = df['Gender'].value_counts()
        count_NaN_Gender = df['Gender'].isnull().sum()
        print('\nCount of gender: \n',gender_count)
        print('Missing gender information in {} case(s).'.format(count_NaN_Gender))

        # Display percentage allocation of gender (incl. NaN):
        gender_pct = df['Gender'].value_counts(normalize=True, dropna = False).multiply(100).round(2)
        print('\nPercentage allocation of gender (%):\n', gender_pct)

    # Display earliest, most recent, most common year of birth and NaN (count and percentage):
    if 'Birth Year' not in df:
        print('No year of birth information available for {}.'.format(city))
    else:
        earliest_year_birth = int(df['Birth Year'].min())
        most_recent_year_birth = int(df['Birth Year'].max())
        most_common_year_birth = int(df['Birth Year'].mode()[0])
        most_common_year_birth_pct = ((df['Birth Year'].value_counts()[most_common_year_birth]) / len(df) * 100).round(2)
        count_NaN_year = df['Birth Year'].isnull().sum()

        print('\nEarliest year of birth:', earliest_year_birth)
        print('Most recent year of birth:', most_recent_year_birth)
        print('Most common year of birth: {} ({}%)'.format(most_common_year_birth, most_common_year_birth_pct))
        print('Missing birth year information in {} case(s) ({}%).'.format(count_NaN_year, (count_NaN_year / len(df) * 100).round(2)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """Displays a random sample of 10 rows of raw data."""

    print('\nSample of raw data...\n')
    print(df.sample(10))
    while True:
        # Display 5 new rows if user types 'yes'. Display stops if user types 'no'.
        more_data = (input('\nDo you want to see more raw data? Enter yes or no.\n')).lower()
        if more_data == 'yes':
            print(df.sample(10))
        elif more_data == 'no':
            break
        else:
            print('That\'s not a valid entry.')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        print('-'*40)
        print('End of selection city: {} - month: {} - day: {}'.format(city, month, day))
        print('-'*40)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
