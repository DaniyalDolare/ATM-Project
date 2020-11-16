from datetime import datetime as dt, timedelta
from tkinter import *
import os
import sqlite3
from face_cap import Capture
from mailer import Mailer
from qr_scanner import Scanner
import threading




root = Tk()
root.geometry("1280x720")
root.resizable(False,False)
root.configure(background="#1ae8d3")
label = Label(root,text="Welcome To ATM",font="Times 20")
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
        btn = Button(root,text="Use ATM/Debit/Credit Card",state=ACTIVE,command=self.card_window)
        btn.pack(pady=20)
        Button(root,text="Use Virtual Card",command=self.vcard_window).pack(pady=10)
        root.after(1000,Audios().welcome)

    # create numpad
    def numpad(self,root,row=0,column=0,command=''):
        b1 = Button(root,text='1',width=5,bg='SlateGray4',fg='white',height=2,font=("Times", 14,'bold'),command = lambda:self.numpad_click(root,'1'))
        b1.place(x=row+0,y=column+0)

                
        b2 = Button(root,text='2',width=5,bg='SlateGray4',fg='white',height=2,font=("Times", 14,'bold'),command = lambda:self.numpad_click(root,'2'))
        b2.place(x=row+70,y=column+0)

        b3 = Button(root,text='3',width=5,bg='SlateGray4',fg='white',height=2,font=("Times", 14,'bold'),command = lambda:self.numpad_click(root,'3'))
        b3.place(x=row+140,y=column+0)

        b4 = Button(root,text='4',width=5,bg='SlateGray4',fg='white',height=2,font=("Times", 14,'bold'),command = lambda:self.numpad_click(root,'4'))
        b4.place(x=row+0,y=column+70)

        b5 = Button(root,text='5',width=5,bg='SlateGray4',fg='white',height=2,font=("Times", 14,'bold'),command = lambda:self.numpad_click(root,'5'))
        b5.place(x=row+70,y=column+70)

            
        b6 = Button(root,text='6',width=5,bg='SlateGray4',fg='white',height=2,font=("Times", 14,'bold'),command = lambda:self.numpad_click(root,'6'))
        b6.place(x=row+140,y=column+70)

        b7 = Button(root,text='7',width=5,bg='SlateGray4',fg='white',height=2,font=("Times", 14,'bold'),command = lambda:self.numpad_click(root,'7'))
        b7.place(x=row+0,y=column+140)

        b8 = Button(root,text='8',width=5,bg='SlateGray4',fg='white',height=2,font=("Times", 14,'bold'),command = lambda:self.numpad_click(root,'8'))
        b8.place(x=row+70,y=column+140)

                
        b9 = Button(root,text='9',width=5,bg='SlateGray4',fg='white',height=2,font=("Times", 14,'bold'),command = lambda:self.numpad_click(root,'9'))
        b9.place(x=row+140,y=column+140)


        b0 = Button(root,text='0',width=5,height=2,bg='SlateGray4',fg='white',font=("Times", 14,'bold'),command = lambda:self.numpad_click(root,'0'))
        b0.place(x=row+70,y=column+210)

            
        
        b = Button(root,text='CLEAR',width=5,bg='SlateGray4',fg='white',height=2,font=("Times", 13,'bold'),command = lambda:self.numpad_click(root,'clear'))
        b.place(x=row+230,y=column+0)

        b = Button(root,text='ENTER',width=5,bg='SlateGray4',fg='white',height=2,font=("Times", 13,'bold'),command = command)
        b.place(x=row+230,y=column+70)

        b = Button(root,text='CANCEL',width=6,bg='SlateGray4',fg='white',height=2,font=("Times",12,'bold'),command = lambda:self.on_cancel(root))
        b.place(x=row+230,y=column+140)


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

    def on_cancel(self,window):
        window.destroy()
        top=Toplevel()
        top.resizable(False,False)
        top.geometry("1280x720")
        top.configure(background="#1ae8d3")
        Label(top,text="Thank you for using our ATM",font="Times 20",background="#1ae8d3").pack(pady=150)
        top.after(6000,top.destroy)


    def on_time_limit_succeeded(self):
        top=Toplevel()
        top.resizable(False,False)
        top.geometry("1280x720")
        top.configure(background="#1ae8d3")
        Label(top,text="Time limit succceeded, try doing transaction again",font="Times 20",background="#1ae8d3").pack(pady=150)
        top.after(6000,top.destroy)

    def vcard_window(self):
        self.top=Toplevel()
        self.top.resizable(False,False)
        self.top.geometry("1280x720")
        self.top.configure(background="#1ae8d3")
        self.label = Label(self.top,text="Scan the QR Code",background="#1ae8d3")
        self.label.pack(pady=5)
        self.top.after(100,self.qr_scan)


    def qr_scan(self):
        text=Scanner.scan(Scanner)
        if text:
            self.top.destroy()
            self.search_win(text)
        else:
            self.label.configure(text="QR code not found")
            self.top.after(3000,self.top.destroy)


    #window to enter card number
    def card_window(self):
        self.top = Toplevel()
        self.top.resizable(False,False)
        self.top.geometry("1280x720")
        self.top.configure(background="#1ae8d3")
        label = Label(self.top,text="Enter your card number")
        label.place(x=550,y=100)
        label.configure(background="#1ae8d3")
        self.e = Entry(self.top,width=30)
        self.e.place(x=520,y=200)
        self.destroyTimer(20,self.top)
        self.numpad(self.top,row=500,column=300,command=self.search_win)
        self.top.after(500,Audios().card_window) 

    #window to search user
    def search_win(self,*card):
        top1 = Toplevel()
        self.top1.resizable(False,False)
        top1.geometry("1280x720")
        top1.configure(background="#1ae8d3")
        label = Label(top1,text="Searching..")
        label.configure(background="#1ae8d3")
        label.pack()
        entered_card = card[0] if card else self.e.get()
        print(entered_card)
        self.top.destroy()
        found = self.search_user(entered_card)
        if found:
            label.configure(text="Scan your face")
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
        top.resizable(False,False)
        top.geometry("1280x720")
        top.configure(background="#1ae8d3")
        label = Label(top,text = 'Cannot find your details!')
        label.configure(background="#1ae8d3")
        label.pack()
        self.destroyTimer(6,top)


    def card_blocked(self):
        top = Toplevel()
        top.resizable(False,False)
        top.geometry("1280x720")
        top.configure(background="#1ae8d3")
        label = Label(top,text = 'Your card is blocked!')
        label.configure(background="#1ae8d3")
        label.pack()
        self.destroyTimer(6,top)           

    def pin_window(self,top1):  #taking top1 as argument to destroy
        top1.destroy()
        self.top2 = Toplevel()
        self.top2.resizable(False,False)
        self.top2.geometry("1280x720")
        self.top2.configure(background="#1ae8d3")
        label = Label(self.top2,text="Enter your pin")
        label.place(x=580,y=100)
        label.configure(background="#1ae8d3")
        self.e = Entry(self.top2,width=30)
        self.e.place(x=520,y=200)
        self.numpad(self.top2,row=500,column=300,command=self.check_pin)
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
        self.top2.resizable(False,False)
        self.top2.geometry("1280x720")
        self.top2.configure(background="#1ae8d3")
        label = Label(self.top2,text="Entered wrong pin...")
        label.pack()
        label.configure(background="#1ae8d3")
        self.destroyTimer(5,self.top2)

            
    def destroyTimer(self,time,window):
        # print("time remaining",time)
        if time==0:
            window.destroy()
            self.on_time_limit_succeeded()
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
        self.top4.resizable(False,False)
        self.top4.configure(background="#1ae8d3")
        self.top4.geometry("1280x720")
        label = Label(self.top4,text="Select your choice",background="#1ae8d3",font = "Times 20")
        btn1 = Button(self.top4,text="Withdraw",font = "Times 20",height=2,width=12,command=self.withdraw_win)
        btn2 = Button(self.top4,text="Deposit",font = "Times 20",height=2,width=12,command=self.deposit_win)
        btn3 = Button(self.top4,text="Change Pin",font = "Times 20",height=2,width=12,command=self.change_pin1)
        btn4 = Button(self.top4,text="Check Balance",font = "Times 20",height=2,width=12,command=self.check_balance)
        btn5 = Button(self.top4,text="Mini Statement",font = "Times 20",height=2,width=12,command=self.transaction_info)

        label.place(x=540,y=50)
        btn1.place(x=50,y=150)
        btn2.place(x=50,y=300)
        btn3.place(x=50,y=450)
        btn4.place(x=1050,y=150)
        btn5.place(x=1050,y=300)

        self.destroyTimer(20,self.top4)


    def withdraw_win(self):
        self.top4.destroy()
        self.top8 = Toplevel()
        self.top8.resizable(False,False)
        self.top8.geometry("1280x720")
        self.top8.configure(background="#1ae8d3")
        label = Label(self.top8,text="Enter the amount in rupees")
        label.configure(background="#1ae8d3")
        label.place(x=550,y=100)
        self.e =Entry(self.top8,width=30)
        self.e.place(x=510,y=200)
        self.numpad(self.top8,row=500,column=300,command=self.withdraw_check)
        self.destroyTimer(20,self.top8)

    def withdraw_check(self):
        self.withdraw_amount = float(self.e.get())
        self.top8.destroy()
        top = Toplevel()
        top.resizable(False,False)
        top.geometry("1280x720")
        top.configure(background="#1ae8d3")
        label = Label(top,background="#1ae8d3",text="Successful",font="Times 20")
        label.pack(pady=150)
        if self.withdraw_amount < self.balance :
            self.edit_balance("withdraw")
            label.configure(text="Successful")    
        else:
            label.configure(text="Insufficient balance")
        top.after(6000,top.destroy)


    def deposit_win(self):
        self.top4.destroy()
        self.top9 = Toplevel()
        self.top9.resizable(False,False)
        self.top9.geometry("1280x720")
        self.top9.configure(background="#1ae8d3")
        label = Label(self.top9,text="Enter the amount to deposit in rupees",background="#1ae8d3")
        label.place(x=510,y=100)
        self.e =Entry(self.top9,width=30)
        self.e.place(x=510,y=200)
        self.numpad(self.top9,row=500,column=300,command=self.deposit_check)
        self.destroyTimer(20,self.top9)

    def deposit_check(self):
        self.deposit_amount = float(self.e.get())
        self.top9.destroy()
        self.edit_balance("deposit")
        top = Toplevel()
        top.resizable(False,False)
        top.geometry("1280x720")
        top.configure(background="#1ae8d3")
        label = Label(top,text="Successful",font="Times 20")
        label.configure(background="#1ae8d3")
        label.pack(pady=150)
        top.after(6000,top.destroy)


    def change_pin1(self):
        self.top4.destroy()
        self.top6 = Toplevel()
        self.top6.resizable(False,False)
        self.top6.geometry("1280x720")
        self.top6.configure(background="#1ae8d3")
        label = Label(self.top6,text="Enter your current pin")
        label.configure(background="#1ae8d3")
        label.place(x=560,y=100)
        self.e = Entry(self.top6,width=30)
        self.e.place(x=520,y=200)
        self.numpad(self.top6,row=500,column=300,command=self.change_pin2)
        self.destroyTimer(20,self.top6)


    def change_pin2(self):
        entered_pin=int(self.e.get())
        self.top6.destroy()
        self.top=Toplevel()
        self.top.resizable(False,False)
        self.top.geometry("1280x720")
        self.top.configure(background="#1ae8d3")
        if (entered_pin == self.pin):
            label = Label(self.top,text="Enter new pin")
            label.configure(background="#1ae8d3")
            label.place(x=580,y=100)
            self.e = Entry(self.top,width=30)
            self.e.place(x=520,y=200)
            self.numpad(self.top,row=500,column=300,command=self.change_pin3)
            self.destroyTimer(20,self.top)
        else:
            label = Label(self.top,text="Wrong pin",font="Times 20",background="#1ae8d3")
            label.pack(pady=150)
            self.top.after(6000,self.top.destroy)

    def change_pin3(self):
        new_pin = int(self.e.get())
        self.top.destroy()
        print(new_pin)
        self.pin = new_pin
        self.edit_balance("pin")
        top = Toplevel()
        top.resizable(False,False)
        top.geometry("1280x720")
        top.configure(background="#1ae8d3")
        label = Label(top,text="Pin changed successful",font="Times 20",background="#1ae8d3")
        label.pack(pady=150)
        top.after(6000,top.destroy)
        

    def check_balance(self):
        self.top4.destroy()
        self.edit_balance("check balance")
        top5 = Toplevel()
        top5.resizable(False,False)
        top5.geometry("1280x720")
        top5.configure(background="#1ae8d3")
        label = Label(top5,text="Your current balance is "+str(self.balance),font="Times 20")
        label.configure(background="#1ae8d3")
        label.pack(pady=150)
        top5.after(10000,top5.destroy)


    def transaction_info(self):
        details = list(self.cur.execute('SELECT trans,amount,balance,datetime FROM Trans WHERE account_id=? ORDER BY id DESC LIMIT ?',(self.account_id,5)))
        self.top4.destroy()
        top = Toplevel()
        top.resizable(False,False)
        top.geometry("1280x720")
        top.configure(background="#1ae8d3")
        title = ('Date','Time','Transaction ',' Amount ',' Balance')
        for i in range(5):
            Label(top,text=title[i],background="#1ae8d3",font="Times 20").grid(row=0,column=i)
        for i in range(len(details),0,-1):
            trans,amount,balance,datetime = details[i-1]
            text=(str(datetime).split(' ')[0]+' ',str(datetime).split(' ')[1],trans,str(amount),str(balance))
            for j in range(5):
                Label(top,text=text[j],background="#1ae8d3",font="Times 20").grid(row=i+1,column=j)
        top.after(10000,top.destroy)

atm = Atm(root)

root.mainloop()

print('after call')
