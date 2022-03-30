# -*- coding: utf-8 -*-

'''

>>> Gain Type, Saccade Type 추가

'''

import pandas as pd
import os

def get_gain(input_dir):
    df = pd.read_csv(input_dir, sep='\t')
    
    gains_type = []
    
    for index, row in df.iterrows():
        test_type = row['Test Type']
        gain = row['Gain']
        
        gain_type = "Normal"
        
        if test_type == 'Head Impulse Lateral':
            if gain < 0.8 or gain > 1.2:
                gain_type = "Abnormal"
        
        else:
            if gain < 0.75 or gain > 1.2:
                gain_type = "Abnormal"
                
        gains_type.append(gain_type)
        
    df['Gain Type'] = gains_type
    
    return df


def get_saccade(df):
    saccade_dict = {}
    
    for type, type_group in df.groupby('Test Type'):
        saccades_cnt = (type_group['Overt Saccades'] >= 1).sum()
        
        saccade_type = 'Normal'
        
        if saccades_cnt >= 3:
            saccade_type = 'Abnormal'
        
        saccade_dict[type] = saccade_type
    
    df['Saccade Type'] = df['Test Type'].apply(lambda x : saccade_dict[x])
    
    return df


def save_result(input_path, df):
    output_dir = 'D:/vHIT_Result/'
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_basename = os.path.basename(input_path)
    output_path = os.path.join(output_dir, output_basename).replace('\\', '/')
    
    df.to_csv(output_path, sep='\t')
    

if __name__ == '__main__':
    # pd.set_option('display.max_rows', None)
    # pd.set_option('display.max_columns', None)
    # pd.set_option('display.width', None)
    
    input_dir = 'D:/vHIT_Parsed/'

    for path, dir, files in os.walk(input_dir):
        for file in files:
            input_path = os.path.join(path, file).replace('\\', '/')
            
            try:
                df = get_gain(input_path)
                df = get_saccade(df)
                save_result(input_path, df)
                
            except:
                print(input_path)
    