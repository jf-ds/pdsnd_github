# adding s line

import time
import pandas as pd
import numpy as np
import datetime


##### REFERENCE DICTIONARIES
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'newyorkcity': 'new_york_city.csv',
              'washington': 'washington.csv' }

city_abbrev = {'chi':'Chicago',
              'new':'New York City',
              'was':'Washington'}

month_abbrev = {'jan':'January',
             'feb':'February',
             'mar':'March',
             'apr':'April',
             'may':'May',
             'jun':'June',
             'all':'All'}

wkday_abbrev = {'sun':'Sunday',
                'mon':'Monday',
                'tue':'Tuesday',
                'wed':'Wednesday',
                'thu':'Thursday',
                'fri':'Friday',
                'sat':'Saturday',
                'all':'All'}

month_num = {'January':1,
             'February':2,
             'March':3,
             'April':4,
             'May':5,
             'June':6,
             'All':99}

wkday_num = {'Sunday':7,
             'Monday':1,
             'Tuesday':2,
             'Wednesday':3,
             'Thursday':4,
             'Friday':5,
             'Saturday':6,
             'All':99}

num_month = {1:'January',
             2:'February',
             3:'March',
             4:'April',
             5:'May',
             6:'June',
             99:'All'}

num_wkday = {1:'Monday',
             2:'Tuesday',
             3:'Wednesday',
             4:'Thursday',
             5:'Friday',
             6:'Saturday',
             7:'Sunday',
             99:'All'}

##### FUNCTION FOR REUSE
def most_common(item_type, city_com):
    """
    takes <item_type> as a STRING just for output
          <city_com> as the LIST of items, of which, we are looking for the most common
    returns nothing, prints out a statement identifying the most common item of <item_type>
    """
    com_dist = pd.DataFrame([[x,city_com.count(x)] for x in set(city_com)])
    com_dist.columns = ['com_name', 'com_ct']
    com_dist1 = com_dist.sort_values(by = ['com_ct'], ascending = False)
    mos_com = com_dist1.iloc[[0]]['com_name'].to_string().split(' ',1)[1]
    resultstring = 'The most common ' + item_type + ' is' + mos_com
    print(resultstring)

##### FUNCTION FOR REUSE
def most_common2(item_type, city_com):
"""
This was just added to make 1 refactoring change
"""
com_dist = pd.DataFrame([[x,city_com.count(x)] for x in set(city_com)])
com_dist.columns = ['com_name', 'com_ct']
com_dist1 = com_dist.sort_values(by = ['com_ct'], ascending = False)
mos_com = com_dist1.iloc[[0]]['com_name'].to_string().split(' ',1)[1]
resultstring = 'The most common ' + item_type + ' is' + mos_com
print(resultstring)

##### BODY FUNCTIONS
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or 'all' to apply no month filter
        (str) day - name of the day of week to filter by, or 'all' to apply no day filter
    """

    ##### Initializing variables
    city_choose = '_'
    city = '_'
    month_choose = '_'
    month = '_'
    wkday_choose = '_'
    wkday = '_'
    print('Hello! Let\'s explore some US bikeshare data!')

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while city_choose not in ['chi','new','was']:
        city_choose = str(input('\nWhich city would you like to explore? \nPlease enter:\n- Chicago \n- New York \n- Washington \n')).lower()[:3]
        # the LOWER method included close to the end of the prevous statement addresses variation in case of input
    city = city_abbrev[city_choose]
    print('\nYou chose ',city)

    # TO DO: get user input for month (all, january, february, ... , june)
    while month_abbrev.get(month_choose) == None:
        month_choose = str(input('\nWhich month would you like to explore? \n(Please type in a month from January - June or all)\n')).lower()[:3]
    month = month_abbrev[month_choose]
    print('You chose ',month)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while wkday_abbrev.get(wkday_choose) == None:
        wkday_choose = str(input('\nWhich day of week would you like to explore? \n(Please type in a day of week or all)\n')).lower()[:3]
    wkday = wkday_abbrev[wkday_choose]
    print('You chose ',wkday)

    print('-'*40)
    return city, month, wkday

def load_data(city, month, wkday):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    cityfile = pd.read_csv(CITY_DATA[city.lower()])
    print(city, 'file loaded')
    cityfile['col_month'] = pd.DatetimeIndex(cityfile['Start Time']).month
    cityfile['col_wkday'] = pd.DatetimeIndex(cityfile['Start Time']).weekday + 1
    # rem: originally for weekday
    #      0 = Monday
    #      6 = Sunday
    # with weekday + 1
    #      1 = Monday
    #      7 = Sunday
    see_file = str(input('Would you like to see a sample of the file?\n(Please type in Yes\nOtherwise, we will move along)\n'))
    if len(see_file) == 0:
        see_file = 'n'
    if see_file.lower()[0] == 'y':
        print(cityfile.head())
    if month != 'All':
        cityfile2 = cityfile[cityfile['col_month'] == month_num[month]]
    else:
        cityfile2 = cityfile
    if wkday != 'All':
        cityfile3 = cityfile2[cityfile2['col_wkday'] == wkday_num[wkday]]
    else:
        cityfile3 = cityfile2
    df = cityfile3

    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    Takes in dataframe <df>
    Returns nothing
    Prints statements on most common:
        month
        day of week
        hour of day
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['col_month'] = pd.DatetimeIndex(df['Start Time']).month
    df['col_wkday'] = pd.DatetimeIndex(df['Start Time']).weekday + 1
    df['col_hour'] = pd.DatetimeIndex(df['Start Time']).hour
    df.replace({'col_month':num_month}, inplace=True)
    df.replace({'col_wkday':num_wkday}, inplace=True)

    # TO DO: display the most common month
    citymonth = df['col_month'].tolist()
    if len(citymonth) == 0:
        print('Sorry, that month isn\'t in the data')
    else:
        most_common('month', citymonth)

    # TO DO: display the most common day of week
    citywkday = df['col_wkday'].tolist()
    if len(citywkday) == 0:
        print('Sorry, that day of the week isn\'t in the data')
    else:
        most_common('day of the week', citywkday)

    # TO DO: display the most common start hour
    cityhour = df['col_hour'].tolist()
    # this is a 24hr clock starting at 0 going to 23
    if len(cityhour) == 0:
        print('Sorry, time of day isn\'t in the data')
    else:
        most_common('start hour', cityhour)

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.
    Takes in dataframe <df>
    Returns nothing
    Prints statements on most common:
        Starting Station
        Ending Station
        Route
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    df['col_route'] = df['Start Station'] + ' --> ' + df['End Station']

    # Most common START STATION
    citystart = df['Start Station'].tolist()
    most_common('starting station', citystart)

    # Most common END STATION
    cityend = df['End Station'].tolist()
    most_common('ending station', cityend)

    # Most common ROUTE
    #citystart = df['col_route'].tolist()
    #most_common('route', citystart)
    #^^^ this was not used because this method took a long time (sometimes > 10mins) to run
    #the following method was MUCH faster
    cityroute = pd.DataFrame(df['col_route'])
    cityroute['it_ct'] = 1
    cityroute_group = pd.DataFrame(cityroute.groupby(['col_route'])['it_ct'].sum())
    ct_max = cityroute_group['it_ct'].max()
    top_route = cityroute_group[cityroute_group['it_ct'] == ct_max]
    top_route_1 = top_route.iloc[[0]]['it_ct'].to_string().split('\n')
    top_route_2 = ''.join(top_route_1[1:len(top_route_1)]).split(' ')
    top_route_3 = ' '.join(top_route_2[0:len(top_route_2)-1]).strip()
    print('The most common route is ',top_route_3)

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    Takes in dataframe <df>
    Returns nothing
    Prints statements on sum and average travel duration
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    trip_duration = df['Trip Duration']
    td_sum = (trip_duration.sum())/(60**2)
    td_mean = (trip_duration.mean())/60
    # TO DO: display total travel time
    print('The total travel time for this city is ','%.2f' % td_sum, 'hours')

    # TO DO: display mean travel time
    print('The average travel time per trip is ','%.2f' % td_mean, 'minutes')

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """
    Displays statistics on bikeshare users.
    Takes in dataframe <df>
    Returns nothing
    Prints frequency counts for:
        User type
        Gender (if available)
        Birth Year (if available)
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type = df['User Type'].tolist()
    com_dist = pd.DataFrame([[x,user_type.count(x)] for x in set(user_type)])
    com_dist.columns = ['User_Type', 'Count']

    # TO DO: Display counts of gender
    dflist = list(df)
    if 'Gender' in dflist:
        print('Gender data is available')
        user_type = df['Gender']
        user_type = user_type.dropna().tolist()
        com_dist = pd.DataFrame([[x,user_type.count(x)] for x in set(user_type)])
        com_dist.columns = ['Gender', 'Count']
        print(com_dist)
    else:
        print('Sorry, gender data is not available')


    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in dflist:
        print('\nBirth Year data is available')
        print('The earliest birth year is',int(df['Birth Year'].min()))
        print('The earliest birth year is',int(df['Birth Year'].max()))
        citybyear = df['Birth Year'].dropna().tolist()
        pd.options.display.float_format = '{:.0f}'.format
        most_common('birth year', citybyear)

    else:
        print('\nSorry, Birth Year data is not available')


    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, wkday = get_filters()
        df = load_data(city, month, wkday)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = str(input('\nWould you like to restart?\nPlease type in Yes\nOtherwise, we will end\n'))
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
