
#用reuuest模擬瀏覽器跟遠端server溝通(使用於80%網站，若下載不完整可能用了javascript套
件改用se)
import requests
res = requests.get('http://www.wibibi.com/info.php?tid=116')

#文字檔顯示
res.text

#如果文字有中文要轉碼，中文常用'utf-8'  'big5'
res.encoding = 'utf-8' # 'big5'
res.text
-----------------------
#方法1:建立一個html檔案並將下載的檔案放入至html檔中，完成後關閉寫入動作
f = open('test.html', 'w', encoding='utf-8')
f.write(res.text)
f.close()

#使用panda讀取html檔並轉成datafram
import pandas as pd
dfs = pd.read_html('test.html')
----------------------
# 方法2:不存檔直接轉成DataFrame
#把res.text存到io(記憶體中)再由panda讀取

from io import StringIO

dfs = pd.read_html(StringIO(res.text))
dfs[3]


#爬收股價資訊

先至要爬收網站右鍵->檢查->選擇network找尋第一個request並且檢查response是否為想要的資訊
將「第一個request」url複製貼至瀏覽器中可以看到是json檔的文字，將json換成csv試試能否使用
，可以的話執行以下語法
import requests
response = requests.get('http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=20180309&type=ALLBUT0999&_=1520785530355')

#檢查前100字是否有抓取
response.text[:100]

#將文字依分隔符號切格，html中「\n」為換行符號
lines = response.text.split('\n')
lines[100]



# 過濾要的資料

newlines = []

for line in lines:
    # 用「",」切開每一行，看是否被切成17個
    if len(line.split('",')) == 17:

        # 將 line 加到新的 newlines 中
        newlines.append(line)
#newlines[2]
print('原本的行數（lines）')
print(len(lines))
print('刪除不需要的行數後，變少了(newlines)')
print(len(newlines))

# 先創造一個字元c(換行符)
c = '\n'
# 利用此字元c，將每一行給連在一起
s = c.join(newlines)
# 將 s 裡面的 等號 刪除
s = s.replace('=', '')

# 將 s 用StringIO變成檔案，並用 pd.read_csv 來讀取檔案
df = pd.read_csv(StringIO(s))

# 顯示前五個
df.head()


# 將所有df中的元素都變成字串，並將字串中的逗號「,」刪除
df = df.astype(str)
#方法一 建立函式
#def func(s):
#    return s.str.replace(',','')
#df=df.apply(func)
#方法二 lambda左邊放input右邊放ouput
df = df.apply(lambda s: s.replace(',', ''))

# 將 df 證券代號變成 index
#df = df.set_index('證券代號')

# 將 df 中的元素從字串變成數字，若無法轉換傳回NaN
df = df.apply(lambda s: pd.to_numeric(s, errors='coerce'))

# 要刪除沒有用的columns
#方法1 取出每一條序列Na數量與總數不同的序列
#df = df[df.columns[df.isnull().sum() != len(df)]]
#df
#方法2 其中 axis=1 為是說每條columns去檢查有沒有NaN
# how='all' 是說假如全部都是 NaN 則刪除該 column
df.dropna(axis=1, how='all', inplace=True)

df.head()
