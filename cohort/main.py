## bokeh serve --show cohort
## crm 1
## ms 2
##invoice 3
##project 4
from os.path import dirname, join

import bokeh.plotting as bplt
from bokeh.plotting import Figure
from bokeh.models import ColumnDataSource, HoverTool, HBox, VBoxForm
from bokeh.models.widgets import Slider, Select, TextInput
from bokeh.models.ranges import Range1d,FactorRange
from bokeh.io import curdoc

from collections import OrderedDict

import numpy as np
import pandas as pd
from pandas import Series,DataFrame
from datetime import *
from dateutil import relativedelta

cohorts_1     = pd.read_pickle(join(dirname(__file__),'data', 'cohorts_1.pkl'))
cohorts_2    = pd.read_pickle(join(dirname(__file__),'data', 'cohorts_2.pkl'))
cohorts_3 = pd.read_pickle(join(dirname(__file__),'data', 'cohorts_3.pkl'))
cohorts_4 = pd.read_pickle(join(dirname(__file__),'data', 'cohorts_4.pkl'))

def add_pname(df,product):
	df['pname'] = product
	df.set_index('pname',append=True,inplace=True)
	df = df.swaplevel(0,1)
	return df

cohorts_1     = add_pname(cohorts_1.copy(),'product 1')
cohorts_2      = add_pname(cohorts_2.copy(),'product 2')
cohorts_3 = add_pname(cohorts_3.copy(),'product 3')
cohorts_4 = add_pname(cohorts_4.copy(),'product 4')

cohort_dfs = [cohorts_1,cohorts_2,cohorts_3,cohorts_4]

cohorts = pd.concat(cohort_dfs)


b_cohorts = DataFrame(cohorts.stack())
b_cohorts.reset_index(inplace=True)

b_cohorts['percents'] = b_cohorts[0]
del b_cohorts[0]
b_cohorts = b_cohorts[b_cohorts['percents']!=0]

b_cohorts['colors'] = b_cohorts['percents'].apply(lambda x: (255 - max(int(255*(x-50)/50),0),min(int((x*255)/50),255),0))
b_cohorts['epoch'] = pd.DatetimeIndex(b_cohorts['y_m']).astype(np.int64)
b_cohorts['epoch'] = b_cohorts['y_m'].astype('string')
b_cohorts['colors'] = b_cohorts['colors'].apply(lambda x:('#%02x%02x%02x' % x).upper())

mons = list(b_cohorts['epoch'].unique())

products = ['product 1','product 2','product 3','product 4']

counts = Slider(title="months since initial order", value=36, start=1, end=36, step=1)
start_mon = Select(title="start month", value='2012-01-01',options=list(mons))
end_mon = Select(title="end month", value='2014-12-01',options=list(mons))
product = Select(title='Product',value='product 1',options=list(products))

df_now = b_cohorts.copy()
source = ColumnDataSource(data=b_cohorts[b_cohorts['pname']=='product 1'])



p = Figure(plot_width = 1000, plot_height = 800,x_axis_location="below",
            y_axis_label='cohort',
            x_axis_label='months Since Initial Order',
            y_range= list(df_now.epoch.unique())[::-1],
            x_range=[0.5,36.5],
            tools="pan,resize,box_zoom,hover,save,wheel_zoom,reset",)

hover = p.select(dict(type=HoverTool))
hover.tooltips = OrderedDict([
    ('initial purchare', '@epoch'),
    ('months after IP', '@counts'),
    ('percentage', '@percents%'),
])

# customize plot
p.grid.grid_line_color = None
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.major_label_text_font_size = "10pt"
p.axis.major_label_standoff = 0
p.xaxis.major_label_orientation = np.pi/3

p.rect('counts','epoch',1,1,source=source,color='colors',alpha='percents',line_color=None)

def get_cohorts_now():
    c = counts.value
    sm = start_mon.value
    em = end_mon.value
    r = relativedelta.relativedelta(pd.to_datetime(em),pd.to_datetime(sm))
    nmons = r.years*12+r.months+1
    c = min(c,nmons)
    pro = product.value
    #cohorts_now = b_cohorts[b_cohorts['y_m'].isin(pd.date_range(sm,em,freq='MS'))]
    cohorts_now = b_cohorts[b_cohorts['pname']==pro]
    #cohorts_now = cohorts_now[cohorts_now['counts'].isin(range(1,c))]
    cn = pd.DataFrame()
    for mon in pd.date_range(sm,em,freq='MS'):
        temp = cohorts_now[(cohorts_now['y_m']==mon) & (cohorts_now['counts'].isin(range(1,c+1)))]
        cn = cn.append(temp)
        c-=1
    cohorts_now = cn.copy()
    cohorts_now.reset_index(inplace=True)
    #p.set(x_range=Range1d(0.5,c+0.5))
    #print(c)
    #mons = list(cohorts_now.epoch.unique())[0]
    #p.y_range = FactorRange(mons[::-1])
    #print(len(cohorts_now))
    return cohorts_now


def update(attrname, old, new):
    df_now = get_cohorts_now()
    source.data = df_now.to_dict('list')


controls = [product,counts,start_mon,end_mon]
for control in controls:
    control.on_change('value',update)

inputs = HBox(VBoxForm(*controls), width=300)

update(None, None, None) # initial load of the data

curdoc().add_root(HBox(inputs, p, width=1100))