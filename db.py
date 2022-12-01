import sqlite3
import uuid
import hashlib, binascii

def create_account_table():
	conn = sqlite3.connect('demo.db')
	cur = conn.cursor()

	cur.execute("""CREATE TABLE IF NOT EXISTS users (
									email text unique, 
									password text 
									)
							""")
	conn.commit()

def createSecurePassword(password, salt=None, round=100000):
    if not salt:
        salt = uuid.uuid4().hex
    
    # hashlib.pbkdf2_hmac(hash_name, password, salt, iterations, dklen=None)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), 
                        salt.encode('utf-8'), round)
    password = binascii.hexlify(dk)
    return f"{password}:{salt}"

def checkPassword(password, hash):
		hash_password, salt = hash.split(':')
		return hash == createSecurePassword(password, salt)

def create_account(email, password):
	conn = sqlite3.connect('demo.db')
	cur = conn.cursor()

	hashed_password = createSecurePassword(password)
	cur.execute("INSERT INTO users VALUES (?, ?)", (email, hashed_password))
	conn.commit()

def check_account(email, password):
	conn = sqlite3.connect('demo.db')
	cur = conn.cursor()

	cur.execute("SELECT password FROM users WHERE email = ?", (email,))
	hashed_password = cur.fetchone()
	if hashed_password:
		print(hashed_password)
		return checkPassword(password, hashed_password[0])
	else:
		return False

if __name__ == '__main__':
	create_account_table()

