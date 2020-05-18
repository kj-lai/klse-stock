import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline
sns.set()

stock_code = pd.read_csv('../personal/stock_code_table.csv')
data1 = pd.read_csv('../personal/klse_screener_52week_price.csv')
data2 = pd.read_csv('../personal/klse_morningstar_merge_split.csv', parse_dates=['split_date'])
data3 = pd.read_csv('../personal/klse_10yr_data.csv')
data4 = pd.read_csv('../personal/klse_stock_stage_4.csv')
data5 = pd.read_csv('../personal/klse_stock_intrinsic.csv')
data6 = pd.read_csv('../personal/klse_stock_dividend_yield.csv')
data2['code'] = data2['code'].astype(str).apply(lambda x: x.zfill(4))
data3['code'] = data3['code'].astype(str).apply(lambda x: x.zfill(4))
data4['code'] = data4['code'].astype(str).apply(lambda x: x.zfill(4))
data5['code'] = data5['code'].astype(str).apply(lambda x: x.zfill(4))
data6['code'] = data6['code'].astype(str).apply(lambda x: x.zfill(4))

def show_tables(input_code):
    symbol = ['—','\xa0-\xa0']
    temp1 = data5[data5.code == str(input_code)]
    temp = temp1.columns.tolist()
    temp1_1 = temp1[temp[1:8]+temp[14:18]]
    temp1_2 = temp1[temp[:1]+temp[8:14]+temp[18:]]
    if len(temp1) == 0:
        temp4 = data6[data6.code == str(input_code)]
        temp = temp4.columns.tolist()
        temp4_1 = temp4[temp[1:8]+temp[14:18]]
        temp4_2 = temp4[temp[:1]+temp[8:14]+temp[18:]]
    temp2 = data3[data3.code == str(input_code)] # the 10 years data
    if len(temp2) == 0:
        print('<<<  This Stock did not pass Stage 1 filter.  >>>')
        return None, None, None
    temp3 = temp2.T.reset_index()
    temp3.columns = ['Year'] + temp3.iloc[1].tolist()[1:]
    temp3.drop(index=[0,1], inplace=True)
    temp_show = temp3.copy()
    for cols in ['NP','OCF','Revenue','Shares']:
        temp3[cols] = temp3[cols].apply(lambda x: int(x.replace(',','')) if x not in symbol else 0)
    for cols in ['D/E','DPS','Div Payout','EPS','EPS GR','EPS GR 10Y avg','EPS GR 5Y avg','NP Margin','NTA',
                 'OCF GR','Price','ROE','Revenue GR','Revenue GR 10Y avg','Revenue GR 5Y avg']:
        temp3[cols] = temp3[cols].apply(lambda x: float(x.replace(',','')) if x not in symbol else 0.0)
    temp_np = temp3['NP'].tolist()
    temp_shares = temp3['Shares'].tolist()
    temp_price = temp3['Price'].tolist()
    temp3['ROI'] = temp3.apply(lambda x: np.around(x['NP']/(x['Shares']*x['Price'])*100, 2) if x['Price'] != 0 else 0.0, axis=1)
    temp_show['ROI'] = temp3['ROI']
    temp3['EY'] = temp3.apply(lambda x: np.around(x['EPS']/x['Price']*100, 2) if x['Price'] != 0 else 0.0, axis=1)
    temp_show['EY'] = temp3['EY']
    temp3['P/E'] = temp3.apply(lambda x: np.around(x['Price']/x['EPS'], 2) if x['EPS'] != 0 else 0.0, axis=1)
    temp_show['P/E'] = temp3['P/E']
    temp3['DY'] = temp3.apply(lambda x: np.around(x['DPS']/x['Price']*100, 2) if x['Price'] != 0 else 0.0, axis=1)
    temp_show['DY'] = temp3['DY']
    temp = temp_show.columns.tolist()
    col_list = [temp[0],temp[-5],temp[-6],temp[13],temp[10],temp[-4],temp[14]]+temp[8:10]+temp[-3:-1]+temp[4:6]+[temp[7],temp[6]]+\
               temp[-1:]+temp[2:4]+[temp[15],temp[16],temp[18],temp[17]]+temp[11:13]+temp[1:2]
    temp_show = temp_show[col_list]
    
    try:
        if len(temp1) != 0:
            title = temp1.name.values[0]
        else:
            title = temp4.name.values[0]
    except:
        title = ''
    
    # print('----- Stock Details for '+str(input_code)+': '+title+' -----')
    # if len(temp1) != 0:
    #     display(temp1_1)
    #     display(temp1_2.iloc[:, :19])
    #     display(temp1_2.iloc[:, 19:33])
    #     display(temp1_2.iloc[:, 33:])
    # else:
    #     if len(temp4_1) != 0:
    #         display(temp4_1)
    #         display(temp4_2.iloc[:, :19])
    #         display(temp4_2.iloc[:, 19:33])
    #         display(temp4_2.iloc[:, 33:])
    #     else:
    #         print('<<<  This Stock did not pass Stage 4 filter.  >>>')
        
    # print('\n----- Past 10 Year Financials -----')
    # display(temp_show)
    
    # print('\n----- Plot Graphs -----')
    fig1, fig2, fig3 = plot_tables(temp3[::-1])
    if len(temp1) != 0:
        return temp1_1, temp1_2, temp_show, fig1, fig2, fig3
    else:
        return temp4_1, temp4_2, temp_show, fig1, fig2, fig3

def add_trendline(x, y):
    z = np.polyfit(x, y, 1)
    return z, np.poly1d(z)(x)

def plot_tables(table):
    nYear = len([x for x in table['NP'].tolist() if x != 0])
    
    fig1, ax = plt.subplots(1, 2, figsize=(20,6))
    fig1.patch.set_facecolor('white')
    ax0 = ax[0].twinx()
    ax[0].bar(np.arange(10)-0.2, table['NP'], color='black', width=0.4, alpha=0.7)
    ax0.bar(np.arange(10)+0.2, table['NP Margin'], color='red', width=0.4, alpha=0.7)
    ax[0].set_xticks(np.arange(0,10,1))
    ax[0].set_xticklabels(table.Year)
    ax[0].set_xlabel('Year')
    ax[0].set_ylabel('Net Profit')
    ax0.set_ylabel('NP Margin (%)')
    ax[0].set_title('Net Profit vs NP Margin')
    coeff1, line1 = add_trendline(np.arange(nYear)-0.2, table['NP'][-nYear:])
    coeff2, line2 = add_trendline(np.arange(nYear)+0.2, table['NP Margin'][-nYear:])
    ax[0].legend([str(np.around(coeff1[0],2))] ,loc="upper left")
    ax0.legend([str(np.around(coeff2[0],2))] ,loc="upper left", bbox_to_anchor=(0, 0.94))
    ax[0].plot(np.arange((10-nYear),10)-0.2, line1, '--', color='black', linewidth=3)
    ax0.plot(np.arange((10-nYear),10)+0.2, line2, '--', color='red', linewidth=3)

    
    ax0 = ax[1].twinx()
    ax[1].bar(np.arange(10)-0.3, table['Revenue'], color='black', width=0.3, alpha=0.7)
    ax0.bar(np.arange(10), table['OCF'], color='red', width=0.3, alpha=0.7)
    ax0.bar(np.arange(10)+0.3, table['NP'], color='blue', width=0.3, alpha=0.7)
    ax[1].set_xticks(np.arange(0,10,1))
    ax[1].set_xticklabels(table.Year)
    ax[1].set_xlabel('Year')
    ax[1].set_ylabel('MYR Mil')
    ax[1].set_title('Revenue vs Operating Cash Flow vs Net Profit')
    coeff1, line1 = add_trendline(np.arange(nYear)-0.3, table['Revenue'][-nYear:])
    coeff2, line2 = add_trendline(np.arange(nYear), table['OCF'][-nYear:])
    coeff3, line3 = add_trendline(np.arange(nYear)+0.3, table['NP'][-nYear:])
    ax[1].legend(['Revenue : '+str(np.around(coeff1[0],2))], loc="upper left")
    ax0.legend(['OCF : '+str(np.around(coeff2[0],2)),
                'NP : '+str(np.around(coeff3[0],2))], loc="upper left",bbox_to_anchor=(0, 0.94))
    ax[1].plot(np.arange((10-nYear),10)-0.3, line1, '--', color='black', linewidth=3)
    ax0.plot(np.arange((10-nYear),10), line2, '--', color='red', linewidth=3)
    ax0.plot(np.arange((10-nYear),10)+0.3, line3, '--', color='blue', linewidth=3)
    
    
    fig2, ax = plt.subplots(1, 2, figsize=(20,6))
    fig2.patch.set_facecolor('white')
    ax0 = ax[0].twinx()
    ax[0].bar(np.arange(10)-0.2, table['EY'], color='black', width=0.4, alpha=0.7)
    ax0.bar(np.arange(10)+0.2, table['DY'], color='red', width=0.4, alpha=0.7)
    ax[0].set_xticks(np.arange(0,10,1))
    ax[0].set_xticklabels(table.Year)
    ax[0].set_xlabel('Year')
    ax[0].set_ylabel('Earning Yield (%)')
    ax0.set_ylabel('Dividend Yield (%)')
    ax[0].set_title('Earning Yield vs Dividend Yield') 
    coeff1, line1 = add_trendline(np.arange(nYear)-0.2, table['EY'][-nYear:])
    coeff2, line2 = add_trendline(np.arange(nYear)+0.2, table['DY'][-nYear:])
    ax[0].legend([str(np.around(coeff1[0],2))] ,loc="upper left")
    ax0.legend([str(np.around(coeff2[0],2))] ,loc="upper left", bbox_to_anchor=(0, 0.94))
    ax[0].plot(np.arange((10-nYear),10)-0.2, line1, '--', color='black', linewidth=3)
    ax0.plot(np.arange((10-nYear),10)+0.2, line2, '--', color='red', linewidth=3)
    
    
    ax[1].bar(np.arange(10)-0.2, table['EPS'], color='black', width=0.4, alpha=0.7)
    ax[1].bar(np.arange(10)+0.2, table['DPS'], color='red', width=0.4, alpha=0.7)
    ax[1].set_xticks(np.arange(0,10,1))
    ax[1].set_xticklabels(table.Year)
    ax[1].set_xlabel('Year')
    ax[1].set_ylabel('Amount per Share (Sen)')
    ax[1].set_title('Earning per Share vs Dividend per Share')
    coeff1, line1 = add_trendline(np.arange(nYear)-0.2, table['EPS'][-nYear:])
    coeff2, line2 = add_trendline(np.arange(nYear)+0.2, table['DPS'][-nYear:])
    ax[1].legend(['EPS : '+str(np.around(coeff1[0],2)),
                  'DPS : '+str(np.around(coeff2[0],2))],loc="upper left")
    ax[1].plot(np.arange((10-nYear),10)-0.2, line1, '--', color='black', linewidth=3)
    ax[1].plot(np.arange((10-nYear),10)+0.2, line2, '--', color='red', linewidth=3)
    
    
    fig3, ax = plt.subplots(1, 2, figsize=(20,6))
    fig3.patch.set_facecolor('white')
    ax0 = ax[0].twinx()
    ax[0].bar(np.arange(10)-0.2, table['Price'], color='black', width=0.4, alpha=0.7)
    ax0.bar(np.arange(10)+0.2, table['P/E'], color='red', width=0.4, alpha=0.7)
    ax[0].set_xticks(np.arange(0,10,1))
    ax[0].set_xticklabels(table.Year)
    ax[0].set_xlabel('Year')
    ax[0].set_ylabel('Share Price (RM)')
    ax0.set_ylabel('Ratio')
    ax[0].set_title('Price vs P/E Ratio')
    coeff1, line1 = add_trendline(np.arange(nYear)-0.2, table['Price'][-nYear:])
    coeff2, line2 = add_trendline(np.arange(nYear)+0.2, table['P/E'][-nYear:])
    ax[0].legend([str(np.around(coeff1[0],2))] ,loc="upper left")
    ax0.legend([str(np.around(coeff2[0],2))] ,loc="upper left", bbox_to_anchor=(0, 0.94))
    ax[0].plot(np.arange((10-nYear),10)-0.2, line1, '--', color='black', linewidth=3)
    ax0.plot(np.arange((10-nYear),10)+0.2, line2, '--', color='red', linewidth=3)
    
    
    ax[1].bar(np.arange(10)-0.2, table['ROI'], color='black', width=0.4, alpha=0.7)
    ax[1].bar(np.arange(10)+0.2, table['ROE'], color='red', width=0.4, alpha=0.7)
    ax[1].set_xticks(np.arange(0,10,1))
    ax[1].set_xticklabels(table.Year)
    ax[1].set_xlabel('Year')
    ax[1].set_ylabel('Percentage (%)')
    ax[1].set_title('Return on Investment vs Return on Equity')
    coeff1, line1 = add_trendline(np.arange(nYear)-0.2, table['ROI'][-nYear:])
    coeff2, line2 = add_trendline(np.arange(nYear)+0.2, table['ROE'][-nYear:])
    ax[1].legend(['ROI : '+str(np.around(coeff1[0],2)),
                  'ROE : '+str(np.around(coeff2[0],2))],loc="upper left")
    ax[1].plot(np.arange((10-nYear),10)-0.2, line1, '--', color='black', linewidth=3)
    ax[1].plot(np.arange((10-nYear),10)+0.2, line2, '--', color='red', linewidth=3)
    
    
    return fig1, fig2, fig3