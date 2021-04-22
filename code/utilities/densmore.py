import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def sum_stats(dataframe, filename_string, y_variable):
        
    import sys
    with open(f'{filename_string}', 'w') as f:

        ## COLUMN HEADERS 
        print('index'     ,',',     # 0
              'feature'   ,',',     #
              'dtype'     ,',',     #   
              'non-nulls' ,',',     # 'alias: col_count'
              'nulls'     ,',',     #
              'pct_nulls' ,',',     # 5
              'unique'    ,',',     #
              'mode'      ,',',     #
              'mode_count',',',     #
              ''          ,',',
              'min'       ,',',     #
              'q1'        ,',',     # 10
              'median'    ,',',     #
              'q3'        ,',',     #
              'max'       ,',',     # 
              ''          ,',',        
              'mean'      ,',',     #
              'stdev'     ,',',     # 15
              'var'       ,',',     #
              'skew'      ,',',     #
              'kurtosis'  ,',',     #
              'y_corr',             #
              file=f
             )
        col_index = -1  # for index column, starting the numbering at -1 so first row is 0
        
        ## VARIABLE ASSIGNMENTS (DETERMINED BY DATATYPE) 
        for (columnName, columnData) in dataframe.iteritems():
                ## OBJECTS
            if columnData.dtype == object:                                   
                col_index += 1                                                        # 0
                col_name = columnName                                                 #
                col_dtype = columnData.dtype                                          #
                col_count = columnData.count()   #non-nulls                           #
                col_nulls = columnData.isnull().sum()                                 #
                col_pct_nulls = round((columnData.isnull().sum())/len(columnData),2)  # 5
                col_unique = columnData.nunique()                                     # 
                col_mode = list(columnData.value_counts().items())[0][0]              #
                col_mode_count = columnData.value_counts().max()                      #
                
                col_min = ''                                                          #
                col_q1 = ''                                                           # 10
                col_median = ''                                                       #
                col_q3 = ''                                                           #
                col_max = ''                                                          #
                
                col_mean = ''                                                         #
                col_stdev = ''                                                        # 15
                col_var = ''                                                          #
                col_skew = ''                                                         # 
                col_kurt = ''                                                         #
                col_y_corr = ''                                                       #
                  
                ## NUMERICS
            else:     
                col_index += 1                                                        # 0
                col_name = columnName                                                 #                
                col_dtype = columnData.dtype                                          #
                col_count = columnData.count()   #non-nulls                           #  
                col_nulls = columnData.isnull().sum()                                 #
                col_pct_nulls = round((columnData.isnull().sum())/len(columnData),2)  # 5
                col_unique = columnData.nunique()                                     # 
                col_mode = list(columnData.value_counts().items())[0][0]              #
                col_mode_count = columnData.value_counts().max()                      #          
                
                col_min = columnData.min()                                            #
                col_q1 = columnData.quantile(.25)                                     # 10
                col_median = columnData.median()                                      #
                col_q3 = columnData.quantile(.75)                                     #           
                col_max = columnData.max()                                            #
                
                col_mean = columnData.mean()                                          #
                col_stdev = columnData.std()                                          # 15
                col_var = columnData.var()                                            #
                col_skew = columnData.skew()                                          #
                col_kurt = columnData.kurtosis()                                      #
                col_y_corr = columnData.corr(dataframe[y_variable])                   #

                ## PRINT VARIABLES
            print(col_index       ,',',     # 0
                  col_name        ,',',     #
                  col_dtype       ,',',     #
                  col_count       ,',',     #
                  col_nulls       ,',',     #
                  col_pct_nulls   ,',',     # 5
                  col_unique      ,',',     #
                  col_mode        ,',',     #
                  col_mode_count  ,',',     #
                  ''              ,',',
                  col_min         ,',',     #
                  col_q1          ,',',     # 10                
                  col_median      ,',',     #
                  col_q3          ,',',     #                  
                  col_max         ,',',     #
                  ''              ,',',                  
                  col_mean        ,',',     #
                  col_stdev       ,',',     # 15
                  col_var         ,',',     #
                  col_skew        ,',',     #
                  col_kurt        ,',',     #
                  col_y_corr,               #
                  file=f
                  )



def val_counts(dataframe):

    for (columnName, columnData) in dataframe.iteritems():

        print(f'Column Name: {columnName}')
        print(f'Unique Values: {dataframe[columnName].nunique()}')
        print('')
        print(dataframe[columnName].value_counts())
        print('')
        print('_________________________')
        print('')
        print('')



def all_uniques(dataframe):

    for (columnName, columnData) in dataframe.iteritems():

        print(f'Column Name: {columnName}')
        print(f'Unique Values: {np.sort(dataframe[columnName].unique())}')
        print('')
        print('')
        print('_________________________')
        print('')
        print('')



def rapid_plots(dataframe, y_var,min_corr):
    plt.style.use('seaborn-darkgrid')             # removable or customizable

    plot_list = [] 

    for (columnName, columnData) in dataframe.iteritems():
        if columnData.dtype != object:
            if (abs(columnData.corr(dataframe[y_var])) > min_corr) and columnData.corr(dataframe[y_var]) != 1:
                plt.figure()
                viz = sns.regplot(x=dataframe[columnName], y=dataframe[y_var], color='steelblue')
                plt.title(f'{columnName}: {round(columnData.corr(dataframe[y_var]), 5)}')
                plot_list.append(viz)
            else:
                pass
        else:
            pass
                
    return plot_list