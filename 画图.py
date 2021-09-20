import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
plt.rcParams['font.sans-serif'] = ['Arial Unicode Ms']
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
pd.options.display.max_columns=None

df= pd.read_pickle('/Users/hanxiaohui/Documents/python/明细_20200930.pkl')
df.dropna(subset = ['投向行业三'],how='any',inplace=True,axis=0)
机构不良 = df.query('监管五级分类.isin(["次级","可疑","损失"])').groupby('投向行业三')['折算后人民币'].sum()
机构不良.name = '不良余额'
机构贷款合计 = df.groupby('投向行业三')['折算后人民币'].sum()
机构贷款合计.name = '贷款合计'
df_merge = pd.merge(机构不良,机构贷款合计,left_index = True,right_index=True)
df_merge['不良率'] = df_merge['不良余额']/df_merge['贷款合计']
df_merge[['不良余额', '贷款合计']] = df_merge[['不良余额','贷款合计']].apply(lambda x:round(x/10000,2))
机构 = df_merge
机构.sort_values(by = '不良余额',ascending=True,inplace=True)
#
布 = plt.figure(figsize=(10,20),dpi=100)
图1 = 布.add_subplot(111)
图1.bar(x=0,bottom=机构.index,height=0.5,width=机构.不良余额,orientation='horizontal',label='不良余额')
图1.legend(loc=(0.7,0.05))
图2 = 图1.twiny()
图2.plot(机构.不良率,机构.index,'or-',label='不良率')
图2.legend(loc=(0.7,0.15))
百分比 = ticker.PercentFormatter(1,2)
图2.xaxis.set_major_formatter(百分比)

for x,y in zip(机构.不良率,机构.index):
    plt.text(x,y,str(round(x*100,2))+'%',fontsize = 10)
plt.tight_layout()
plt.grid(axis='y')
plt.show()
# print(df)