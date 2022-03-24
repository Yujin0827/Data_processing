# -*- coding: utf-8 -*-

'''

>>> 폴더 내 여러 환자의 데이터 -> 하나의 tsv로 정리 

'''

import csv
import os
import glob
import pandas as pd
from collections import OrderedDict

if __name__ == '__main__':
    file_path = 'D:/vHIT_Result'
    file_list = []
    
    result_path = file_path + '/result_tsv.tsv'
    # result_dir = os.path.dirname(result_path)
    #
    # if not os.path.exists(result_dir):
    #     os.makedirs(result_dir)
    
    columns = OrderedDict()
    
    for path, dir, files in os.walk(file_path):
        for file in files:
            if '.tsv' in file:
                try:
                    tsv_path = os.path.join(path, file).replace('\\', '/')
                    df = pd.read_csv(tsv_path, sep='\t')
                    
                    for col in df.columns:
                        columns[col] = ' '
                except:
                    print(file)
                
    print(columns.keys())
    
    for path, dir, files in os.walk(file_path):
        for file in files:
            if '.tsv' in file:
                try:
                    tsv_path = os.path.join(path, file).replace('\\', '/')
                    df = pd.read_csv(tsv_path, sep='\t')
                    for col in columns:
                        if col in df.columns:
                            df[col] = ' '
    
    
    # df_from_each_file = (pd.read_csv(f, sep='\t') for f in file_list)
    # df_merged = pd.concat(df_from_each_file, axis=0, ignore_index=True)
    
    # df_merged.to_csv("merged.csv")
    
    for group, df_group in df_merged.groupby(by=["Patient ID", "Test Date"]):
        for test_type, df_test_type in df_group.groupby("Test Type"):
            df_test_type["Gain Type"] = df_test_type.apply(lambda row: get_gain_type(row), axis=1)
            df_test_type["Saccade Type"] = df_test_type["Overt Saccade"]
            
    
    # combined_tsv = pd.concat([pd.read_csv(f) for f in file_list])
    #
    # combined_tsv.to_csv("combined_tsv.tsv", index=False, encoding='utf-8')
    

    # all_col = []
    
    # for f in file_list:
    #     each_tsv = pd.read_csv(f, sep='\t')
    #     ['file'] = f.split('/')[-1]
    #     all_col.append(each_tsv)
    #
    # merged_tsv = pd.concat(all_col, ignore_index=True, sort=True)
    
    # merged_tsv.to_csv(result_path)
    
    # tsv_from_each_file = (pd.read_csv(f, sep='\t') for f in file_list)
    # result_tsv = pd.concat(tsv_from_each_file, ignore_index=True)
    #
    # result_tsv.to_csv(result_path)
    
    