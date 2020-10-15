from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime,timedelta
import time

def get_folder():
    path = input("Initiating.. (동작 없을 시 엔터 입력)")
    path = input("로그 파일들이 저장된 폴더 위치를 입력하세요.(저장도 같은 위치에 수행됩니다.)")
    path = path.__str__().split('\\')
    path = '/'.join(path)
    return Path(path)

def get_file_names(path):
    path = path.__str__().split('\\')
    path = '/'.join(path)
    data_dir = Path(path)
    files = data_dir.glob('*.txt')
    raw_norminal_var = list(files)
    return raw_norminal_var

def make_dataset(f):
    col_test = []

    print(f"{f} is in process.")
    with open(f, encoding="utf16", errors='ignore') as f:
        contents = f.read()
    contents = contents.split("\n")

    q_1 = []
    q_2 = []
    for i in range(1,len(contents)-1):
        q_1.append(contents[i].split(']')[0][1:])
        q_2.append((']'.join(contents[i].split(']')[1:])[1:]))


    df = pd.DataFrame(data=np.transpose([q_1,q_2]))
    #return df

    df = make_new_log_name(df.copy())
    df.columns = ['Time','New Name']

    merged = df.join(motions[['New Name','Key','Start/End','Unnamed: 4']].set_index('New Name'), on='New Name')
    merged.columns=['Time','Name','Key','Start/End','Code']
    return merged

def read_motions():
    path = input("Initiating.. (동작 없을 시 엔터 입력)")
    path = input("사전 정의 파일 위치를 슬래시('/'  역슬래시,원표시\ 아님!)를 활용하여 파일명까지 정확히 입력하세요. \n(예시: K:/DualAA_motions.csv)\n")
    while True:
        try:
            m = pd.read_csv(path,engine='c')
            break
        except UnicodeDecodeError:
            m = pd.read_csv(path,engine='python')
            break
    return m


def make_new_motions_name(m):
    q_name =[]
    for i in range(0,len(m)):
        key = m.iloc[i]['Key']
        k = m.iloc[i]['Start/End']
        if ('LaserStep:' in m[(m['Key']==key) & (m['Start/End']==k)]['Name'].tolist()[0]):
            ind = m[(m['Key']==key) & (m['Start/End']==k)]['Name'].tolist()[0].index('LaserStep') + 11
            q_name.append(m[(m['Key']==key) & (m['Start/End']==k)]['Name'].tolist()[0][:ind])
        else:
            q_name.append(m.Name[i])
    
    m['New Name'] = q_name
    return m

def get_changeable_names(m):
    q=[]
    for i in range(0,len(m)):
        key = m.iloc[i]['Key']
        k = m.iloc[i]['Start/End']
        if ('LaserStep:' in m[(m['Key']==key) & (m['Start/End']==k)]['Name'].tolist()[0]):
            ind = m[(m['Key']==key) & (m['Start/End']==k)]['Name'].tolist()[0].index('LaserStep') + 11
            q.append(m[(m['Key']==key) & (m['Start/End']==k)]['Name'].tolist()[0][:ind])
    names = q
    return names

def make_new_log_name(df):
    #names = get_changeable_names(motions)

    q_name =[]
    for _ in df[1]:
        if'LaserStep:' in _:
            ind = _.index('LaserStep') + 11
            q_name.append(_[:ind])
        else:
            q_name.append(_)
    df[2] = q_name
    
    q = []
    i=0
    for _ in df[2]:
        if _ in motions['New Name'].tolist():
            q.append(i)
        i += 1
        
    df_new = df.iloc[q][[0,2]]
    return df_new

def len_max(): 
    len_max = 0
    for i in merged['Key'].unique():
        off = merged[(merged['Key'] == i) & (merged['Start/End'] == 0)].index.tolist()
        if len(off) > len_max:
            len_max = len(off)
        mid = merged[(merged['Key'] == i) & (merged['Start/End'] == 1)].index.tolist()
        if len(mid) > len_max:
            len_max = len(mid)
        on = merged[(merged['Key'] == i) & (merged['Start/End'] == 2)].index.tolist()
        if len(on) > len_max:
            len_max = len(on)
    print(len_max)
    return len_max

def get_time_delta(merged):
        
    init_list = [None]*len_max()
    init_list_1 = [0]*len_max()
    delta_off = pd.DataFrame(columns = merged['Key'].unique())
    delta_off[1] = init_list.copy()
    delta_mid = pd.DataFrame(columns = merged['Key'].unique())
    delta_on = pd.DataFrame(columns = merged['Key'].unique())

    for i in merged['Key'].unique(): 
        q_off = init_list_1.copy()
        q_mid = init_list_1.copy()
        q_on = init_list_1.copy()
        if len(set(merged[merged['Key'] == i]['Start/End'])) is 2:
            off = merged[(merged['Key'] == i) & (merged['Start/End'] == 0)].index.tolist() # off 시점 추출
            on = merged[(merged['Key'] == i) & (merged['Start/End'] == 1)].index.tolist() # off 시점 추출
            for j in range(0,len(off)):
                if j ==0:
                    positions = []
                    for _ in on:
                        if _ <= off[j]:
                            positions.append(_)
                    if len(positions) is 0:
                        continue
                    pos_on = min(positions) #on 값
                else:
                    positions = []
                    for _ in on:
                        if (_ <= off[j])&(off[j-1]<_):
                            positions.append(_)
                    if len(positions) is 0:
                        continue
                    pos_on = min(positions)
                q_on[j]=(pos_on)
                q_off[j]=(off[j])
        else:
            
            off = merged[(merged['Key'] == i) & (merged['Start/End'] == 0)].index.tolist()
            mid = merged[(merged['Key'] == i) & (merged['Start/End'] == 1)].index.tolist()
            on = merged[(merged['Key'] == i) & (merged['Start/End'] == 2)].index.tolist()
            for j in range(0,len(off)):            
                if j ==0:
                    positions= []
                    for _ in mid:
                        if (_ <= off[j]):
                            positions.append(_)
                    if len(positions) is 0:
                        continue
                    pos_mid = min(positions) #mid 값

                    positions = []
                    for _ in on:
                        if (_ <= mid[j]):
                            positions.append(_)
                    if len(positions) is 0:
                        continue
                    pos_on = min(positions) #on 값
                else:
                    positions = []
                    for _ in mid:
                        if (_ <= off[j])&(off[j-1]<_):
                            positions.append(_)
                    if len(positions) is 0:
                        continue
                    pos_mid = min(positions)
                    
                    positions = []
                    for _ in on:
                        if (_ <= mid[j])&(mid[j-1]<_):
                            positions.append(_)
                    if len(positions) is 0:
                        continue
                    pos_on = min(positions)
                q_on[j]=(pos_on)
                q_mid[j]=(pos_mid)
                q_off[j]=(off[j])
        delta_off[i] = q_off
        delta_mid[i] = q_mid
        delta_on[i] = q_on
    return delta_off, delta_mid, delta_on

def get_mid_motions(merged):
    #2,1,0 Key 값
    q_3motions=[]
    for i in merged['Key'].unique(): 
        if len(set(merged[merged['Key'] == i]['Start/End'])) is 3:
            q_3motions.append(i)
    return q_3motions

def get_motion_times(merged, delta_off, delta_mid, delta_on, path, log):

    q_3motions = get_mid_motions(merged)
    df = pd.DataFrame()
    ind = 0
    for key in merged['Key'].unique(): #key
        print(f"Code {key} is in process.")
        t_off=[]
        t_mid=[]
        t_on=[]


        if key in q_3motions:
            if len(delta_off[key][delta_off[key] > 0]) *  len(delta_on[key][delta_on[key] > 0]) * len(delta_mid[key][delta_mid[key] > 0]) is 0:
                 continue 
            else:
                for i in delta_off[key][delta_off[key]>0]:
                    t_off_str = merged.Time[i]
                    t_off.append(datetime.strptime(t_off_str, '%H:%M:%S.%f'))

                for i in delta_mid[key][delta_mid[key]>0]:
                    t_mid_str = merged.Time[i]
                    t_mid.append(datetime.strptime(t_mid_str, '%H:%M:%S.%f'))

                for i in delta_on[key][delta_on[key]>0]:
                    t_on_str = merged.Time[i]
                    t_on.append(datetime.strptime(t_on_str, '%H:%M:%S.%f'))

                result =[None]*(len_max()+3)
                result[0] = motions[(motions['Key'] == key) & (motions['Start/End'] == 0)]['Name'].tolist()[0]
                result[1] = motions[(motions['Key'] == key) & (motions['Start/End'] == 1)]['Name'].tolist()[0]
                #off ~ mid
                for j in range(3,len(t_off)):
                    t_delta = t_off[j] - t_mid[j]
                    result[j] = t_delta.seconds + t_delta.microseconds/1000000
                result[2] = np.mean(result[3:(len(t_off)-1)])
                df[ind] = result
                ind += 1


                #mid ~ on
                result =[None]*(len_max()+3)
                result[0] = motions[(motions['Key'] == key) & (motions['Start/End'] == 0)]['Name'].tolist()[0]
                result[1] = motions[(motions['Key'] == key) & (motions['Start/End'] == 1)]['Name'].tolist()[0]
                for j in range(3,len(t_off)):
                    t_delta = t_off[j] - t_mid[j]
                    result[j] = t_delta.seconds + t_delta.microseconds/1000000
                result[2] = np.mean(result[3:(len(t_off)-1)])

                df[ind] = result
                ind += 1
            

        else:
            if len(delta_off[key][delta_off[key] > 0]) *  len(delta_on[key][delta_on[key] > 0])  is 0:
                continue 
            else:
                    
                for i in delta_off[key][delta_off[key]>0]:
                    t_off_str = merged.Time[i]
                    t_off.append(datetime.strptime(t_off_str, '%H:%M:%S.%f'))

                for i in delta_on[key][delta_on[key]>0]:
                    t_on_str = merged.Time[i]
                    t_on.append(datetime.strptime(t_on_str, '%H:%M:%S.%f'))
                
                result =[None]*(len_max()+3)
                result[0] = motions[(motions['Key'] == key) & (motions['Start/End'] == 0)]['Name'].tolist()[0]
                result[1] = motions[(motions['Key'] == key) & (motions['Start/End'] == 1)]['Name'].tolist()[0]
                #off ~ mid
                for j in range(3,len(t_off)):
                    t_delta = t_off[j] - t_on[j]
                    result[j] = t_delta.seconds + t_delta.microseconds/1000000
                result[2] = np.mean(result[3:(len(t_off)-1)])
                df[ind] = result
                ind += 1
    file = '/'.join(path.__str__().split('\\'))+'/'+log.__str__().split(".")[-2].split('\\')[-1]+'_result.csv'

    df.to_csv(file, encoding='utf-8-sig')
    print(f"Result is saved at {file}.")
    print(f"{log} is completed.")

###### Main Code ######
motions = read_motions()
motions = make_new_motions_name(motions.copy())

folder_path = get_folder()
files = get_file_names(folder_path)
for log in files:
    merged = make_dataset(log)
    delta_off, delta_mid, delta_on = get_time_delta(merged)
    get_motion_times(merged,delta_off, delta_mid, delta_on,folder_path,log)
