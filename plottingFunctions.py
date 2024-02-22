import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import copy
from datetime import datetime
from datetime import timedelta
import matplotlib.dates as mdates
import matplotlib.colors as mcolors
from dateutil.parser import parse

def plot_daily_boxplot_with_annot(data2:pd.DataFrame,datetime_intervals_:pd.DataFrame,datetime_intervals_2_:pd.DataFrame):
    data=copy.copy(data2)
    datetime_intervals=copy.copy(datetime_intervals_)
    datetime_intervals_2=copy.copy(datetime_intervals_2_)
    data['Numerical_Date'] = data['date'].apply(lambda x: x.toordinal())
    fig=plt.figure(figsize=(10, 6))
    plt.grid()
    ax=sns.boxplot( data=data,x='Numerical_Date',y='value')

    dates=data['date'].drop_duplicates()
    ax.set_xticklabels(dates.apply(lambda x: x.strftime('%Y-%m-%d')), rotation=45,rotation_mode='anchor',ha='right')
    #ax.set_xticks(dates.toordinal())

    print('xtickslabel:')

    locs,labels=plt.xticks()
    print(f'Locs: {locs}')
    print(f'Labels: {labels}')

    #ax.set_xticks(list(data['Numerical_Date'].unique()))
    ax.set_xticklabels(dates.dt.strftime('%Y-%m-%d'), rotation=45,rotation_mode='anchor',ha='right')



    locs,labels=plt.xticks()
    print(f'Locs: {locs}')
    print(f'Labels: {labels}')

    print(ax.get_xticks())
    # Overlay the intervals on the plot
    for i,interval in datetime_intervals.iterrows():
        start_date = interval[0].toordinal()
        print(start_date)
        end_date = interval[1].toordinal()
        print(end_date)
        gf_dates=[start_date,end_date]
        gf_dates_remapped=np.interp(gf_dates,data['Numerical_Date'].unique(),locs)
        print(gf_dates_remapped)
        if i==0:
            ax.axvspan(gf_dates_remapped[0]-0.5,gf_dates_remapped[1]+0.5,0,.2, alpha=0.3, color='orange',label="WS")
        else:
            ax.axvspan(gf_dates_remapped[0]-0.5,gf_dates_remapped[1]+0.5,0,.2, alpha=0.3, color='orange')

    for i,interval in datetime_intervals_2.iterrows():
        start_date = interval[0].toordinal()
        print(start_date)
        end_date = interval[1].toordinal()
        print(end_date)
        gf_dates=[start_date,end_date]
        gf_dates_remapped=np.interp(gf_dates,data['Numerical_Date'].unique(),locs)
        print(gf_dates_remapped)
        if i==0:
            ax.axvspan(gf_dates_remapped[0]-0.5,gf_dates_remapped[1]+0.5,0.2,0.4, alpha=0.3, color='purple',label="CL")
        else:
            ax.axvspan(gf_dates_remapped[0]-0.5,gf_dates_remapped[1]+0.5,0.2,0.4, alpha=0.3, color='purple')
    
    
    plt.legend()
    
    plt.xlabel('Date')
    plt.ylabel('Values')
    plt.title('Boxplot with DateTime X-axis')
    return fig,ax

def time_interval_plotting(datetime_intervals_in:pd.DataFrame,xmin,xmax,ymin=.1,ymax=.2,annotations=None,ax=None):
    datetime_intervals=copy.copy(datetime_intervals_in)
    if ax is None:
        ax=plt.gca()

    ax.autoscale(True)
    bbox = dict(boxstyle="round", fc="0.8")
    arrowprops = dict(
        arrowstyle="-[,widthB=3",
        connectionstyle="angle,angleA=0,angleB=90,rad=10",
        facecolor='red',linewidth=2,edgecolor='red')

    xyoffset=50

    rectangles=[]
    kk=0
    for i,interval in enumerate(datetime_intervals.iterrows()):
        print(interval)
        ypos=76
        x_start,x_end=interval[1]['begin'],interval[1]['end']
        #x_start,x_end=max([interval[1]['begin'],xmin]),min([interval[1]['end'],xmax])
        ax.hlines(ypos+i*5, x_start, x_end)
        if (annotations is not None) and (annotations[i]!=''):
            ax.annotate(annotations[i],(interval[1]['begin'],ypos+i*5,),bbox=bbox,arrowprops=arrowprops,
                        xytext=(xyoffset,xyoffset),textcoords='offset points',annotation_clip=False)

        rect=ax.axvspan(x_start, x_end, ymin, ymax, color='gray', alpha=0.5)
        kk=kk+1
        if kk==1:
            rect.set_label('DTC')
        rectangles.append(rect)
        ax.autoscale(True)
    return ax


def string_to_datetime(in_string,dt_format=None):
    if dt_format is not None:
        out_date = datetime.strptime(in_string,dt_format)
    else:  
        try:
            dt_format='%Y-%m-%d'
            out_date = datetime.strptime(in_string,dt_format)
        except ValueError:
            try:
                dt_format='%Y-%m-%d %H:%M:%S'
                out_date = datetime.strptime(in_string,dt_format)
            except ValueError:
                try:
                    dt_format='%d-%b-%Y %H:%M:%S'
                    out_date = datetime.strptime(in_string,dt_format)
                except:
                    try:
                        dt_format='Auto'
                        out_date=parse(in_string)
                    except:
                        raise ValueError
    print(f"{in_string} converted to {out_date} using format {dt_format}")
    return out_date, dt_format

def event_plot(events,y_coord,label=None,annotations=None,arrowprops=None,ax=None):
    '''Plots a specific type of events, all with the same format'''
    if ax is None:
        ax=plt.gca()
    try:
        iter(events)
    except:
        ValueError(f"events variable must be an iterable. {type(events)} is not iterable")
    ax.scatter(events,[y_coord]*len(events),marker='x',s=800,label=label)

    if annotations is not None:
        bbox = dict(boxstyle="round", fc="0.8")
        if arrowprops is None:
            arrowprops = dict(
                arrowstyle="->",
                connectionstyle="angle,angleA=0,angleB=90,rad=10",
                facecolor='red',linewidth=2,edgecolor='red')

        for e_dt,ann in zip(events,annotations):
            if ann!='':
                ax.annotate(ann,(e_dt,.5),bbox=bbox,arrowprops=arrowprops,
                            xytext=(50,50),textcoords='offset points',annotation_clip=False)
    return ax


def detail_HI_plot(hi_df_in:pd.DataFrame,datetime_intervals,interval_annotations=None,
                   events=None,event_annotations=None,events_labeel=None,events_arrowprops=None,
                   start_date=None,end_date=None,figsize=(15,5),major_locator=None):
    hi_df=copy.copy(hi_df_in)
    
    if type(start_date) ==str:
        start_date,_ = string_to_datetime(start_date)
    if type(end_date) ==str:
        end_date,_ = string_to_datetime(end_date)
    
    xmin,xmax=np.min(hi_df['timestamp']),np.max(hi_df['timestamp'])


    if (start_date is not None) and start_date>xmin:
        xmin =start_date
    if (end_date is not None) and end_date<xmax:
        xmax =end_date
    cmap=plt.get_cmap('jet',lut=100).reversed()
    norm=mcolors.Normalize(0,100)
    fig,ax=plt.subplots(figsize=figsize)

    ax=sns.scatterplot(data=hi_df,x='timestamp',y='HI',hue='HI',palette=cmap,
                    edgecolor='face',s=3,hue_norm=norm,ax=ax,legend=None
                    )
    
    ax=time_interval_plotting(datetime_intervals,xmin,xmax,annotations=interval_annotations)

    ax=event_plot(events,.5,events_labeel,event_annotations,events_arrowprops,ax)
    #plt.ylim(0,140)
    ax.grid()
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
            rotation_mode="anchor")
    plt.xlabel(None)
    handles, labels = ax.get_legend_handles_labels()
    print(handles,labels)
    ax.legend(handles, labels)

    plt.ylim(bottom=0)

    if major_locator is not None:
        ax.xaxis.set_major_locator(major_locator)
    ax.set_xlim(xmin,xmax)
    #plt.legend([])
    return fig,ax
