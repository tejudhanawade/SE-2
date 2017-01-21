#import sys
import json
import os
from pprint import pprint
from all_validation_fun import *
#file_name = sys.argv[1]

def parse_json(file_name):
    with open(file_name) as datafile:
         data = json.load(datafile)
         afile= open(file_name)
         file_size = len(afile.read())
         if file_size is False:
             return 0
         else:
             return data

def count_of_persons(data):
    length_data = len(data['persons'])
    return  length_data

#data = parse_json(file_name)
#print data

def phone_numbers_validation(phn_nums,lst):
    num_cnt = len(phn_nums)
    mb_lst=[]
    phn_lst = []
    #nums=[]
    bool_lst=[]
    for i in range(0,num_cnt):
        if(phn_nums[i].get('type')):
            if(phn_nums[i]['type']=='mobile'):
                bool_lst.append(valid_mb_number(phn_nums[i]['number']))
                mb_lst.append(phn_nums[i]['number'])
            else:
                bool_lst.append(valid_phn_number(phn_nums[i]['number']))
                phn_lst.append(phn_nums[i]['number'])
   # nums=map(lambda x,y:(x,y), phn_lst,mb_lst)
    #print 'valid Numers:',all(bool_lst)
    if(all(bool_lst)):
        lst.append(str(phn_lst))
        lst.append(str(mb_lst))
        return None #[phn_lst,mb_lst]
    else:
        return False

def address_validation(addr_record,addr):
    #addr=[]
    bool_lst=[]
    if(addr_record.get('streetAddress')):
        bool_lst.append(valid_street_add(addr_record['streetAddress']))
        addr.append(addr_record['streetAddress'])
    else:
        bool_lst.append[False]
    if(addr_record.get('city')):
        bool_lst.append(valid_city(addr_record['city']))
        addr.append(addr_record['city'])
    else:
        bool_lst.append(False)
    if(addr_record.get('state')):
        bool_lst.append(valid_state(addr_record['state']))
        addr.append(addr_record['state'])
    else:
        bool_lst.append(False)
    if(addr_record.get('postalCode')):
        bool_lst.append(valid_code(addr_record['postalCode']))
        addr.append(addr_record['postalCode'])
    else:
        bool_lst.append(False)
    if(all(bool_lst)):
        return None
    else:
        return False


def perosn_validation(person_record,record):
    lst=[]
    if (person_record.get('firstName')):
        lst.append(valid_name(person_record['firstName']))
        record.append(person_record['firstName'])
    else:
        lst.append(False)
    if (person_record.get('middleName')):
        lst.append(valid_name(person_record['middleName']))
        record.append(person_record['middleName'])
    else:
        record.append("")
    if (person_record.get('lastName')):
        lst.append(valid_name(person_record['lastName']))
        record.append(person_record['lastName'])
    else:
        lst.append(False)
    if (person_record.get('age')):
        lst.append(valid_age(person_record['age']))
        record.append(person_record['age'])
    else:
        lst.append(False)
    if(person_record.get('address')):
        val= address_validation(person_record['address'],record)
        if(val==False):
            lst.append(False)
        else:
            lst.append(True)
            #record.append(val)
    if(person_record.get('phoneNumbers')):
        nums = phone_numbers_validation(person_record['phoneNumbers'],record)
        #print nums
        if(nums == False):
            lst.append(False)
        else:
            lst.append(True)
            #record.append(nums)

    return all(lst)


    
    
    


def file_validation(fl_data):
    no_persons=count_of_persons(fl_data)
    all_records = []
    valid_or_not = []
    for i in range(0,no_persons):
        record = []
        person=fl_data['persons'][i]
        valid_or_not.append(perosn_validation(person,record))
        all_records.append(record)
    if(all(valid_or_not))==False:
        return False
    else:
        return all_records
    





