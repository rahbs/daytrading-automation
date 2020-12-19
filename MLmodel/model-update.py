import os
import pandas as pd
import numpy as np
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

'''
  model: model 파일 이름
  date: 추가하고자 하는 데이터 날짜

  '''
def update_model(model, date):
    # 전체 업종 코드 리스트 불러오기
    data_path = '../stock_data/KOSPI200_daily_data/'
    code_list = []
    file_list = os.listdir(data_path)
    for file in file_list:
        stock_code = file[:-4]
        code_list.append(stock_code)

    # 데이터 로드
    df_list = []
    for i,code in enumerate(code_list):
        df = pd.read_csv(data_path+code+'.csv', index_col=0, engine='python')
        df.index.name = 'date'
        df["code"]=i
        df_list.append(df.loc[date:][:120])

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

    ## 데이터셋 생성하기
    x_list = [] 
    y_list = []
    # 행은 그대로 두고 열을 우측에 붙여 합친다 
    for scaled_price_indicator, scaled_volume_indicator, df in zip(scaled_price_indicators,scaled_volume_indicators,df_list):
        # (가격 관련 지표 + 거래량 관련 지표)
        x = np.concatenate((scaled_price_indicator, scaled_volume_indicator), axis=1)  # axis=1
        # 종목 code 추가
        x = np.concatenate((x,df.loc[:,'code':'code'].values[:].astype(np.int)), axis=1)
        y = x[:, [1]]
        x_list.append(x)
        y_list.append(y) # 타켓은 주식 고가

    seq_length = 60
    n_features = 6

    dataX_list = []
    dataY_list = []
    for x, y in zip(x_list, y_list):
        # dataX와 dataY 생성 
        tmp_dataX = [] # Input - Sequence Data
        tmp_dataY = [] # Output(target)
        for i in range(0, int(len(y) - seq_length)): # len_data - seq_length
            _x = x[i : i + seq_length]
            _y = y[i + seq_length] # 다음날 고가(정답) 
            tmp_dataX.append(_x) # dataX 리스트에 추가
            tmp_dataY.append(_y) # dataY 리스트에 추가 
        dataX_list.append(tmp_dataX)
        dataY_list.append(tmp_dataY)

    trainX_list = []
    trainY_list = []
    valX_list = []
    valY_list = []
    trainX = np.empty(shape = [0,seq_length,n_features])
    trainY = np.empty(shape = [0,1])

    for dataX, dataY in zip(dataX_list, dataY_list):
        trainX_list.append(dataX)
        trainY_list.append(dataY)

        trainX = np.concatenate((trainX, dataX),axis = 0)
        trainY = np.concatenate((trainY, dataY),axis = 0)

    # 모델 추가 학습
    model = load_model('models/'+model)
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.summary()
    hist = model.fit(trainX, trainY, epochs=50, batch_size=30, verbose=1)
    model.save('models/daily_data_updated'+'_'+date+'.h5')

update_model('initial_model_daily_data.h5','20201006')