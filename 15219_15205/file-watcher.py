from os import listdir
import os
import time
from os.path import isfile,join
import sys
import re
import operator
import sqlite3
from xml_parsing import *


conn = sqlite3.connect('tempdb')
temp_curs=conn.cursor()
temp_curs.execute("create table if not exists file_content_table(file_id integer primary key autoincrement,file_name varchar(25) not null unique,priority     int not null,file_contents text not null) ");

path= sys.argv[1]
#temp_curs=create_tempdb()

def change_file_name(old_nm,new_nm):
    os.rename(old_nm,new_nm)
    return

def check_priority_change_rqst():
    pat=re.compile('\.(?P<JsonFl>([a-z]*|[0-9]*|[-_]*)+\.json)\.(?P<old_prt>[0-9]*)\.(?P<nw_prt>[0-9]*)')
    for fl_nm in os.listdir(path):
        obj=pat.match(fl_nm)
        if(obj!=None):
            old_pat = re.compile('\.(?P<JsonFl>([a-z]*|[0-9]*|[-_]*)+\.json)\.(?<old_prt>[0-9]*)')
            for fl in os.listdir(path):
                nwobj=old_prt.match(fl)
                if(nwobj!=None and (nwobj.group()==(obj.group('JsonFl')+'.'+obj.group('old_prt')))):
                    nw_name = obj.group('JsonFl')+'.'+obj.group('nw_prt')
                    change_file_name(fl,nw_name)
    return



def remove_element_from_list(elem,lst):
    if elem in lst:lst.remove(elem)
    return elem

def check_json_file_present(all_fl_lst,json_fl):
    patrn= re.compile('(?P<JsonFl>([a-z]*|[0-9]*|[-_]*)+\.json)$')
    for i in all_fl_lst:
        obj = patrn.match(i)
        if(obj!=None):
            if(json_fl==obj.group('JsonFl')):
                return 1
    return 0



def sort_files_priority(lst_fl):
    from collections import OrderedDict
    new_lst=OrderedDict()
    for key,val in sorted(lst_fl.iteritems(),key=lambda(k,v):(v,k)):
        new_lst[key]=val
    print new_lst
    return new_lst 


def find_all_files(path):
    check_priority_change_rqst()
    all_file= [f for f in listdir(path) if isfile(join(path,f))]
    pat= re.compile('\.(?P<filename>([a-z]*|[0-9]*|[-_]*)+\.json)\.(?P<priority>[0-9]*)$')
    lst={}
    for i in all_file:
        obj = pat.match(i)
        if(obj!=None):
            if(check_json_file_present(all_file,obj.group('filename'))):
                lst[obj.group('filename')]=int(obj.group('priority'))
            #print os.path.getmtime(i)
    return lst


def find_new_files(path):
    fl_lst = find_all_files(path)
    db_files=temp_curs.execute('select file_name from file_content_table');
    all_file_lst =[x.encode('UTF8') for x  in [j[0] for j in  [i for i in db_files]]]
    old_fl = fl_lst.keys()
    lst_file=filter(lambda x : x not in all_file_lst,old_fl)
    nw_fls={k:fl_lst[k] for k in fl_lst.keys() if k in lst_file}
    if(nw_fls=={}):
        return 1
    else:
        return sort_files_priority(nw_fls)

def denie_file_edit_permissions_to_user(all_nw_fl):
    for i in all_nw_fl:
        os.chmod(i,0444)
    return


def insert_file_to_tempdb(path):
    conf_file = 'tConfig.sleepDuration.xml'
    tm = float(find_time(conf_file))
    while(1):
        lst_new_files = find_new_files(path)
        if(lst_new_files==1):
            print 'No new files found'
            #try :
            time.sleep(tm)
            return insert_file_to_tempdb(path)
        denie_file_edit_permissions_to_user(lst_new_files)
        for i in lst_new_files:
            fp = open(i,'r')
            fnm = i 
            fp_contents = fp.readlines()
            fp_contents = "".join(fp_contents)
            val = (lst_new_files[i])
            temp_curs.execute("insert into file_content_table (file_name,priority,file_contents) values (?,?,?)",(fnm,val,fp_contents))
            conn.commit()
        entries = temp_curs.execute('select file_id,file_name,priority from file_content_table');
        #print entries
        #for i in entries:
        #    print i ,'\n'



#lst =  find_all_files(path)
#print lst 

#n_lst = find_new_files(lst)
insert_file_to_tempdb(path)

