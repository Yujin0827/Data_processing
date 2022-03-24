# -*- coding: utf-8 -*-
'''

>>> 폴더 내 여러 환자의 데이터 -> 각 tsv로 정리 

>>> meta_dict data => left, right로 분리
>>> Impulse number 추가

'''

import csv
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import parse
import pandas as pd
import os

def get_columns(input_path, patient_id, patient_uid):

    is_catch_up_saccade_analysis = False
    is_impulse = False

    meta_dict = {}
    impulse_dict = {}

    columns = []
    col_max = 0
    
    
    with open(input_path, 'r', encoding='UTF-8') as fin:
        for line in fin:
            tokens = line.split(',')
            

            if 'Patient Name:' in line:
                patient_name = ' '.join(tokens[1:])
                
                
            elif 'Test Date' in line:
                is_catch_up_saccade_analysis = False
                is_impulse = False

                meta_dict = {}
                impulse_dict = {}

                key = tokens[0].strip()
                value = tokens[1].strip()

                meta_dict['Patient Name'] = patient_name
                meta_dict['Patient ID'] = patient_id
                meta_dict['Patient UID'] = patient_uid
                meta_dict[key] = value


            elif 'Test Type' in line:
                key = tokens[0].strip()
                value = tokens[1].strip()

                meta_dict[key] = value


            elif 'Impulse' in line:
                if len(impulse_dict.keys()) != 0:
                    meta_dict_keys = [meta_key.strip() for meta_key in meta_dict.keys()]
                    meta_dict_keys.remove('')
                    
                    for impulse_key, impulse_value in impulse_dict.items():
                        impulse_dict_keys = []
                        for impulse_dict_key in impulse_value.keys():
                            impulse_dict_keys.append(impulse_dict_key.strip())
                    
                    column_candidates = meta_dict_keys + ['Trial Number'] + impulse_dict_keys
                    
                    if len(column_candidates) > col_max:
                        columns = []
                        columns.append(column_candidates)
                        col_max = len(column_candidates)
                        
                is_impulse = True
                is_catch_up_saccade_analysis = False

                impulse_key = tokens[0]
                value_list_key = tokens[1]
                value_list_value = tokens[2]

                impulse_dict[impulse_key] = {}
                impulse_dict[impulse_key][value_list_key] = value_list_value


            else:
                if 'Catch-up Saccade Analysis' in line:
                    is_catch_up_saccade_analysis = True


                if len(tokens) == 1:
                    continue


                if is_catch_up_saccade_analysis:
                    if tokens[1] and tokens[2]:
                        key = tokens[1].strip() + ' ' + tokens[2].strip()
                        s_group = tokens[1].strip()

                    elif tokens[2]:
                        key = s_group + ' ' + tokens[2].strip()

                    else:
                        key = tokens[0].strip() + tokens[1].strip()

                    value_left = tokens[-2].strip()
                    value_right = tokens[-1].strip()
                    value = (value_left, value_right)

                    if key.strip():
                        meta_dict[key + '-left'] = value_left
                        meta_dict[key + '-right'] = value_right

                    else:
                        meta_dict[key] = value

                elif is_impulse:
                    key = tokens[1].strip()

                    if len(tokens) == 3:
                        value = tokens[2].strip()

                    else:
                        value = tokens[2:]

                    impulse_dict[impulse_key][key] = value

                else:
                    key = tokens[0].strip()
                    value = tokens[1].strip()

                    meta_dict[key] = value

        for col in columns:
            return col

        return []

def parse_csv(file):
    if '.xml' in file:
        xml_path = os.path.join(path, file).replace('\\', '/')
        input_path = xml_path.strip('.xml') + '.csv'
        result_path = path.replace('vHIT', 'vHIT_Result') + '/' + file.strip('.xml') + '.tsv'
        result_dir = os.path.dirname(result_path)
        
        if not os.path.exists(result_dir):
            os.makedirs(result_dir)
            
        
        is_catch_up_saccade_analysis = False
        is_impulse = False
        
        meta_dict = {}
        impulse_dict = {}
        all_dict = {}
        all_dict_list = []
        
        s_group = ''
        impulse_key = ''
        impulse_num = 1
        
        
        xml_doc = ET.parse(xml_path)
        root = xml_doc.getroot()
        
        ics_patient = root.findall("{http://tempuri.org/PMRExportDataSet.xsd}ICSPatient")
        patient_id = [x.findtext("{http://tempuri.org/PMRExportDataSet.xsd}PatientID") for x in ics_patient][0]
        patient_uid = [x.findtext("{http://tempuri.org/PMRExportDataSet.xsd}PatientUID") for x in ics_patient][0]
        patient_name = ""
        
        columns = get_columns(input_path, patient_id, patient_uid)
        # print("\t".join(columns))
        
        
        with open(input_path, 'r', encoding='UTF-8') as fin:
            for line in fin:
                line = line.strip()
                
                tokens = line.split(',')
                
                
                if 'Patient Name:' in line:
                    patient_name = ' '.join(tokens[1:]).strip()
                    
                    
                elif 'Test Date' in line:
                    if len(meta_dict) != 0:
                        for col in columns:
                            if col in meta_dict:
                                # print(meta_dict[col], end='\t')
                                all_dict[col] = meta_dict[col]
        
                            for impulse_key, impulse_value in impulse_dict.items():
                                for impulse_value_key, impulse_value_value in impulse_value.items():
                                    if col in impulse_value_key:
                                        # print(impulse_value_value, end='\t')
                                        all_dict[col] = impulse_value_value
                        # print()
                        all_dict_list.append(all_dict)
        
                    is_catch_up_saccade_analysis = False
                    is_impulse = False
        
                    meta_dict = {}
                    impulse_dict = {}
                    all_dict = {}
                    impulse_num = 1
        
                    key = tokens[0].strip()
                    value = tokens[1].strip()
        
                    meta_dict['Patient Name'] = patient_name
                    meta_dict['Patient ID'] = patient_id
                    meta_dict['Patient UID'] = patient_uid
                    meta_dict[key] = value
                    
                    
                elif 'Test Type' in line:
                    key = tokens[0].strip()
                    value = tokens[1].strip()
        
                    meta_dict[key] = value
                    
                    
                elif 'Impulse' in line:
                    if len(impulse_dict.keys()) != 0:
                        for col in columns:
                            if col in meta_dict:
                                # print(meta_dict[col], end='\t')
                                all_dict[col] = meta_dict[col]
        
                            for impulse_key, impulse_value in impulse_dict.items():
                                for impulse_value_key, impulse_value_value in impulse_value.items():
                                    if col in impulse_value_key:
                                        # print(impulse_value_value, end='\t')
                                        all_dict[col] = impulse_value_value
                        # print()
                        impulse_num = impulse_num + 1
                        all_dict_list.append(all_dict)
                        
                    impulse_dict = {}
                    all_dict = {}
                    
                    is_impulse = True
                    is_catch_up_saccade_analysis = False
                    
                    impulse_key = tokens[0].strip()
                    value_list_key = tokens[1].strip()
                    value_list_value = tokens[2].strip()
                    
                    impulse_dict[impulse_key] = {}
                    impulse_dict[impulse_key][value_list_key] = value_list_value
                    
                    meta_dict['Trial Number'] = str(impulse_num)
                    impulse_dict[impulse_key] = {}
                    impulse_dict[impulse_key][value_list_key] = value_list_value
                    
                    
                else:
                    if 'Catch-up Saccade Analysis' in line:
                        is_catch_up_saccade_analysis = True
                        
                    if len(tokens) == 1:
                        continue
                        
                    if is_catch_up_saccade_analysis:
                        if tokens[1] and tokens[2]:
                            key = tokens[1].strip() + ' ' + tokens[2].strip()
                            s_group = tokens[1].strip()
                            
                        elif tokens[2]:
                            key = s_group + ' ' + tokens[2].strip()
                            
                        else:
                            key = tokens[0].strip() + tokens[1].strip()
                            
                        value_left = tokens[-2].strip()
                        value_right = tokens[-1].strip()
                        value = (value_left, value_right)
                        
                        if key.strip():
                            meta_dict[key + '-left'] = value_left
                            meta_dict[key + '-right'] = value_right
                            
                        else:
                            meta_dict[key] = value
                            
                    elif is_impulse:
                        key = tokens[1].strip()
        
                        if len(tokens) == 3:
                            value = tokens[2].strip()
        
                        else:
                            value = tokens[2:]
        
                        impulse_dict[impulse_key][key] = value
        
                    else:
                        key = tokens[0].strip()
                        value = tokens[1].strip()
        
                        meta_dict[key] = value
        
        
        with open(result_path, 'w', encoding='UTF-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=columns, delimiter='\t')
            writer.writeheader()
            
            writer.writerows(all_dict_list)


if __name__ == '__main__':
    file_path = 'D:/vHIT/'
    
    for path, dir, files in os.walk(file_path):
        for file in files:
            try:
                parse_csv(file)
                
            except UnicodeDecodeError:
                print(file)
                
            except FileNotFoundError:
                print(file)