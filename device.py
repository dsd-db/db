import os
import shutil
import sqlite3
from uuid import UUID

from db.__config import DB_DEVICE,MODEL,CALIBRATION
con=sqlite3.connect(DB_DEVICE,check_same_thread=False)
cur=con.cursor()
cur.execute('create table if not exists device(uuid varchar(64) primary key,banned boolean,email varchar(1024),model varchar(1024),calibration varchar(1024))')
con.commit()


def get(uuid:str,create:bool=True):
    uuid=str(uuid)
    UUID(uuid,version=4)
    cur.execute('select banned,email,model,calibration from device where uuid=?',(uuid,))
    info=cur.fetchone()

    if create and not info:
        _model=MODEL%uuid
        _calibration=CALIBRATION%uuid
        cur.execute('insert into device(uuid,banned,email,model,calibration) values(?,?,?,?,?)',(uuid,False,None,_model,_calibration))
        con.commit()
        info=(0,None,_model,_calibration)
        os.makedirs(_calibration)

    if info:
        return Device(uuid)
    # else:
    #     return None


def remove(uuid:str)->None:
    uuid=str(uuid)
    UUID(uuid,version=4)
    cur.execute('delete from device where uuid=?',(uuid,))
    _dir=os.path.dirname(CALIBRATION%uuid)
    if os.path.exists(_dir):
        shutil.rmtree(_dir)
    con.commit()


class Device:
    def __init__(
        self,
        uuid:str
    )->None:
        self._id=uuid

    @property
    def id(self):
        return UUID(self._id,version=4)

    @property
    def banned(self)->bool:
        cur.execute('select banned from device where uuid=?',(self._id,))
        return cur.fetchone()[0]
    
    @banned.setter
    def banned(self,value:bool)->None:
        cur.execute('update device set banned=? where uuid=?',(value,self._id))
        con.commit()

    @property
    def email(self)->str:
        cur.execute('select email from device where uuid=?',(self._id,))
        return cur.fetchone()[0]

    @email.setter
    def email(self,value:str)->None:
        cur.execute('update device set email=? where uuid=?',(value,self._id))
        con.commit()

    @property
    def model(self)->str:
        cur.execute('select model from device where uuid=?',(self._id,))
        s=cur.fetchone()[0]
        if os.path.exists(s):
            return s
        # else:
        #     return None

    @model.setter
    def model(self,value:str)->None:
        cur.execute('select model from device where uuid=?',(self._id,))
        s=cur.fetchone()[0]
        shutil.copyfile(value,s)


    @property
    def calibration(self)->str:
        cur.execute('select calibration from device where uuid=?',(self._id,))
        s=cur.fetchone()[0]
        if os.listdir(s):
            return s
        # else:
        #     return None

    @calibration.setter
    def calibration(self,value:str)->None:
        cur.execute('select calibration from device where uuid=?',(self._id,))
        s=cur.fetchone()[0]
        shutil.copytree(value,s,dirs_exist_ok=True)
