import glob
import time
from os import system

venv = glob.glob('*/bin/activate')
if venv:
    system(f". {venv[0]}")
else:
    system("python3 -m venv venv")
    time.sleep(2)
    system(". venv/bin/activate")

system("pip install -r requirements.txt")

env = open(".env", 'w+')
env.write("DEBUG=True\n")

while True:
    print(f'{"*"*120}\n'*10)
    ADMIN_URL = input("enter the admin url").strip()
    if not ADMIN_URL:
        print("admin url can not be blank")
        continue
    if ADMIN_URL.__contains__(" "):
        print("admin url cant contain space")
        continue
    env.write(f"{ADMIN_URL=}\n")
    break
gauth = input("would you  like to add google auth ? (y/n)").lower()
if gauth == "y":
    GOOGLE_KEY = input("enter the google key (ending with .com)").strip()
    GOOGLE_SECRET = input("enter google secret key").strip()
    env.write(f"{GOOGLE_SECRET=}\n")
    env.write(f"{GOOGLE_KEY=}\n")
env.write("DEFAULT_CLIENT=\n")
input("to continue you need to install  postgres enter to continue ")
psql = input("would you  create new user and database for postgres (y/n)").lower()
if psql == "y":
    DB_NAME = input("enter the dbname").strip()
    DB_USER = input("enter the db user name").strip()
    DB_PASSWORD = input("enter the db password").strip()
    DB_PORT = input("enter the db port ( press enter to set default 5432)")
    if not DB_PORT:
        DB_PORT = 5432
    print("execute the following command in psql shell)")
    print(
        f'create user {DB_USER};create database {DB_NAME};alter role {DB_USER} with password {DB_PASSWORD};grant all privileges on database {DB_NAME} to {DB_USER};alter database {DB_NAME} owner to {DB_USER};ALTER USER {DB_USER} with superuser;')
    input("enter to continue")
else:
    DB_NAME = input("enter the dbname").strip()
    DB_USER = input("enter the db user name").strip()
    DB_PASSWORD = input("enter the db password").strip()
    DB_PORT = input("enter the db port ( press enter to set default 5432)")
    if not DB_PORT:
        DB_PORT = 5432

env.write(f"{DB_USER=}\n")
env.write(f"{DB_NAME=}\n")
env.write(f"{DB_PASSWORD=}\n")
env.write(f"{DB_PORT=}\n")
env.write("OIDC_RSA_PRIVATE_KEY=\n")
