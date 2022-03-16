'''

>>> 환자 1명의 data에 대한 processing

1. 조건 => token 개수로 분류하기

'''
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import parse
from pickle import TRUE
import pandas as pd


if __name__ == '__main__':
    input_path = 'D:/vHIT/ahn ,hyo joon_200555967/ahn _hyo joon_2020_12_24_14_45_43.csv'
    xml_path = 'D:/vHIT/ahn ,hyo joon_200555967/ahn _hyo joon_2020_12_24_14_45_43.xml'
    
    print(input_path)
    
    is_impulse = False
    
    meta_dict = {}
    impulse_dict = {}
    
    impulse_key = ''
    
    
    xml_doc = ET.parse(xml_path)
    root = xml_doc.getroot()
    
    ics_patient = root.findall("{http://tempuri.org/PMRExportDataSet.xsd}ICSPatient")
    patient_uid = [x.findtext("{http://tempuri.org/PMRExportDataSet.xsd}PatientUID") for x in ics_patient]
    patient_id = [x.findtext("{http://tempuri.org/PMRExportDataSet.xsd}PatientID") for x in ics_patient]
    
    
    with open(input_path, 'r', encoding='UTF-8') as fin:
        for line in fin:
            
            tokens = line.split(',')
            
            if 'Patient Name:' in line:
                key = tokens[0].strip()
                value = ' '.join(tokens[1:])
                
                meta_dict[key] = value
                meta_dict['patient UID'] = patient_uid[0]
                meta_dict['patient ID'] = patient_id[0]
            
            else:
                if 'Test Date' in line:
                    print()
                    for key, value in meta_dict.items():
                        print(key, value)
                    
                    for impulse_key, impulse_value in impulse_dict.items():
                        print()
                        print(impulse_key)
                        for key, value in impulse_value.items():
                            print(key, value)
                        
                    is_impulse = False
                    
                    meta_dict = {}
                    impulse_dict = {}
                    
                elif ('Impulse' in line) and (len(tokens) == 3):
                    is_impulse = True
                    
                    
                if len(tokens) == 1:
                    continue
                
                elif len(tokens) == 2:
                    key = tokens[0].strip()
                    value = tokens[1].strip()
                
                elif len(tokens) == 3:
                    if ('Impulse' in line) and (len(tokens) == 3):
                        another_type = False
                        is_impulse = True
                    
                        impulse_key = tokens[0]
                        key = tokens[1]
                        value = tokens[2]
                    
                        impulse_dict[impulse_key] = {}
                    
                    else:
                        key = tokens[1].strip()
                        value = tokens[2].strip()
                    
                elif len(tokens) == 4:
                    key = tokens[0].strip()
                    value = tokens[1].strip()
                
                elif len(tokens) == 5:
                    key = ' '.join(tokens[:3])
                    value_left = tokens[-2].strip()
                    value_right = tokens[-1].strip()
                    value = (value_left, value_right)
                
                elif len(tokens) >= 6:
                    key = tokens[1].strip()
                    value = tokens[2:]
                
                
                if is_impulse:
                    impulse_dict[impulse_key][key] = value
                    
                else:
                    meta_dict[key] = value
                
                
        print()
        for key, value in meta_dict.items():
            print(key, value)
        
        for impulse_key, impulse_value in impulse_dict.items():
            print()
            print(impulse_key)
            for key, value in impulse_value.items():
                print(key, value)
                