'''
Murali Palla, Feb 2021
The following code lets you click on a set of points 
and then create a curve that fits the set of points.
In order to execute this code, 
you need to install bokeh, 
I recommend using a package like Anaconda so that you will not have
issues with compatibility of different versions etc.
How to execute:
    Normally you will execute like this
Go to a shell and say this
bokeh serve --show draggable.py

But in the following code, 
we issue a system command so that Python itself 
will call the bokeh server, 
so run like a normal python code from a shell or Ipython console. 
'''

from bokeh.io import curdoc
from bokeh.plotting import figure, output_file
from bokeh.layouts import column,row
from bokeh.models import ColumnDataSource
from bokeh.models import PointDrawTool
from bokeh.models import Button
from bokeh.events import DoubleTap
from scipy.spatial import ConvexHull
import numpy as np
from scipy import interpolate
from os import sys
from os import system
print('START OF THE PROGRAM')

try:
    print(sys.argv)
    if len(sys.argv)<=1:
       command='bokeh serve --show draggablepoints_demo.py --args d1 d2 d3'
       if system(command) == 0:
           pass
       else:
           print('Error occured in running the program')    
           exit()
except:
    print('Error in system command (may be)')
    exit()
finally:
    pass
       
# Create a plot
fig = figure( title="CAD/Curves/01 Curve Fit", 
              plot_width=800,
              plot_height=500,
              x_range=(-5, 5), 
              y_range=(-5, 5)
              )
fig.title.text_font_size='24pt'
fig.title.text_color='blue'
# Create some data sources
xydict=dict(x=[],y=[])
psource = ColumnDataSource(data=xydict)
csource = ColumnDataSource(data=xydict)
hsource = ColumnDataSource(data=xydict)
# Create some glyphs
lines       = fig.line('x', 'y', source=psource)
vertices    = fig.square('x', 'y', source=psource,size=10)
curved      = fig.line('x','y',source=csource, color='red')
hullbnd     = fig.patch('x','y',
                        source=hsource,
                        fill_color='red',
                        fill_alpha=0.1)

# curve fitting/interpolation

def curvefit():
    print('Interpolation')
    xarr=np.array(psource.data['x'])
    yarr=np.array(psource.data['y'])
    f=interpolate.interp1d(xarr,yarr,kind='cubic')
    x1arr=np.linspace(xarr.min(),xarr.max(),100)
    y1arr=f(x1arr)
    csource.data['x']=x1arr.tolist()
    csource.data['y']=y1arr.tolist()
    
# constructing a convex hull

def conhull():
    xarr=np.array(psource.data['x'])
    yarr=np.array(psource.data['y'])
    pt=np.array([xarr,yarr])
    hull=ConvexHull(pt.T)
    bnd=np.append(hull.vertices,hull.vertices[0])
    hsource.data['x']=pt.T[bnd,0].tolist()
    hsource.data['y']=pt.T[bnd,1].tolist()

# clear all 
def clearall():
    psource.data['x']=[]
    psource.data['y']=[]
    csource.data['x']=[]
    csource.data['y']=[]
    hsource.data['x']=[]
    hsource.data['y']=[]

##################################################################

def callback(event):
    curvefit()
    conhull()
    
fig.on_event(DoubleTap,callback)


##################################################################

xbutton=Button(label='Exit')
def xbutton_func():
    exit()
xbutton.on_click(xbutton_func)
###################################################################
    
cfitbutton=Button(label='Curve Fit')
def cfit_func():
    curvefit()
        
cfitbutton.on_click(cfit_func)

#########################################################
hullbutton=Button(label='Show Convex Hull')
def hullbutton_func():
    conhull()
        
hullbutton.on_click(hullbutton_func)
##########################################################
wipebutton=Button(label='Clear all points')
def wipe_func():
    clearall()
    
wipebutton.on_click(wipe_func)        
##########################################################




brow1 = row(cfitbutton,hullbutton)
brow2 = row(wipebutton,xbutton)
layout = column(fig,brow1,brow2)

pointdrawtool = PointDrawTool(renderers=[vertices,lines,curved,hullbnd])
fig.add_tools(pointdrawtool)


curdoc().add_root(layout)