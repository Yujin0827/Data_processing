# -*- coding: utf-8 -*-

'''

>>> 환자 1명의 data => tsv로 정리

'''

import csv
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import parse


def get_columns(input_path):
    is_catch_up_saccade_analysis = False
    is_impulse = False
    
    meta_dict = {}
    impulse_dict = {}
        
    columns = []
    
    with open(input_path, 'r', encoding='UTF-8') as fin:
        for line in fin:
            
            tokens = line.split(',')
            
            if 'Patient Name:' in line:
                patient_name = ' '.join(tokens[1:])
            
            
            elif 'Test Date' in line:
                if len(meta_dict.keys()) != 0:
                    meta_dict_keys = [meta_key.strip() for meta_key in meta_dict.keys()]
                    meta_dict_keys.remove('')
                            
                    for impulse_key, impulse_value in impulse_dict.items():
                        impulse_dict_keys = []
                        for impulse_dict_key in impulse_value.keys():
                            impulse_dict_keys.append(impulse_dict_key.strip())
                    
                    column_candidates = meta_dict_keys + impulse_dict_keys
                    columns.append(column_candidates)
                
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
    

if __name__ == '__main__': 
    input_path = 'D:/vHIT/ahn ,hyo joon_200555967/ahn _hyo joon_2020_12_24_14_45_43.csv'
    xml_path = 'D:/vHIT/ahn ,hyo joon_200555967/ahn _hyo joon_2020_12_24_14_45_43.xml'
    
    
    is_catch_up_saccade_analysis = False
    is_impulse = False
    
    meta_dict = {}
    impulse_dict = {}
    all_dict = {}
    all_dict_list = []
    
    impulse_key = ''
    s_group = ''
    
    
    xml_doc = ET.parse(xml_path)
    root = xml_doc.getroot()
    
    ics_patient = root.findall("{http://tempuri.org/PMRExportDataSet.xsd}ICSPatient")
    patient_uid = [x.findtext("{http://tempuri.org/PMRExportDataSet.xsd}PatientUID") for x in ics_patient][0]
    patient_id = [x.findtext("{http://tempuri.org/PMRExportDataSet.xsd}PatientID") for x in ics_patient][0]
    patient_name = ""
    
    columns = get_columns(input_path)
    
    
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
                            all_dict[col] = meta_dict[col]
                        
                        for impulse_key, impulse_value in impulse_dict.items():
                            for impulse_value_key, impulse_value_value in impulse_value.items():
                                if col in impulse_value_key:
                                    all_dict[col] = impulse_value_value
                    all_dict_list.append(all_dict)
                
                is_catch_up_saccade_analysis = False
                is_impulse = False
                
                meta_dict = {}
                impulse_dict = {}
                all_dict = {}
                
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
                            all_dict[col] = meta_dict[col]
                            
                        for impulse_key, impulse_value in impulse_dict.items():
                            for impulse_value_key, impulse_value_value in impulse_value.items():
                                if col in impulse_value_key:
                                    all_dict[col] = impulse_value_value
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
                    
                    
    with open('D:/vhit/ahn ,hyo joon_200555967/Result_Ex_processing3.tsv', 'w', encoding='UTF-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns, delimiter='\t')
        writer.writeheader()
        
        writer.writerows(all_dict_list)
        