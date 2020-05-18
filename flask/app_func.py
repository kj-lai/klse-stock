import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline
sns.set()

stock_code = pd.read_csv('../personal/stock_code_table.csv')
data1 = pd.read_csv('../personal/klse_screener_52week_price.csv')
data2 = pd.read_csv('../personal/klse_morningstar_merge_split.csv', parse_dates=['split_date'])
data3 = pd.read_csv('../personal/klse_investor_10yr.csv')
data4 = pd.read_csv('../personal/klse_stock_stage_4.csv')
data5 = pd.read_csv('../personal/klse_stock_intrinsic.csv')
data6 = pd.read_csv('../personal/klse_stock_dividend_yield.csv')
data2['code'] = data2['code'].astype(str).apply(lambda x: x.zfill(4))
data3['code'] = data3['code'].astype(str).apply(lambda x: x.zfill(4))
data4['code'] = data4['code'].astype(str).apply(lambda x: x.zfill(4))
data5['code'] = data5['code'].astype(str).apply(lambda x: x.zfill(4))
data6['code'] = data6['code'].astype(str).apply(lambda x: x.zfill(4))

def show_tables(input_code):
    symbol = ['  -  ', '-', '- %', '\xa0-\xa0', '\xa0-\xa0 %', '-\xa0 %', 'nan']
    temp1 = data5[data5.code == str(input_code)]
    # temp = temp1.columns.tolist()
    # col_1 = [temp[-4],temp[29],temp[28]]+temp[26:28]+[temp[-5]]+temp[-9:-5]+temp[-3:]
    # col_2 = temp[:2]+[temp[25]]+temp[2:9]+temp[15:18]+temp[9:15]+temp[18:25]
    # temp1 = temp1[col_1 + col_2]
    temp1_1 = temp1.iloc[:, :13]
    temp1_2 = temp1.iloc[:, 13:]
    if len(temp1) == 0:
        temp4 = data6[data6.code == str(input_code)]
        # temp = temp4.columns.tolist()
        # col_1 = [temp[-1],temp[29],temp[28]]+temp[26:28]+[temp[-2]]+temp[-6:-2]
        # col_2 = temp[:2]+[temp[25]]+temp[2:9]+temp[15:18]+temp[9:15]+temp[18:25]
        # temp4 = temp4[col_1 + col_2]
        temp4_1 = temp4.iloc[:, :10]
        temp4_2 = temp4.iloc[:, 10:]
    temp2 = data3[data3.code == str(input_code)]
    if len(temp2) == 0:
        # print('This Stock did not pass 1st stage filter.')
        return 'msg', None, None, None
    temp3 = temp2.T.reset_index()
    temp3.columns = ['Year'] + temp3.iloc[2].tolist()[1:]
    temp3.drop(index=[0,1,2], inplace=True)
    temp_show = temp3.copy()
    for cols in ['NP','Div','NOSH']:
        temp3[cols] = temp3[cols].apply(lambda x: int(x.replace(',','')) if str(x).strip() not in symbol else 0)
    for cols in ['Div Payout','NP Margin','ROE', 'EPS GR']:
        temp3[cols] = temp3[cols].apply(lambda x: float(x.replace('%','').replace(',','')) if str(x).strip() not in symbol else 0.0)
    for cols in ['EPS','DPS','Price','P/E','DY']:
        temp3[cols] = temp3[cols].apply(lambda x: float(x) if str(x).strip() not in symbol else 0.0)
    temp3['ROI'] = np.around(temp3['NP']/(temp3['NOSH']*temp3['Price'])*100, 2)
    temp_show['ROI'] = temp3['ROI']
    temp_cols = temp_show.columns.tolist()
    temp_show = temp_show[temp_cols[:8]+temp_cols[-1:]+temp_cols[8:-1]]
    
    try:
        if len(temp1) != 0:
            title = temp1.name.values[0]
        else:
            title = temp4.name.values[0]
    except:
        title = ''
        
    # print('----- Stock Details for '+str(input_code)+': '+title+' -----')
    # display(temp1.iloc[:, :18])
    # display(temp1.iloc[:, 18:])

    # if len(temp1) == 0:
    #     display(temp4.iloc[:, :18])
    #     display(temp4.iloc[:, 18:])
        
    # print('\n----- Past 10 Year Financials -----')
    # display(temp_show)
    
    # print('\n----- Plot Graphs -----')
    table, _ = plot_tables(temp3[::-1])
        
    if len(temp1) != 0:
        return temp1_1, temp1_2, temp_show, table
    else:
        return temp4_1, temp4_2, temp_show, table

def plot_tables(table):
    fig, ax = plt.subplots(3, 2, figsize=(20,20))
    fig.patch.set_facecolor('white')
    ax0 = ax[0,0].twinx()
    ax[0,0].bar(np.arange(10)-0.2, table['NP'], color='r', width=0.4)
    ax0.bar(np.arange(10)+0.2, table['NP Margin'], color='k', width=0.4)
    ax[0,0].set_xticks(np.arange(0,10,1))
    ax[0,0].set_xticklabels(table.Year)
    ax[0,0].set_xlabel('Year')
    ax[0,0].set_ylabel('Net Profit')
    ax0.set_ylabel('NP Margin (%)')
    ax[0,0].set_title('Net Profit vs NP Margin')

    ax[0,1].bar(np.arange(10)-0.2, table['NP'], color='r', width=0.4)
    ax[0,1].bar(np.arange(10)+0.2, table['Div'], color='k', width=0.4)
    ax[0,1].set_xticks(np.arange(0,10,1))
    ax[0,1].set_xticklabels(table.Year)
    ax[0,1].set_xlabel('Year')
#     ax[0,1].set_ylabel("Volume '000")
    ax[0,1].set_title('Net Profit vs Dividend')
    ax[0,1].legend(['NP','Div'],loc="upper right")
    
    ax0 = ax[1,0].twinx()
    ax[1,0].bar(np.arange(10)-0.2, table['Div Payout'], color='r', width=0.4)
    ax0.bar(np.arange(10)+0.2, table['DY'], color='k', width=0.4)
    ax[1,0].set_xticks(np.arange(0,10,1))
    ax[1,0].set_xticklabels(table.Year)
    ax[1,0].set_xlabel('Year')
    ax[1,0].set_ylabel('Divident Payout (%)')
    ax0.set_ylabel('Dividend Yield (%)')
    ax[1,0].set_title('Divident Payout vs Dividend Yield')
    # ax[1,0].legend(['Div Payout','Div Yield'],loc="upper right")   

    ax[1,1].bar(np.arange(10)-0.2, table['EPS'], color='r', width=0.4)
    ax[1,1].bar(np.arange(10)+0.2, table['DPS'], color='k', width=0.4)
    ax[1,1].set_xticks(np.arange(0,10,1))
    ax[1,1].set_xticklabels(table.Year)
    ax[1,1].set_xlabel('Year')
    ax[1,1].set_ylabel('Amount per Share (Sen)')
    ax[1,1].set_title('Earning per Share vs Dividend per Share')
    ax[1,1].legend(['EPS','DPS'],loc="upper right")

    ax0 = ax[2,0].twinx()
    ax[2,0].bar(np.arange(10)-0.2, table['Price'], color='r', width=0.4)
    ax0.bar(np.arange(10)+0.2, table['P/E'], color='k', width=0.4)
    ax[2,0].set_xticks(np.arange(0,10,1))
    ax[2,0].set_xticklabels(table.Year)
    ax[2,0].set_xlabel('Year')
    ax[2,0].set_ylabel('Share Price (RM)')
    ax0.set_ylabel('Ratio')
    ax[2,0].set_title('Price per Share vs P/E Ratio')
    
    ax[2,1].bar(np.arange(10)-0.2, table['ROI'], color='r', width=0.4)
    ax[2,1].bar(np.arange(10)+0.2, table['ROE'], color='k', width=0.4)
    ax[2,1].set_xticks(np.arange(0,10,1))
    ax[2,1].set_xticklabels(table.Year)
    ax[2,1].set_xlabel('Year')
    ax[2,1].set_ylabel('Percentage (%)')
    ax[2,1].set_title('Return on Investment vs Return on Equity')

    return fig, ax