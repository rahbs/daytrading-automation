
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model

# date 다음 날의 n개의 추천 종목 코드 리스트 반환
def getRecommendedCodeList(date,n):    
    ## 데이터 로드
    data_path1 = '../stock_data/KOSPI200_daily_data/'
    data_path2 = '../stock_data/KOSPI200_5minute_data/'
    code_list = []
    file_list = os.listdir(data_path1)
    for file in file_list:
        stock_code = file[:-4]
        code_list.append(stock_code)

    df_list = []
    for i,code in enumerate(code_list):
        df = pd.read_csv(data_path1+code+'.csv', index_col=0, engine='python')
        df.index.name = 'date'
        df["code"]=i
        df_list.append(df.loc[date:][:60]) # 해당 날짜포함 60일간 데이터 불러오기

    data_len_arr = np.zeros(shape=(len(df_list)))
    for i, df in enumerate(df_list):
        data_len_arr[i]=len(df)

    ## 데이터 전처리 
    scaled_price_indicators = []
    scaled_volume_indicators = []
    for i, df in enumerate (df_list) :
        price_indicator = df.loc[:,'open':'close'].values[:].astype(np.float) # 가격 관련 지표 
        volume_indicator = df.loc[:,'volume':'volume'].values[:].astype(np.float) # 거래량 관련 지표 

    scaler = MinMaxScaler(feature_range=(0, 1)) # 0~1 값으로 스케일링
    scaled_price_indicators.append(scaler.fit_transform(price_indicator)) # 가격 관련 지표에 스케일링
    scaled_volume_indicators.append(scaler.fit_transform(volume_indicator)) # 거래량 관련 지표에 스케일링

    seq_length = 60
    n_features = 6

    ## 데이터셋 생성하기
    X =  np.empty(shape = [0,seq_length,n_features])
    for scaled_price_indicator, scaled_volume_indicator, df in zip(scaled_price_indicators,scaled_volume_indicators,df_list):
        # (가격 관련 지표 + 거래량 관련 지표)
        x = np.concatenate((scaled_price_indicator, scaled_volume_indicator), axis=1)  # axis=1
        # 종목 code 추가
        x = np.concatenate((x,df.loc[:,'code':'code'].values[:].astype(np.int)), axis=1)
        # y = x[:, [1]]
        x = np.expand_dims(x,axis=0)
        X = np.append(X, x, axis = 0)

    X_close = X[:,0,3] #해당 날짜의 종가

    ## 모델 로드
    model1 = load_model('models/initial_model_daily_data.h5')
    model2 = load_model('models/initial_model_5minute_data.h5')

    ## 예측
    y_pred1 = model1.predict(X, batch_size=200, verbose=1)
    y_pred2 = model2.predict(X, batch_size=200, verbose=1)

    # 두 모델의 결과 평균 이용
    y_pred = (y_pred1+y_pred2)/2
    y_pred = y_pred.squeeze()

    # 전날 종가 대비 상승률 높은 탑 n 종목코드 리스트 리턴
    rise = y_pred - X_close
    code_list = []
    
    for i in range(n):
        max_idx = rise.argmax()
        code_list.append(max_idx)
        rise = np.delete(rise,max_idx)

    return code_list

getRecommendedCodeList('20201005',10)