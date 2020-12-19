import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import datetime as dt
import logging
import math
import keras
from keras.models import Sequential
from keras.layers import Dense, LSTM, Activation,MaxPooling1D, Conv1D,Flatten,Dropout
from keras import optimizers
from keras.models import load_model
import tensorflow as tf
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

# GPU 연결
device_name = tf.test.gpu_device_name()
if device_name != '/device:GPU:0':
  raise SystemError('GPU device not found')
print('Found GPU at: {}'.format(device_name))

# 전체 업종 코드 리스트 불러오기
data_path = '../stock_data/KOSPI200_5_minute_data/'
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
  df_list.append(df.loc['20201004':])  # 2020-10-04 이전의 데이터만 사용

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
  print(x.shape, y.shape)

seq_length = 231 # 77 * 3 (하루에 77개 데이터) * (3일)
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
valX = np.empty(shape = [0,seq_length,n_features])
valY = np.empty(shape = [0,1])

for dataX, dataY in zip(dataX_list, dataY_list):
  # train/validation 데이터 생성
  tmp_trainX, tmp_valX, tmp_trainY, tmp_valY = train_test_split(dataX, dataY, test_size=0.2, random_state=321)

  trainX_list.append(tmp_trainX)
  trainY_list.append(tmp_trainY)
  valX_list.append(tmp_valX)
  valY_list.append(tmp_valY)

  trainX = np.concatenate((trainX, tmp_trainX),axis = 0)
  trainY = np.concatenate((trainY, tmp_trainY),axis = 0)
  valX = np.concatenate((valX, tmp_valX),axis = 0)
  valY = np.concatenate((valY, tmp_valY),axis = 0)
  
print('final trainX shape: ', trainX.shape)
print('final trainY shape: ', trainY.shape)
print('final valX shape: ', valX.shape)
print('final valY shape: ', valY.shape)

with tf.device('/device:GPU:0'):
  ## LSTM 모델
  model = Sequential()
  model.add(Dense(128,input_shape = trainX[1].shape))
  model.add(Conv1D(input_shape = trainX[1].shape,filters=112,kernel_size=1,activation='relu'))
  model.add(MaxPooling1D(pool_size = 2))
  model.add(Conv1D(filters=64,kernel_size=1,activation='relu'))
  model.add(MaxPooling1D(pool_size = 1))
  model.add(LSTM(40,input_length=32, return_sequences=True, stateful=False))
  model.add(LSTM(40, return_sequences=True, stateful=False))
  model.add(LSTM(40, return_sequences=False, stateful=False))
  model.add(Dense(100))
  model.add(Dense(1,activation='relu'))

  # 모델 학습 설정 및 진행
  keras.optimizers.Adam(lr=0.01, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
  model.compile(loss='mean_squared_error', optimizer='adam')
  model.summary()
  print("="*50)
  hist = model.fit(trainX, trainY, epochs=50, batch_size=30, verbose=1, validation_data=(valX, valY))

# 학습 과정 그래프
print(hist.history['loss'])
print(hist.history['val_loss'])
fig, loss_ax = plt.subplots()
acc_ax = loss_ax.twinx()
loss_ax.plot(hist.history['loss'], 'y', label='train loss')
loss_ax.plot(hist.history['val_loss'], 'r', label='val loss')
loss_ax.set_xlabel('epoch')
loss_ax.set_ylabel('loss')
loss_ax.legend(loc='upper left')
acc_ax.legend(loc='lower left')
plt.show()

# 모델 저장
model.save('models/initial_model_5minute_data.h5')