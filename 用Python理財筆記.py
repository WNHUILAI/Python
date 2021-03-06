
##文字應用
a='Hello Line'
b="Hello Line"
c="""Hello Line"""

c[2]
c.count('l')
c.find('o',1)--->1表示第二個出現的o，可省略不寫
#集合[]
d=[2,5,4,4,3,'Hello']
e=d.append(5)
#字典{}
f={'Line':20,'Ken':30}
f['Lee']=70
print(f)-->變成{'Line':20,'Ken':30,'Lee':70}
f['Line']-->20
len(f)-->3
f.keys()
f.values()

##自己定義的減法函式
def aaa(a,b):
    ret=a - b
    return(ret)-->注意定義的東西必須並排上面，當沒有空行時表示定義結束

h=10
y=4
aaa(h,y)
##引用Package
import datetime
datetime.datetime.now()
datetime.date.today()

##簡單if條件
buy = 40
sell = 30

if buy < sell:
    print('賺錢了')
elif buy == sell:
    print('打平')
else:
    print('虧錢了')
    print(':(')

##簡單for迴圈
for i in (1,2,3,4):
    print(i)
print('------')
for x in range(1,11):
    print(x)

##簡單While
i=1
while(i<5):
    print(i)
    i=i+1

##以下是使用panda 套件，建立以時間序列的資料
date = pd.date_range('20180101', periods=6)
s = pd.Series([2,2,3,4,8,10], index=date)
-------loc:查詢index;iloc:查詢第幾個
s.loc['20180104']-->傳回4
s.loc['20180102':'2018-01-04']-->傳回2,3,4
s.iloc[2]-->傳回3
s.iloc[1:4]-->傳回2,3,4

s.max()
s.min()
s.mean()
s.std()


s.cumsum()--->累加
s.cumprod()--->累乘
.shift()-->將所有數字往後推一格，但這會使第一個變成na
.fillna(0)-->發現na都改成0

------移動窗格
s.rolling(2).sum()--->自己index+前面一個index返回的Value
s.rolling(2).max()--->自己index及前面一個index兩天中最大index，這可以適合用在取7天最大交易額
s.rolling(2).min()
s.rolling(2).mean()
s.rolling(2).std()

----針對序列我們也可以一同做加減乘除
s + 2

---將序列(dataFram也可以
)繪製成圖

%matplotlib inline-->在jupyter中畫圖要加上這一段
s.plot()

##某小明體重從'2018-01-01'為60公斤，由於在'2018-01-03'吃太多，導致隔天起床發現變重5公斤
weight = pd.Series(60, index=pd.date_range('2018-01-01', periods=10))
方法1weight.loc['2018-01-04':] += 5
方法2weight.loc['2018-01-04':] =weight.loc['2018-01-04':] + 5
weight
#使用DataFrame方法
s1 = pd.Series([1,2,3,4,5,6], index=date)
s2 = pd.Series([5,6,7,8,9,10], index=date)
s3 = pd.Series([11,12,5,7,8,2], index=date)

dictionary = {
    'c1': s1,
    'c2': s2,
    'c3': s3,
}

df = pd.DataFrame(dictionary)
df

#累加累乘跟移動窗格都可以用dataFrame呈現

#DataFram指定查詢序列
df.loc['2018-01-02':'2018-01-05', ['c1','c2']]
df.iloc[1:4, [0, 1]]
DataFram也適用以上loc及iloc語法

#Data特有功能序列沒有的
df['c3']->找出某欄可以不要用loc
df.cumsum(axis=1)->axis=1表示橫的相加
df.drop('c1',axis=1 )

##練習算簡單股票
account=100000
stockprice=35
buyamount=1
feeratio=1.425/1000
taxratio=3/1000

stockvalue= stockprice*buyamount*1000

account=account-stockvalue - (stockvalue *feeratio)

stockpricenew= stockprice*1.3*buyamount


stockvalue= stockpricenew*buyamount*1000

account=account+stockvalue - stockvalue*(taxratio+feeratio)

#練習畫人生曲線圖
import pandas as pd
import random
%matplotlib inline
def asset_prediction(起始資金 ,起始年紀,
    每月薪水 ,
    每月開銷 ,
    每月房租 ,
    退休年齡 ,
    投資部位,
    投資年利率,
    買房價格,
    買房頭期款,
    買房年紀,
    房貸利率,
    貸款年數,):

    預測時段 = range(起始年紀, 100)
    每年淨額 = pd.Series(0, index=預測時段)
    每年淨額.iloc[0] = 起始資金
    每年淨額.loc[:退休年齡] += 每月薪水 * 12
    每年淨額 -= (每月開銷 + 每月房租) * 12


    #新增
    每年淨額父母房子 = pd.Series(0, index=預測時段)
    每年淨額父母房子.iloc[0] = 起始資金
    每年淨額父母房子.loc[:退休年齡] += 每月薪水 * 12
    每年淨額父母房子 -= 每月開銷 * 12

    def compound_interest(arr, ratio, return_rate):
        ret = [arr.iloc[0]]
        for v in arr[1:]:
            ret.append(ret[-1] * ratio * (return_rate/100 + 1) + ret[-1] * (1 - ratio) + v)
        return pd.Series(ret, 預測時段)

    買房花費 = pd.Series(0, index=預測時段)
    買房花費[買房年紀] = 買房頭期款
    買房花費.loc[買房年紀:買房年紀+貸款年數-1] += (買房價格 - 買房頭期款) / 貸款年數

    欠款 = pd.Series(0, index=預測時段)
    欠款[買房年紀] = 買房價格
    欠款 = 欠款.cumsum()
    欠款 = 欠款 - 買房花費.cumsum()
    利息 = 欠款.shift().fillna(0) * 房貸利率 / 100


    房租年繳 = pd.Series(每月房租*12, index=預測時段)
    房租年繳.loc[買房年紀:] = 0

    每年淨額_買房 = pd.Series(0, index=預測時段)
    每年淨額_買房.iloc[0] = 起始資金
    每年淨額_買房.loc[:退休年齡] += 每月薪水 * 12
    每年淨額_買房 -= (每月開銷*12 + 房租年繳 + 利息 + 買房花費)




    pd.DataFrame({
        'no invest, no house': 每年淨額.cumsum(),
        'invest, no house': compound_interest(每年淨額, 投資部位, 投資年利率),
        'no invest, house': 每年淨額_買房.cumsum(),
        'invest, house': compound_interest(每年淨額_買房, 投資部位, 投資年利率),
        'no invest,family house': 每年淨額父母房子.cumsum(),
        'invest,family house': compound_interest(每年淨額父母房子, 投資部位, 投資年利率),
    }).plot()


    import matplotlib.pylab as plt
    plt.ylim(0, None)

    print('月繳房貸', (買房價格 - 買房頭期款) / 貸款年數 / 12)
    print('利息', 利息.sum() / 貸款年數)
    print('')

import ipywidgets as widgets
widgets.interact(asset_prediction,
    起始資金=widgets.FloatSlider(min=0, max=100, step=10, value=30),
    起始年紀=widgets.IntSlider(min=0, max=100, step=1, value=24),
    每月薪水=widgets.FloatSlider(min=0, max=20, step=0.1, value=4.5),
    每月開銷=widgets.FloatSlider(min=0, max=20, step=0.1, value=1.5),
    每月房租=widgets.FloatSlider(min=0, max=20, step=0.1, value=0.75),
    退休年齡=widgets.IntSlider(min=0, max=100, step=1, value=75),
    投資部位=widgets.FloatSlider(min=0, max=1, step=0.1, value=0.3),
    投資年利率=widgets.FloatSlider(min=0, max=20, step=0.5, value=5),
    買房價格=widgets.IntSlider(min=100, max=2000, step=50, value=1000),
    買房頭期款=widgets.IntSlider(min=100, max=2000, step=50, value=100),
    買房年紀=widgets.IntSlider(min=20, max=100, step=1, value=35),
    房貸利率=widgets.FloatSlider(min=1, max=5, step=0.1, value=2.4),
    貸款年數=widgets.IntSlider(min=0, max=40, step=1, value=20)
)
