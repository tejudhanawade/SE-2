import sqlite3,time
import time,hashlib
from xml_parsing import *


path = findPath('pConfig.databasePath.xml')
conn = sqlite3.connect(path)
curs = conn.cursor()

conn_md5 = sqlite3.connect('tempdb.tgz.md5')
curs_md5 = conn_md5.cursor()


def find_new_entries():
    curs.execute('select file_id from file_content_table');
    tmdb_lst=curs.fetchall()
    tmdb_lst=[i for i in tmdb_lst]
    curs_md5.execute('select file_id from compressed_data_table');
    md5_lst = curs_md5.fetchall()
    curs_md5.execute('select file_id from compressed_data_table where md5_hash_value is null ');
    md5_null_lst= curs_md5.fetchall()
    md5_lst=[i for i in md5_lst]
    new_fls= filter(lambda x: x not in md5_lst,tmdb_lst)
    lst = new_fls+md5_null_lst
    return lst


def compressData(lst):
    for i in lst:
        k=curs.execute('select * from file_content_table where file_id=? order by priority',i)
        flObj=k.fetchall()
        strn = flObj[0][-1]
        mdVal= hashlib.md5(strn).hexdigest()
        cmprs = sqlite3.Binary(strn.encode("zlib"))
        curs_md5.execute('update compressed_data_table set compress_data=?  where file_id = ?',(cmprs,i[0]));
        curs_md5.execute('update compressed_data_table set md5_hash_value=?  where file_id = ?',(mdVal,i[0]));
        curs_md5.execute('select * from compressed_data_table');
        curs_md5.execute('insert into compressed_data_table(file_id,compress_data,md5_hash_value) select ?,?,? where (select changes()=0)',(i[0],cmprs,mdVal));

        conn_md5.commit()

def main():
    tm = float(find_time('tConfig.sleepDuration.xml'))
    
    while(1):
        lst = find_new_entries()
        if(lst==[]):
            time.sleep(tm)
            return main()
        else:
           compressData(lst)


if __name__=="__main__":main()

