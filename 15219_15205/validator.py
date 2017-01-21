from json_content_validator import *
from xml_parsing import *
import sqlite3
import time

path = findPath('pConfig.databasePath.xml')
conn= sqlite3.connect(path)
curs=conn.cursor()

connMd=sqlite3.connect('tempdb.tgz.md5')
cursMd=connMd.cursor()

connValid=sqlite3.connect('tempdb-json')
cursValid=connValid.cursor()

def searchFroNewEntries(tempCurs,mdCurs):
    tempCurs.execute('select file_id from file_content_table;')
    allFileLst = tempCurs.fetchall()
    mdCurs.execute('select file_id from compressed_data_table;')
    oldFileLst=mdCurs.fetchall()
    newFileEtries=[i[0] for i in (filter(lambda i : i not in oldFileLst,allFileLst))]
    tempCurs.execute("select * from file_content_table where (file_id in ("+",".join(["?"]*len(newFileEtries))+")) order by priority",newFileEtries);
    values = tempCurs.fetchall()
    return values    #return values[0]


def fetch_data_to_validate(listJson):
    jsonObj = json.loads(listJson)
    return jsonObj


def insertValidData(listOfNewEntries):
    for i in listOfNewEntries:
        jObj = fetch_data_to_validate(i[3])
        checkValid=file_validation(jObj)
        if (checkValid!=False):
            cursMd.execute('update compressed_data_table set validFlag=1 where file_id = ?',(i[0],));
            cursMd.execute('insert into compressed_data_table(file_id,validFlag) select ?,? where (select changes()=0)',(i[0],1));
            print i[0],i[1]
            cursValid.execute('insert into file_details values(?,?)',(i[0],i[1]));
            for entry in checkValid:
                entry = [i[0]]+entry
                cursValid.execute('insert into person_details(f_id,first_Name,Middle_Name,Last_Name,person_age,street_add,city,state,postal_code,phn_num,mb_num) values(?,?,?,?,?,?,?,?,?,?,?)',entry);
                connValid.commit()
                print entry
        else:
            cursMd.execute('update compressed_data_table set validFlag = 0 where file_id=?',(i[0],));
            cursMd.execute('insert into compressed_data_table(file_id,validFlag) select ?,? where (select changes()=0)',(i[0],0));
    connMd.commit()
    connValid.commit()


#insertValidData(records)
#cursValid.execute('select * from person_details');
#lst = cursValid.fetchall()
#print lst

def main():
    conf_file = 'tConfig.sleepDuration.xml'
    tm = float(find_time(conf_file))
    while(1):
        records =  searchFroNewEntries(curs,cursMd)
        if(records==[]):
            print "no record found"
            time.sleep(tm)
            return main()
        insertValidData(records)
        print "record inserted"
        



if __name__=="__main__":main()    
