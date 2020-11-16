from datetime import datetime as dt, timedelta
from tkinter import *
import os
import sqlite3
from face_cap import Capture
from mailer import Mailer
from qr_scanner import Scanner
import threading




root = Tk()
#root.attributes('-zoomed', True)
root.geometry("1280x720")
root.resizable(0,0)
root.configure(background="#1ae8d3")
#w, h = root.winfo_screenwidth(),root.winfo_screenheight()
label = Label(root,text="Welcome To ATM")
label.configure(background="#1ae8d3")
label.pack(pady=50)

class Audios():
    def welcome(self):    
        #os.system("mpg321 welcome.mp3") 
        pass
    def card_window(self):
        #os.system("mpg321 card_no.mp3") 
        pass

class Atm():
       
    row_num = 0
    entered_card = ''
    entered_pin = 0
    pin = 0
    balance = 0.0
    card_state = 0
    pin_count = 0
    unblock_time = dt.now()

    def __init__(self,root):
        btn = Button(root,text="Continue",state=ACTIVE,command=self.card_window)
        btn.pack(pady=20)
        Button(root,text="Use Virtual Card",command=self.vcard_window).pack(pady=10)
        root.after(1000,Audios().welcome)

    # create numpad
    def numpad(self,root,row=0,column=0):
        b1 = Button(root,text='1',width=5,bg='SlateGray4',fg='white',height=2,font=("Times", 14,'bold'))
        b1.place(x=row+0,y=column+0)

                
        b2 = Button(root,text='2',width=5,bg='SlateGray4',fg='white',height=2,font=("Times", 14,'bold'))
        b2.place(x=row+70,y=column+0)

        b3 = Button(root,text='3',width=5,bg='SlateGray4',fg='white',height=2,font=("Times", 14,'bold'))
        b3.place(x=row+140,y=column+0)

        b4 = Button(root,text='4',width=5,bg='SlateGray4',fg='white',height=2,font=("Times", 14,'bold'))
        b4.place(x=row+0,y=column+70)

        b5 = Button(root,text='5',width=5,bg='SlateGray4',fg='white',height=2,font=("Times", 14,'bold'))
        b5.place(x=row+70,y=column+70)

            
        b6 = Button(root,text='6',width=5,bg='SlateGray4',fg='white',height=2,font=("Times", 14,'bold'))
        b6.place(x=row+140,y=column+70)

        b7 = Button(root,text='7',width=5,bg='SlateGray4',fg='white',height=2,font=("Times", 14,'bold'))
        b7.place(x=row+0,y=column+140)

        b8 = Button(root,text='8',width=5,bg='SlateGray4',fg='white',height=2,font=("Times", 14,'bold'))
        b8.place(x=row+70,y=column+140)

                
        b9 = Button(root,text='9',width=5,bg='SlateGray4',fg='white',height=2,font=("Times", 14,'bold'))
        b9.place(x=row+140,y=column+140)


        b0 = Button(root,text='0',width=5,height=2,bg='SlateGray4',fg='white',font=("Times", 14,'bold'))
        b0.place(x=row+70,y=column+210)

            
        
        b = Button(root,text='CLEAR',width=5,bg='SlateGray4',fg='white',height=2,font=("Times", 13,'bold'))
        b.place(x=row+230,y=column+0)

        b = Button(root,text='ENTER',width=5,bg='SlateGray4',fg='white',height=2,font=("Times", 13,'bold'))
        b.place(x=row+230,y=column+70)

        b = Button(root,text='CANCEL',width=6,bg='SlateGray4',fg='white',height=2,font=("Times",12,'bold'))
        b.place(x=row+230,y=column+140)

        # btn0 = Button(window,text = "0", padx=40,pady=20,command = lambda:self.numpad_click(window,'0'))
        # btn1 = Button(window,text = "1", padx=40,pady=20,command = lambda:self.numpad_click(window,'1'))
        # btn2 = Button(window,text = "2", padx=40,pady=20,command = lambda:self.numpad_click(window,'2'))
        # btn3 = Button(window,text = "3", padx=40,pady=20,command = lambda:self.numpad_click(window,'3'))
        # btn4 = Button(window,text = "4", padx=40,pady=20,command = lambda:self.numpad_click(window,'4'))
        # btn5 = Button(window,text = "5", padx=40,pady=20,command = lambda:self.numpad_click(window,'5'))
        # btn6 = Button(window,text = "6", padx=40,pady=20,command = lambda:self.numpad_click(window,'6'))
        # btn7 = Button(window,text = "7", padx=40,pady=20,command = lambda:self.numpad_click(window,'7'))
        # btn8 = Button(window,text = "8", padx=40,pady=20,command = lambda:self.numpad_click(window,'8'))
        # btn9 = Button(window,text = "9", padx=40,pady=20,command = lambda:self.numpad_click(window,'9'))
        # btn_delete = Button(window,text = "delete", padx=27,pady=20,command = lambda:self.numpad_click(window,'delete'))
        # btn1_clear = Button(window,text = "clear", padx=27,pady=20,command = lambda:self.numpad_click(window,'clear'))
        
        # btn0.grid(row=row+3,column=column+1)
        # btn1.grid(row=row+0,column=column+0)
        # btn2.grid(row=row+0,column=column+1)
        # btn3.grid(row=row+0,column=column+2)
        # btn4.grid(row=row+1,column=column+0)
        # btn5.grid(row=row+1,column=column+1)
        # btn6.grid(row=row+1,column=column+2)
        # btn7.grid(row=row+2,column=column+0)
        # btn8.grid(row=row+2,column=column+1)
        # btn9.grid(row=row+2,column=column+2)
        # btn_delete.grid(row=row+3,column=column+2)
        # btn1_clear.grid(row=row+3,column=column+0)

    # numpad actions
    def numpad_click(self,window,key):
        previous = self.e.get()
        if key=='clear':
            self.e.delete(0,END)
        elif (key=='delete'):
            self.e.delete(0,END)
            self.e.insert(0,previous[0:len(previous)-1])
        else:
            self.e.delete(0,END)
            self.e.insert(0,previous+key)


    def vcard_window(self):
        self.top=Toplevel()
        self.top.geometry("1280x720")
        self.top.configure(background="#1ae8d3")
        self.label = Label(self.top,text="Scan the QR Code",background="#1ae8d3")
        self.label.pack(pady=5)
        self.top.after(100,self.qr_scan)


    def qr_scan(self):
        text=Scanner.scan(Scanner)
        #print('text='+text)
        if text:
            self.top.destroy()
            self.search_win(text)
        else:
            self.label.configure(text="QR code not found")
            self.top.after(3000,self.top.destroy)


    #window to enter card number
    def card_window(self):
        self.top = Toplevel()
        self.top.geometry("1280x720")
        # self.top.attributes('-zoomed', True)
        self.top.configure(background="#1ae8d3")
        label = Label(self.top,text="Enter your card number")
        label.grid(row =0,column=0,pady=20,padx=100,columnspan=3)
        label.configure(background="#1ae8d3")
        self.e = Entry(self.top,width=30)
        self.e.grid(row=1,column=0,pady=20,columnspan=3)
        Button(self.top,text="Continue",command=self.search_win).grid(row=2,column=1,pady=20)
        self.destroyTimer(20,self.top)
        self.numpad(self.top,row=500,column=400)
        self.top.after(500,Audios().card_window) 

    #window to search user
    def search_win(self,*card):
        top1 = Toplevel()
        top1.attributes('-zoomed', True)
        top1.configure(background="#1ae8d3")
        label = Label(top1,text="searching")
        label.configure(background="#1ae8d3")
        label.pack()
        #Button(top1,text="Continue",command=Capture.click).pack()
        entered_card = card[0] if card else self.e.get()
        print(entered_card)
        self.top.destroy()
        found = self.search_user(entered_card)
        if found:
            if (self.card_state == 0 and self.unblock_time > dt.now()):
                top1.after(3000,self.card_blocked)
                top1.after(3000,top1.destroy)
                self.conn.commit()
            elif (self.card_state == 0):
                self.edit_balance('unblock')
            elif found:
                print("found")
                top1.after(100,self.cam,top1,label)
                print('opening camera')
        else:
            print('not found')
            top1.after(1000,self.not_found)
            top1.after(3000,top1.destroy)
            self.conn.commit()

    def cam(self,top1,label):
        Capture.capture(Capture)
        if Capture.clicked:
            top1.after(500,self.pin_window,top1)
            Capture.clicked=0
        else:
            label.configure(text="face not detected")
            top1.after(3000,top1.destroy)
            print("face detection failed")
            self.conn.commit()

    def not_found(self):
        top = Toplevel()
        top.attributes('-zoomed', True)
        top.configure(background="#1ae8d3")
        label = Label(top,text = 'Cannot find your details!')
        label.configure(background="#1ae8d3")
        label.pack()
        self.destroyTimer(6,top)


    def card_blocked(self):
        top = Toplevel()
        top.attributes('-zoomed', True)
        top.configure(background="#1ae8d3")
        label = Label(top,text = 'Your card is blocked!')
        label.configure(background="#1ae8d3")
        label.pack()
        self.destroyTimer(6,top)           

    def pin_window(self,top1):  #taking top1 as argument to destroy
        top1.destroy()
        self.top2 = Toplevel()
        #self.top2.geometry("400x300")
        self.top2.attributes('-zoomed', True)
        self.top2.configure(background="#1ae8d3")
        label = Label(self.top2,text="Enter your pin")
        label.grid(row=0,column=0,columnspan=3,pady=20)
        label.configure(background="#1ae8d3")
        self.e = Entry(self.top2,width=30)
        self.e.grid(row=1,column=0,columnspan=3,pady=20)
        Button(self.top2,text="Continue",command=self.check_pin).grid(row=2,column=1)
        self.numpad(self.top2,row=3)
        self.destroyTimer(20,self.top2)


    def check_pin(self):
        entered_pin = self.e.get()
        print(self.pin)
        print(entered_pin)
        if (int(entered_pin)== self.pin):
            print("pin verified")
            self.top2.destroy()
            self.menu()
        else:
            self.pin_count-=1
            self.edit_balance("pin_count") 
            self.top2.destroy()
            if self.pin_count==0:
                self.card_blocked()
                self.edit_balance('block')#edit card state to 0
            else:
                self.wrong_pin()
                print("wrong pin")

    def wrong_pin(self):
        self.top2 = Toplevel()
        #self.top2.geometry("400x300")
        self.top2.attributes('-zoomed', True)
        self.top2.configure(background="#1ae8d3")
        label = Label(self.top2,text="Entered wrong pin...")
        label.grid(row=0,column=0,columnspan=3,pady=20)
        label.configure(background="#1ae8d3")
        self.destroyTimer(5,self.top2)

            
    def destroyTimer(self,time,window):
        print("time remaining",time)
        if time==0:
            window.destroy()
            return
        window.after(1000,self.destroyTimer,time-1,window)


    def search_user(self,entered_card):

        self.conn = sqlite3.connect("data.sqlite")
        self.cur = self.conn.cursor()

        self.cur.execute("SELECT account_id,balance,pin,card_state,pin_count,unblock_time,expiry FROM Account JOIN Card ON Account.id=Card.account_id WHERE card_no=?",(entered_card,))
        user = self.cur.fetchone()
        if user:
            account_id,balance,pin,card_state,pin_count,unblock_time,expiry = user
            print(account_id)
            self.account_id = account_id
            self.pin = pin
            self.balance = balance
            self.pin_count = pin_count
            self.card_state = card_state
            t_str = unblock_time
            self.unblock_time = dt(int(t_str[0:4]),int(t_str[5:7]),int(t_str[8:10]),int(t_str[11:13]),int(t_str[14:16]),int(t_str[17:19]))
            return 1
        else:
            print('not found')
        return 0
       

    def edit_balance(self,*detail):  
        print("in edit")
        self.cur.execute("SELECT email FROM Personal JOIN Account ON Personal.id=Account.personal_id WHERE Account.id=?",(self.account_id,))
        email=self.cur.fetchone()[0] 
        try:
            if detail[0]=="pin_count":
                self.cur.execute('UPDATE Card SET pin_count=? WHERE account_id=?',(self.pin_count,self.account_id))
                print('pincount updated')
                threading.Thread(target=Mailer.mail,args=(Mailer,email,"wrong pin")).start()
            if detail[0] == 'unblock':
                self.cur.execute('UPDATE Card SET card_state=?,pin_count=? WHERE account_id=?',(1,3,self.account_id))
            if detail[0] == 'block':
                self.cur.execute('UPDATE Card SET card_state=?,unblock_time=? WHERE account_id=?',(0,dt.now()+ timedelta(hours=24),self.account_id))
                threading.Thread(target=Mailer.mail,args=(Mailer,email,"block")).start()
                print("blocked on ", dt.now())
            if detail[0]=="pin":
                print("in pin")
                self.cur.execute('UPDATE Card SET pin=? WHERE account_id=?',(self.pin,self.account_id))   
                threading.Thread(target=Mailer.mail,args=(Mailer,email,"pin")).start()            
            if detail[0] == "withdraw":
                self.balance = self.balance - self.withdraw_amount
                self.cur.execute('UPDATE Account SET balance=? WHERE id=?',(self.balance,self.account_id))
                threading.Thread(target=Mailer.mail,args=(Mailer,email,"withdraw",self.withdraw_amount)).start()
                self.add_trans("withdraw")
            if detail[0] =="deposit":
                self.balance = self.balance + self.deposit_amount
                self.cur.execute('UPDATE Account SET balance=? WHERE id=?',(self.balance,self.account_id))
                self.add_trans("deposit")
                threading.Thread(target=Mailer.mail,args=(Mailer,email,"deposit",self.deposit_amount)).start()
            if detail[0] == "check balance":
                threading.Thread(target=Mailer.mail,args=(Mailer,email,"check balance")).start()
        except:
            pass

        self.conn.commit()

    def add_trans(self,detail):
        if detail == "deposit":
            print("transaction added")
            trans="Credited"
            amount = self.deposit_amount
            self.cur.execute('''INSERT INTO "Trans" (trans,amount,balance,datetime,account_id) VALUES (?,?,?,?,?)''',(trans,amount,self.balance,str(dt.now()).split('.')[0],self.account_id))
        if detail == "withdraw":
            trans="Debited"
            amount = self.withdraw_amount
            self.cur.execute('INSERT INTO "Trans" (trans,amount,balance,datetime,account_id) VALUES (?,?,?,?,?)',(trans,amount,self.balance,str(dt.now()).split('.')[0],self.account_id))
        self.conn.commit()



    def menu(self):
        self.top4 = Toplevel()
        self.top4.attributes('-zoomed', True)
        self.top4.configure(background="#1ae8d3")
        self.top4.geometry("1280x720")
        btn1 = Button(self.top4,text="Withdraw",command=self.withdraw_win)
        btn2 = Button(self.top4,text="Deposit",command=self.deposit_win)
        btn3 = Button(self.top4,text="Change Pin",command=self.change_pin1)
        btn4 = Button(self.top4,text="Check Balance",command=self.check_balance)
        Button(self.top4,text="last 5 transaction",command=self.transaction_info).grid(row=4,column=0)

        btn1.grid(row= 0,column=0)
        btn2.grid(row= 1,column=0)
        btn3.grid(row= 2,column=0)
        btn4.grid(row= 3,column=0)

        self.destroyTimer(20,self.top4)            

    def withdraw_check(self):
        self.withdraw_amount = float(self.e.get())
        self.top8.destroy()
        if self.withdraw_amount < self.balance :
            self.edit_balance("withdraw")
            top = Toplevel()
            top.geometry("400x300")
            top.configure(background="#1ae8d3")
            label = Label(top,text="Successful")
            label.configure(background="#1ae8d3")
            label.pack()
            self.destroyTimer(6,top)
        else:
            top = Toplevel()
            top.geometry("400x300")
            top.configure(background="#1ae8d3")
            label = Label(top,text="Insufficient balance")
            label.configure(background="#1ae8d3")
            label.pack()
            self.destroyTimer(6,top)

    def withdraw_win(self):
        self.top4.destroy()
        self.top8 = Toplevel()
        #self.top8.geometry("400x300")
        self.top8.attributes('-zoomed', True)
        self.top8.configure(background="#1ae8d3")
        label = Label(self.top8,text="Enter the amount in rupees")
        label.configure(background="#1ae8d3")
        label.grid(row=0,column=0,columnspan=3)
        self.e =Entry(self.top8,width=30)
        self.e.grid(row=1,column=0,columnspan=3) 
        btn = Button(self.top8,text="Continue",command=self.withdraw_check)
        btn.grid(row=2,column=1)
        self.numpad(self.top8,row=3)
        self.destroyTimer(20,self.top8)

    def deposit_check(self):
        self.deposit_amount = float(self.entry5.get())
        self.top9.destroy()
        self.edit_balance("deposit")
        top = Toplevel()
        top.geometry("400x300")
        top.configure(background="#1ae8d3")
        label = Label(top,text="Successful")
        label.configure(background="#1ae8d3")
        label.pack()
        self.destroyTimer(6,top)


    def deposit_win(self):
        self.top4.destroy()
        self.top9 = Toplevel()
        self.top9.geometry("400x300")
        self.top9.configure(background="#1ae8d3")
        label = Label(self.top9,text="Enter the amount to deposit in rupees")
        label.configure(background="#1ae8d3")
        label.pack()
        self.entry5 =Entry(self.top9,width=30)
        self.entry5.pack() 
        btn = Button(self.top9,text="Continue",command=self.deposit_check)
        btn.pack()
        self.destroyTimer(20,self.top9)

    def change_pin1(self):
        self.top4.destroy()
        self.top6 = Toplevel()
        self.top6.geometry("400x300")
        self.top6.configure(background="#1ae8d3")
        label = Label(self.top6,text="Enter your current pin")
        label.configure(background="#1ae8d3")
        label.pack()
        self.entry1 = Entry(self.top6,width=20)
        self.entry1.pack()
        btn = Button(self.top6,text="Continue",command=self.change_pin2)
        btn.pack()

    def change_pin2(self):
        print(self.pin)
        if (int(self.entry1.get()) == self.pin):
            self.top6.destroy()
            self.top7 = Toplevel()
            self.top7.geometry("400x300")
            self.top7.configure(background="#1ae8d3")
            label = Label(self.top7,text="Enter new pin")
            label.configure(background="#1ae8d3")
            label.pack()
            self.entry3 = Entry(self.top7,width=20)
            self.entry3.pack()
            btn = Button(self.top7,text="Continue",command=self.change_pin3)
            btn.pack()
            self.destroyTimer(20,self.top7)
        else:
            self.top6.destroy()
            top = Toplevel()
            top.geometry("400x300")
            top.configure(background="#1ae8d3")
            label = Label(top,text="Wrong pin")
            label.configure(background="#1ae8d3")
            label.pack()
            self.destroyTimer(6,top)

    def change_pin3(self):
        new_pin = int(self.entry3.get())
        self.top7.destroy()
        print(new_pin)
        self.pin = new_pin
        self.edit_balance("pin")
        top = Toplevel()
        top.geometry("400x300")
        top.configure(background="#1ae8d3")
        label = Label(top,text="Pin changed successful")
        label.configure(background="#1ae8d3")
        label.pack()
        self.destroyTimer(6,top)
        

    def check_balance(self):
        self.top4.destroy()
        self.edit_balance("check balance")
        top5 = Toplevel()
        top5.geometry("400x300")
        top5.configure(background="#1ae8d3")
        label = Label(top5,text=self.balance)
        label.configure(background="#1ae8d3")
        label.pack()
        self.destroyTimer(10,top5)


    def transaction_info(self):
        details = list(self.cur.execute('SELECT trans,amount,balance,datetime FROM Trans WHERE account_id=? ORDER BY id DESC LIMIT ?',(self.account_id,5)))
        self.top4.destroy()
        top = Toplevel()
        top.geometry("1280x720")
        title = ('Date','Time','Transaction ',' Amount ',' Balance')
        for i in range(5):
            Label(top,text=title[i]).grid(row=0,column=i)
        for i in range(len(details),0,-1):
            trans,amount,balance,datetime = details[i-1]
            text=(str(datetime).split(' ')[0]+' ',str(datetime).split(' ')[1],trans,str(amount),str(balance))
            for j in range(5):
                Label(top,text=text[j]).grid(row=i+1,column=j)
        top.after(10000,top.destroy)

atm = Atm(root)

root.mainloop()

print('after call')
