'''

1. 한 파일을 읽어서 한 줄씩 출력하는 코드를 일단 작성
2. 환자 이름과 날짜시간을 추출하여 파일에 저장하는 부분 일단 작성
3. 수치값에 대해서 저장하는 코드 작성
4. 2와 3에서 얻은 환자이름, 날짜시간, 수치값 한 trial이 한 줄에 저장되도록 코드 수정

'''

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import parse


if __name__ == '__main__':    
    input_path = 'D:/vHIT/ahn ,hyo joon_200555967/ahn _hyo joon_2020_12_24_14_45_43.csv'
    xml_path = 'D:/vHIT/ahn ,hyo joon_200555967/ahn _hyo joon_2020_12_24_14_45_43.xml'
    
    print(input_path)
    
    is_catch_up_saccade_analysis = False
    is_impulse = False
    
    meta_dict = {}
    impulse_dict = {}
    
    impulse_key = ''
    
    
    xml_doc = ET.parse(xml_path)
    root = xml_doc.getroot()
    
    ics_patient = root.findall("{http://tempuri.org/PMRExportDataSet.xsd}ICSPatient")
    patient_uid = [x.findtext("{http://tempuri.org/PMRExportDataSet.xsd}PatientUID") for x in ics_patient]
    patient_id = [x.findtext("{http://tempuri.org/PMRExportDataSet.xsd}PatientID") for x in ics_patient]
    
    
    with open(input_path, 'r', encoding='UTF8') as fin:
        for line in fin:
            
            tokens = line.split(',')
            
            if 'Patient Name:' in line:
                key = tokens[0].strip()
                value = ' '.join(tokens[1:])
                
                meta_dict[key] = value
                meta_dict['patient UID'] = patient_uid[0]
                meta_dict['patient ID'] = patient_id[0]
                
                
            elif 'Test Date' in line:
                print()
                for key, value in meta_dict.items():
                    print(key, value)
                
                for impulse_key, impulse_value in impulse_dict.items():
                    print()
                    print(impulse_key)
                
                    for key, value in meta_dict.items():
                        print(key, value)
                
                    print()
                    for key, value in impulse_value.items():
                        print(key, value)
                
                is_catch_up_saccade_analysis = False
                is_impulse = False
                
                meta_dict = {}
                impulse_dict = {}
                
                key = tokens[0].strip()
                value = tokens[1].strip()
                
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
                    if len(tokens) == 5:
                        key = ' '.join(tokens[:3])
                        
                    else:
                        key = tokens[0].strip() + tokens[1].strip()
        
                    value_left = tokens[-2].strip()
                    value_right = tokens[-1].strip()
                    value = (value_left, value_right)
                    
                    meta_dict[key] = value

                elif is_impulse:
                    key = tokens[1].strip()
                    value = tokens[2:]
                    
                    impulse_dict[impulse_key][key] = value
                    
                else:
                    key = tokens[0].strip()
                    value = tokens[1].strip()
                    
                    meta_dict[key] = value
                
                
        print()
        for key, value in meta_dict.items():
            print(key, value)
        
        for impulse_key, impulse_value in impulse_dict.items():
            print()
            print(impulse_key)
        
            for key, value in meta_dict.items():
                print(key, value)
        
            print()        
            for key, value in impulse_value.items():
                print(key, value)
        
