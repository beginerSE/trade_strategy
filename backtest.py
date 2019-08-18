import talib

def cal_backtest(price,mterm1=12,mterm2=26,mterm3=5,momterm=6):
    numpyprice=np.array(price)
    change=price.pct_change()
    hold_return=(change+1).cumprod()
    hold_return[0]=1
    hold_return=hold_return*10000
    momentam=talib.MOM(price,timeperiod=momterm)
    macd=talib.MACD(price,fastperiod=mterm1, slowperiod=mterm2,    signalperiod=mterm3)
    signal=[]
    for i in range(len(price)):
        if momentam[i]>0 and macd[2][i] >0:
            signal.append(1)
        elif momentam[i]<0 and macd[2][i]<0 :
            signal.append(-1)
        else:
            signal.append(0)
    ##累積リターンの計算##累積リターンの計算
    trade_returns=((change[1:]*signal[:-1])+1).cumprod()
    return trade_returns

 
# 試しにバックテスト関数を実行する
cal_backtest(price,mterm1=12,mterm2=26,mterm3=5,momterm=6)[-1]


# グリッドサーチ的な感じで最適場パラメーターを発見する
returns=[]
for i in range(2,21):
    for r in range(2,21):
        for e in range(5,26):
            for f in range(6,31):
                returns.append([cal_backtest(price,mterm1=i,mterm2=r,mterm3=int(e),momterm=int(f))[-1],i,r,e,f])
                print(returns[-1])

backtest_data = pd.DataFrame(returns)
backtest_data.columns=['returns','macd_short','macd_long','macd_diff','momentam']
