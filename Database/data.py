import sqlite3
from datetime import datetime as dt

conn = sqlite3.connect('data.sqlite')
cur = conn.cursor()


# cur.executescript('''

# DROP TABLE IF EXISTS Personal;
# DROP TABLE IF EXISTS Account;
# DROP TABLE IF EXISTS Card;
# DROP TABLE IF EXISTS Trans;

# CREATE TABLE "Personal" (
# 	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
# 	"name"	TEXT,
# 	"email"	TEXT,
# 	"mobile"	INTEGER,
# 	"dob"	NUMERIC
# );

# CREATE TABLE "Account" (
# 	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
# 	"account_no"	INTEGER,
# 	"balance"	REAL,
# 	"personal_id"	INTEGER
# );

# CREATE TABLE "Card" (
# 	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
# 	"card_no"	INTEGER,
# 	"pin"	INTEGER,
# 	"card_state"	INTEGER,
# 	"pin_count"	INTEGER,
# 	"unblock_time"	TEXT,
# 	"account_id"	INTEGER,
# 	"personal_id"	INTEGER,
# 	"expiry"	NUMERIC,
#     "csv"   INTEGER
# );

# CREATE TABLE "Trans" (
# 	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
#     "trans"   TEXT,
# 	"amount"	REAL,
#   "balance"	REAL,
# 	"datetime"	TEXT,
# 	"account_id"	INTEGER
# );


# ''')

# name = input('enter your name:')
# email = input('enter your email:')
# mobile = int(input('enter your mobile no:'))
# dob = input('enter your dob:')
# pin=int(input("Enter pin:"))
# first_depo=float(input('enter the first amount:'))

#............. For first insertion use code below..................................
# cur.execute("INSERT INTO Personal (name,email,mobile,dob) VALUES (?,?,?,?)",(name,email,mobile,dob))
# cur.execute("SELECT id FROM Personal WHERE (name,email,mobile,dob) = (?,?,?,?)",(name,email,mobile,dob))
# personal_id = cur.fetchone()[0]
# cur.execute("INSERT INTO Account (account_no,balance,personal_id) VALUES (?,?,?) ",(100001,first_depo,personal_id))
# cur.execute("SELECT id FROM Account WHERE personal_id = ?",(personal_id,))
# account_id = cur.fetchone()[0]
# cur.execute("""INSERT INTO Card (card_no,pin,card_state,pin_count, unblock_time, account_id, personal_id, expiry ,csv) 
#                VALUES (?,?,?,?,?,?,?,?,?)  """,(1000000+1,pin,1,3,dt.now(),account_id,personal_id,'1/25',100))
# cur.execute('''INSERT INTO Trans (trans,amount,balance,datetime,account_id) VALUES (?,?,?,?,?)''',('Debited',first_depo,first_depo,str(dt.now()).split('.')[0],account_id))



# ...............For insertion other than first use the code below..........................

# cur.execute("INSERT INTO Personal (name,email,mobile,dob) VALUES (?,?,?,?)",(name,email,mobile,dob))
# cur.execute("SELECT id FROM Personal WHERE (name,email,mobile,dob) = (?,?,?,?)",(name,email,mobile,dob))
# personal_id = cur.fetchone()[0]

# cur.execute("SELECT account_no FROM Account WHERE personal_id=?",(personal_id-1,))	#selecting previous id's account_no
# account_no=cur.fetchone()[0]

# cur.execute("INSERT INTO Account (account_no,balance,personal_id) VALUES (?,?,?) ",(int(account_no)+1,first_depo,personal_id))
# cur.execute("SELECT id FROM Account WHERE personal_id = ? ",(personal_id,))
# account_id = cur.fetchone()[0]

# cur.execute("SELECT card_no FROM Card WHERE personal_id=?",(personal_id-1,))	#selecting previous id's card_no
# card_no=cur.fetchone()[0]

# cur.execute("""INSERT INTO Card (card_no,pin,card_state,pin_count, unblock_time, account_id, personal_id, expiry ,csv) 
#                VALUES (?,?,?,?,?,?,?,?,?)  """,(int(card_no)+1,pin,1,3,dt.now(),account_id,personal_id,'1/25',100))

# cur.execute('''INSERT INTO Trans (trans,amount,balance,datetime,account_id) VALUES (?,?,?,?,?)''',('Debited',first_depo,balance,str(dt.now()).split('.')[0],account_id))



#...........CODE FOR UNDERSTANDING WORKING OF DIFFERENT FUNCTIONS............
#.............SELECTION OF PARTICUALR DATA.................

# card_no=100003
# cur.execute('SELECT account_id,balance,pin,card_state,pin_count,unblock_time,expiry FROM Account JOIN Card on Account.id=Card.account_id WHERE card_no=?',(card_no,))
# # for a in aa:
# #     print(a)
# #     account_id=a[0]
# #     balance=a[1]
# a=cur.fetchone()
# if a:
#     account_id,balance,pin,card_state,pin_count,unblock_time,expiry = a
#     print(a)
#     if account_id:
#         print('got it')
# else:
#     print('ahhyeah')

#.............UPDATION OF PARTICULAR DATA..................

# deposit=1000
# cur.execute('UPDATE Account SET balance = ? WHERE id=?',(balance+deposit,account_id))

#...................ADDING TRANSACTION.........

#cur.execute('''INSERT INTO Trans (trans,amount,balance,datetime,account_id) VALUES (?,?,?,?,?)''',('Debited',first_depo,first_depo,str(dt.now()).split('.')[0],account_id))


#...............DISPLAYING LAST N TRANSACTIONS...............

cur.execute('SELECT account_id FROM Card WHERE card_no=?',(100001,))
account_id = cur.fetchone()[0]
details = cur.execute('SELECT trans,amount,balance,datetime FROM Trans WHERE account_id=? ORDER BY id DESC LIMIT ?',(account_id,5))
text='Date\t\tTime\t Transaction\t Amount\t Balance'
print(text)
for detail in details:
    trans,amount,datetime,balance = detail
    text=datetime.split(' ')[0]+'    '+datetime.split(' ')[1]+'\t   '+trans+'\t '+str(amount)+'\t '+str(balance)
    print(text)

conn.commit()
