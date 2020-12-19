import os

def changeName(path):
    i=1
    for filename in os.listdir(path):
        #new_file_path = path+'/'+str(i)
        old_file_path = path+'/'+filename
        #os.rename(old_file_path,new_file_path)
        #print('changed '+old_file_path,"=>",new_file_path)
        print('changed '+old_file_path)
        i+=1

changeName('C:\Users\shinborah\Desktop\stock data/KOSPI200')