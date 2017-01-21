import sqlite3


def create_tempdb():
    conn = sqlite3.connect('tempdb')
    curs=conn.cursor()
    curs.execute("create table if not exists file_content_table(file_id integer primary key autoincrement,file_name varchar(25) not null,priority int not null,file_contents text not null) ");
    return 

def create_compressed_db():
    conn=sqlite3.connect('tempdb.tgz.md5')
    curs = conn.cursor()
    curs.execute('create table if not exists compressed_data_table(file_id int  primary key,compress_data blob,md5_hash_value char(32),validFlag int )');
    return 

def create_validated_db():
    conn=sqlite3.connect('tempdb-json')
    curs = conn.cursor()
    curs.execute('create table if not exists file_details(f_id integer primary key,f_name varchar(25))')
    curs.execute('create table if not exists person_details(person_id integer primary key autoincrement,f_id integer,first_name varchar(20) not null,Middle_name varchar(25) ,last_name varchar(25) not null,person_age int,street_add text not null, city text not null,state text not null ,postal_code int not null,phn_num text,mb_num text,foreign key(f_id) references file_details(f_id) )');

    return 
create_tempdb()
create_compressed_db()
create_validated_db()
