import os
import re
import shutil
from uuid import UUID

from db.__config import Union,e,MODEL,CALIBRATION

class Model:
    def __init__(self,uuid:str)->None:
        self._id=uuid

    def __getitem__(self,key:str)->Union[str,None]:
        if not re.match('^[a-z0-9]+(-[a-z0-9]+)*$',key):
            raise ValueError('algo contains invalid characters')
        return e('select path from model where uuid=? and algo=?',(self._id,key,))

    def __setitem__(self,key:str,value:Union[str,None])->None:
        if not re.match('^[a-z0-9]+(-[a-z0-9]+)*$',key):
            raise ValueError('algo contains invalid characters')
        s=self[key]
        if value is None:
            if s is not None:
                shutil.rmtree(s,ignore_errors=True)
                e('delete from model where uuid=? and algo=?',(self._id,key,))
        else:
            _model=MODEL%(self._id,key,)
            if s is None:
                e('insert into model(uuid,algo,path) values(?,?,?)',(self._id,key,_model,))
            shutil.copyfile(value,_model)


class Device:
    def __init__(self,uuid:str)->None:
        self._id=uuid

    @property
    def id(self)->UUID:
        return UUID(self._id)

    @property
    def email(self)->Union[str,None]:
        return e('select email from device where uuid=?',(self._id,))[0]

    @email.setter
    def email(self,value:Union[str,None])->None:
        if value and len(value)>254:
            raise ValueError('email is too long')
        e('update device set email=? where uuid=?',(value,self._id,))

    @property
    def model(self)->Model:
        return Model(self._id)

    @property
    def calibration(self)->Union[str,None]:
        return e('select calibration from device where uuid=?',(self._id,))[0]

    @calibration.setter
    def calibration(self,value:Union[str,None])->None:
        s=self.calibration
        if value is None:
            if s is not None:
                shutil.rmtree(s,ignore_errors=True)
                e('update device set calibration=? where uuid=?',(None,self._id,))
        else:
            _calibration=CALIBRATION%(self._id,)
            if s is None:
                e('update device set calibration=? where uuid=?',(_calibration,self._id,))
            shutil.copytree(value,_calibration,dirs_exist_ok=True)


def exists(devid:Union[str,UUID])->bool:
    devid=UUID(str(devid)).hex
    return e('select 1 from device where uuid=?',(devid,)) is not None

def get(devid:Union[str,UUID])->Device:
    devid=UUID(str(devid)).hex

    if e('select 1 from device where uuid=?',(devid,)) is None:
        e('insert into device(uuid,email,calibration) values(?,?,?)',(devid,None,None))

    return Device(devid)


def remove(devid:Union[str,UUID])->None:
    devid=UUID(str(devid)).hex
    # s=Device(devid).calibration
    e('delete from device where uuid=?',(devid,))
    _dir=os.path.dirname(CALIBRATION%devid)
    shutil.rmtree(_dir,ignore_errors=True)
