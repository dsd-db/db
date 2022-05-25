from db.__config import e

def add(username:str,password:str)->bool:
    s=e('select 1 from admin where username=?',(username,))
    if s is not None:
        return False

    if username is None:
        raise ValueError('username is empty')
    if password is None:
        raise ValueError('password is empty')
    if len(username)>40:
        raise ValueError('username is too long')
    if len(password)>40:
        raise ValueError('password is too long')
    if not all(c in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_' for c in username):
        raise ValueError('username contains invalid characters')
    if not all(0x1f<ord(c)<0x7f for c in password):
        raise ValueError('password contains invalid characters')

    e('insert into admin(username,email,password) values(?,?,?)',(username,None,password,))
    return True


def check(username:str,password:str)->bool:
    s=e('select password from admin where username=?',(username,))
    if not s:
        return None
    if s[0]!=password:
        return False
    return True

def remove(username:str)->None:
    e('delete from admin where username=?',(username,))
