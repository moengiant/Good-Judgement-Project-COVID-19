import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline, BSpline
from scipy.ndimage.filters import gaussian_filter1d
from matplotlib.ticker import MaxNLocator

# If you have saved a local copy of the CSV file as LOCAL_CSV_FILE,
# set READ_FROM_URL to True
READ_FROM_URL = True
LOCAL_CSV_FILE = 'covid-19-cases.csv'

# Start the plot on the day when the number of confirmed cases reaches MIN_CASES.
MIN_CASES = 1

# The country to plot the data for.
state = 'Illinois'

# This is the GitHub URL for the Johns Hopkins data in CSV format
data_loc = ('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv')

# Read in the data to a pandas DataFrame.
if not READ_FROM_URL:
    data_loc = LOCAL_CSV_FILE
df = pd.read_csv(data_loc)

# Group by country and sum over the different states/regions of each country.
grouped = df.groupby('Province_State')
df2 = grouped.sum()

def make_plot(state):
    """Make the bar plot of case numbers and change in numbers line plot."""

    # Extract the Series corresponding to the case numbers for country.
    c_df = df2.loc[state, df2.columns[11:]]
    # Discard any columns with fewer than MIN_CASES.
    c_df = c_df[c_df >= MIN_CASES].astype(int)
    # Convet index to a proper datetime object
    c_df.index = pd.to_datetime(c_df.index)
    n = len(c_df)
    if n == 0:
        print('Too few data to plot: minimum number of deaths is {}'
                .format(MIN_CASES))
        sys.exit(1)

    fig = plt.Figure()

    # Arrange the subplots on a grid: the top plot (case number change) is
    # one quarter the height of the bar chart (total confirmed case numbers).
    ax2 = plt.subplot2grid((5,50), (0,3), rowspan=2, colspan=48)
    ax1 = plt.subplot2grid((5,50), (2,3), rowspan=3, colspan=48)
    ax1.plot(range(n), c_df.values, '.k')

    ysmoothed = gaussian_filter1d(c_df.values, sigma=2)
    ax1.plot(range(n),ysmoothed,color='red')
        
    # Force the x-axis to be in integers (whole number of days) in case
    # Matplotlib chooses some non-integral number of days to label).
    ax1.xaxis.set_major_locator(MaxNLocator(integer=True))

    c_df_change = c_df.diff()
    
    ax2.bar(range(n), c_df_change.values)
    ax2.set_xticks([])

    ax1.set_xlabel('Days since {} Death'.format(MIN_CASES))
    ax1.set_ylabel('Confirmed Deaths, $N$')
    ax2.set_ylabel('$\Delta N$')

    # Add a title reporting the latest number of cases available.
    title = '{}\n{} Deaths on {}'.format(state, c_df[-1],
                c_df.index[-1].strftime('%d %B %Y'))
    plt.suptitle(title)



make_plot(state)
plt.show()
make_plot('Florida')
plt.show()
make_plot('Louisiana')
plt.show()
