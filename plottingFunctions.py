import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import copy



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