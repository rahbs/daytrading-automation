import creonAPI
import pandas as pd
import win32com
import pickle as pkl

with open('../stock_data/KOSPI200_code_name_dict.pkl','rb') as f:
    data = pkl.load(f)

g_objCodeMgr = win32com.client.Dispatch('CpUtil.CpCodeMgr')
# KOSPI 200 데이터
KOSPI200_codelist= g_objCodeMgr.GetGroupCodeList(180)

KOSPI200_df = pd.DataFrame(columns = ['code','name','industryCode','industryName'])
for code in KOSPI200_codelist:
    row = {}
    name = g_objCodeMgr.CodeToName(code)
    industryCode = g_objCodeMgr.GetStockIndustryCode(code)
    industryName = g_objCodeMgr.GetIndustryName(industryCode)
    row['code'] = code
    row['name'] = name
    row['industryCode'] = industryCode
    row['industryName'] = industryName
    KOSPI200_df = KOSPI200_df.append(row, ignore_index = True)

#print(KOSPI200_df)
# write pickle
#KOSPI200_df.to_pickle('../stock_data/KOSPI200_info_df.pkl')

# read pickle
df = pd.read_pickle("../stock_data/KOSPI200_info_df.pkl")
print(df)

# with open('KOSPI200_info_df.pkl','w') as f:
#     f.write(KOSPI200_df)
