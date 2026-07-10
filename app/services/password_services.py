from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()


def hash_password(password:str):
    return password_hash.hash(password)



def verify_password(plain_password:str,hash_password:str):
    return password_hash.verify(plain_password,hash_password)


