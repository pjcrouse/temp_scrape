from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, DatetimeTickFormatter
from bokeh.plotting import figure
import requests
from datetime import datetime
from math import radians
from pytz import timezone

#create web scraping function
wund_api_key = 'your_wunderground_api_key_goes_here'
def get_data():
    url = 'http://api.wunderground.com/api/'+wund_api_key+'/geolookup/conditions/q/MA/Groton.json'
    r = requests.get(url)
    return r.json()['current_observation']['temp_f'] 

#create figure
f=figure(title='Temp in Groton MA as scraped from Wunderground', 
         x_axis_type='datetime', plot_width=500, plot_height=500)
f.yaxis.axis_label = "Temp - F"

#create columndatasource
source=ColumnDataSource(dict(x=[], y=[]))

#create glyphs
f.circle(x='x', y='y', color='blue', line_color='red',size=10,source=source)
f.line(x='x', y='y', source=source)

#create periodic function
def update():
    new_data=dict(x=[datetime.now(tz=timezone('America/New_York'))],y=[get_data()])
    source.stream(new_data,rollover=200)
    print(source.data)

date_str = '%m/%d/%y %H:%M:%S'    
f.xaxis.formatter=DatetimeTickFormatter(formats=dict(
        seconds=[date_str],
        minsec=[date_str],
        minutes=[date_str],
        hourmin=[date_str],
        hours=[date_str],
        years=[date_str],
        days=[date_str],
        months=[date_str]
        ))

f.xaxis.major_label_orientation=radians(60)

#cretae curdoc and configure callback
curdoc().add_root(f)    
curdoc().add_periodic_callback(update, 30000)