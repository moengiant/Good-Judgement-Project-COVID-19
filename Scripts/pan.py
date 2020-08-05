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
country = 'US'

# This is the GitHub URL for the Johns Hopkins data in CSV format
data_loc = ('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/'
           'csse_covid_19_data/csse_covid_19_time_series'
           '/time_series_covid19_confirmed_global.csv')

# Read in the data to a pandas DataFrame.
if not READ_FROM_URL:
    data_loc = LOCAL_CSV_FILE
df = pd.read_csv(data_loc)

# Group by country and sum over the different states/regions of each country.
grouped = df.groupby('Country/Region')
df2 = grouped.sum()

def make_plot(country):
    """Make the bar plot of case numbers and change in numbers line plot."""

    # Extract the Series corresponding to the case numbers for country.
    c_df = df2.loc[country, df2.columns[3:]]
    # Discard any columns with fewer than MIN_CASES.
    c_df = c_df[c_df >= MIN_CASES].astype(int)
    # Convet index to a proper datetime object
    c_df.index = pd.to_datetime(c_df.index)
    n = len(c_df)
    if n == 0:
        print('Too few data to plot: minimum number of cases is {}'
                .format(MIN_CASES))
        sys.exit(1)

    fig = plt.Figure()

    # Arrange the subplots on a grid: the top plot (case number change) is
    # one quarter the height of the bar chart (total confirmed case numbers).
    ax2 = plt.subplot2grid((10,100), (0,3), rowspan=4, colspan=95)
    ax1 = plt.subplot2grid((10,100), (4,3), rowspan=4, colspan=95)
    ax1.plot(range(n), c_df.values, '.k')

    ysmoothed = gaussian_filter1d(c_df.values, sigma=3)
    ax1.plot(range(n),ysmoothed,color='red')
        
    # Force the x-axis to be in integers (whole number of days) in case
    # Matplotlib chooses some non-integral number of days to label).
    ax1.xaxis.set_major_locator(MaxNLocator(integer=True))

    c_df_change = c_df.diff()
    
    ax2.bar(range(n), c_df_change.values)
    y2smoothed = gaussian_filter1d(c_df_change.values, sigma=3)
    ax2.plot(range(n),y2smoothed,color='red')

    
    firstDate =  min(c_df.index)
    lastDate = max(c_df.index)

    maxDate = c_df_change.idxmax(axis = 0)
    unique_index = pd.Index(list(c_df_change.index))
    high_spot = unique_index.get_loc(maxDate)
    end_spot = unique_index.get_loc(lastDate)
    
    print(str(maxDate) + ' : ' + str(c_df_change.get(key=maxDate)))
    print(str(lastDate) + ' : ' + str(c_df_change.get(key=lastDate)))
    swing_down = (c_df_change.get(key=maxDate) - c_df_change.get(key=lastDate)) 
       
 
    days = maxDate - firstDate
    dayIndex = days.days
    #print(dayIndex)
    slopeV = (c_df_change.get(key=lastDate)-c_df_change.get(key=maxDate))/(n - dayIndex)
    print(slopeV)

    diffChange = c_df_change.get(key=lastDate) - c_df_change.get(key=maxDate)
    
    perChange = (diffChange/c_df_change.get(key=maxDate))*100
    maxVal = c_df_change.max()
    #print(maxVal)
    
    if maxDate < lastDate: 
        ax2.annotate('Number of New Cases in Decline\n' + 'Decreance in new Cases: ' + str(round(swing_down,0)) + '\n' + 'Percentage decrease: ' + str(round(perChange,0)) + '% over ' + str((n - dayIndex)) + ' days\n' +
        'Larger negative number indicates better job in mitigation', color='green',
        xy=((dayIndex+n)/2, (c_df_change.get(key=lastDate)+c_df_change.get(key=maxDate))/2),
        xytext=(0,maxVal/2),
        arrowprops = dict(arrowstyle='-',facecolor='green', alpha=0.5),
        horizontalalignment='left', verticalalignment='center',
        fontsize=6,
        )
        
    
    ax2.annotate('Max number of new cases\n' + str(maxVal) + '\n', xy=(dayIndex, maxVal), xytext=(0, maxVal),
            arrowprops=dict(arrowstyle='-',facecolor='black'),
            horizontalalignment='left', verticalalignment='top',
            fontsize=6,
            )
    slope = ''
    ax2.set_xticks([])

    plt.figtext(.05, .05, 'Data provided by Johns Hopkins University Center for Systems Science and Engineering (JHU CSSE).\n' +
             ' Also, Supported by ESRI Living Atlas Team and the Johns Hopkins University Applied Physics Lab (JHU APL).\n' +
             ' Data files can be obtained at https://github.com/CSSEGISandData/COVID-19'   
        ,
        style='italic',
        fontsize=5,
        
        bbox={'facecolor':'white', 'edgecolor':'none','alpha': 0.5, 'pad': 10})
    

    ax1.set_xlabel('Days since {} case'.format(MIN_CASES))
    ax1.set_ylabel('Confirmed cases, $N$')
    ax2.set_ylabel('$\Delta N$')

    # Add a title reporting the latest number of cases available.
    title = '{}\n{} cases on {}'.format(country, c_df[-1],
                c_df.index[-1].strftime('%d %B %Y'))
    plt.suptitle(title)



make_plot(country)
plt.show()
make_plot('Spain')
plt.show()
make_plot('Italy')
plt.show()
