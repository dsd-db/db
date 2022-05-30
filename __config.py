import os
import sqlite3
from typing import Union

DIR=os.getenv('DSD_DATABASE')

if DIR is None:
    DIR='./.data'

DIR=os.path.abspath(DIR)

DEVICE='device'
DEVICE=os.path.join(DIR,DEVICE)

MODEL='%s.mdl'
MODEL=os.path.join(DEVICE,'%s',MODEL)

CALIBRATION='calibration'
CALIBRATION=os.path.join(DEVICE,'%s',CALIBRATION)

DB='main.db'
DB=os.path.join(DIR,DB)

os.makedirs(DEVICE,exist_ok=True)

con=sqlite3.connect(DB,check_same_thread=False)
# con.set_trace_callback(print)

def e(s:str,t:tuple=tuple())->Union[str,None]:
    if t:
        s=con.execute(s,t).fetchone()
    else:
        s=con.execute(s).fetchone()
    con.commit()
    if s is None:
        return None
    else:
        return s[0]

e('''
    create table if not exists admin(
        username varchar(64) primary key not null,
        email varchar(256),
        password varchar(64) not null
    );
''')

e('''
    create table if not exists device(
        uuid varchar(64) primary key not null,
        email varchar(256),
        calibration varchar(256)
    );
''')

e('''
    create table if not exists model(
        uuid varchar(64) not null,
        algo varchar(64),
        path varchar(256),
        primary key(uuid,algo),
        foreign key(uuid) references device(uuid)
    );
''')


if __name__=='__main__':
    print(DIR)
    print(DEVICE)
    print(MODEL)
    print(CALIBRATION)
    print(DB)
