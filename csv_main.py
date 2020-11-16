import csv
from datetime import datetime as dt, timedelta
from tkinter import *
import os
from face_cap import Capture
#import threading


file = 'acc.csv' #file location

root = Tk()
root.attributes('-zoomed', True)
#root.geometry("1280x720")
root.resizable(0,0)
root.configure(background="#1ae8d3")
#w, h = root.winfo_screenwidth(),root.winfo_screenheight()
label = Label(root,text="Welcome To ATM")
label.configure(background="#1ae8d3")
label.pack(pady=50)

class Audios():
    def f(self):    
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
    balance = 0
    card_state = ''
    pin_count = 0
    unblock_time = dt.now()

    def __init__(self,root):
        self.btn = Button(root,text="Continue",state=ACTIVE,command=self.card_window)
        self.btn.pack(pady=20)
        root.after(1000,Audios().f)

    # create numpad
    def numpad(self,window,row=0,column=0):
        btn0 = Button(window,text = "0", padx=40,pady=20,command = lambda:self.numpad_click(window,'0'))
        btn1 = Button(window,text = "1", padx=40,pady=20,command = lambda:self.numpad_click(window,'1'))
        btn2 = Button(window,text = "2", padx=40,pady=20,command = lambda:self.numpad_click(window,'2'))
        btn3 = Button(window,text = "3", padx=40,pady=20,command = lambda:self.numpad_click(window,'3'))
        btn4 = Button(window,text = "4", padx=40,pady=20,command = lambda:self.numpad_click(window,'4'))
        btn5 = Button(window,text = "5", padx=40,pady=20,command = lambda:self.numpad_click(window,'5'))
        btn6 = Button(window,text = "6", padx=40,pady=20,command = lambda:self.numpad_click(window,'6'))
        btn7 = Button(window,text = "7", padx=40,pady=20,command = lambda:self.numpad_click(window,'7'))
        btn8 = Button(window,text = "8", padx=40,pady=20,command = lambda:self.numpad_click(window,'8'))
        btn9 = Button(window,text = "9", padx=40,pady=20,command = lambda:self.numpad_click(window,'9'))
        btn_delete = Button(window,text = "delete", padx=27,pady=20,command = lambda:self.numpad_click(window,'delete'))
        btn1_clear = Button(window,text = "clear", padx=27,pady=20,command = lambda:self.numpad_click(window,'clear'))
        
        btn0.grid(row=row+3,column=column+1)
        btn1.grid(row=row+0,column=column+0)
        btn2.grid(row=row+0,column=column+1)
        btn3.grid(row=row+0,column=column+2)
        btn4.grid(row=row+1,column=column+0)
        btn5.grid(row=row+1,column=column+1)
        btn6.grid(row=row+1,column=column+2)
        btn7.grid(row=row+2,column=column+0)
        btn8.grid(row=row+2,column=column+1)
        btn9.grid(row=row+2,column=column+2)
        btn_delete.grid(row=row+3,column=column+2)
        btn1_clear.grid(row=row+3,column=column+0)

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

    #window to enter card number
    def card_window(self):
        self.top = Toplevel()
        #self.top.geometry("400x300")
        self.top.attributes('-zoomed', True)
        self.top.configure(background="#1ae8d3")
        label = Label(self.top,text="Enter your card number")
        label.grid(row =0,column=0,pady=20,padx=100,columnspan=3)
        label.configure(background="#1ae8d3")
        self.e = Entry(self.top,width=30)
        self.e.grid(row=1,column=0,pady=20,columnspan=3)
        Button(self.top,text="Continue",command=self.search_win).grid(row=2,column=1,pady=20)
        self.destroyTimer(20,self.top)
        self.numpad(self.top,row=3)
        self.top.after(500,Audios().card_window) 

    #window to search user
    def search_win(self):
        top1 = Toplevel()
        top1.attributes('-zoomed', True)
        top1.configure(background="#1ae8d3")
        label = Label(top1,text="searching")
        label.configure(background="#1ae8d3")
        label.pack()
        #Button(top1,text="Continue",command=Capture.click).pack()
        entered_card = self.e.get()
        print(entered_card)
        self.top.destroy()
        found = self.search_user(entered_card)
        if (self.card_state == 'D' and self.unblock_time > dt.now()):
            #print("unblocked")
            #self.edit_balance('unblock')
            top1.after(3000,self.card_blocked)
            top1.after(3000,top1.destroy)
        else:
            if (self.card_state == 'D'):
                self.edit_balance('unblock')
            if found:
                print("found")
                top1.after(100,self.cam,top1,label)
                print('opening camera')
                # if Capture.clicked:
                #     top1.after(500,self.pin_window,top1)
                # else:
                #     print("not recognized")
            else:
                print('not found')
                top1.after(1000,self.not_found)
                top1.after(3000,top1.destroy)
            #print("outside is else")

    def cam(self,top1,label):
        Capture.capture(Capture)
        if Capture.clicked:
            top1.after(500,self.pin_window,top1)
            Capture.clicked=0
        else:
            label.configure(text="face not detected")
            top1.after(3000,top1.destroy)
            print("face detection failed")

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
        self.top2.destroy()
        print(self.pin)
        print(entered_pin)
        if (int(entered_pin)== self.pin):
            print("pin verified")
            self.menu()
        else:
            self.pin_count-=1
            self.edit_balance()
            if self.pin_count==0:
                self.card_blocked()
                self.edit_balance('block')#edit card state to D
            else:
                self.reenter_pin()
                print("wrong pin")

    def reenter_pin(self):
        self.top2 = Toplevel()
        #self.top2.geometry("400x300")
        self.top2.attributes('-zoomed', True)
        self.top2.configure(background="#1ae8d3")
        label = Label(self.top2,text="Re-enter your pin")
        label.grid(row=0,column=0,columnspan=3,pady=20)
        label.configure(background="#1ae8d3")
        self.e = Entry(self.top2,width=30)
        self.e.grid(row=1,column=0,columnspan=3,pady=20)
        Button(self.top2,text="Continue",command=self.check_pin).grid(row=2,column=1)
        self.numpad(self.top2,row=3)
        self.destroyTimer(20,self.top2)

        

            
    def destroyTimer(self,time,window):
        print("time remaining",time)
        if time==0:
            window.destroy()
            return
        window.after(1000,self.destroyTimer,time-1,window)
        

    def edit_balance(self,*detail):  
        print("in edit") 
        f = open(file, 'r') 
        reader = csv.reader(f)
        mylist = list(reader)
        f.close()
        mylist[self.row_num][7] = self.pin_count
        try:
            if detail[0] == 'unblock':
                mylist[self.row_num][8] = 'E'
                mylist[self.row_num][7] = 3
            if detail[0] == 'block':
                mylist[self.row_num][8] = 'D'
                mylist[self.row_num][9] = dt.now()+ timedelta(hours=24)
                print("blocked on ", dt.now())
            if detail[0]=="pin":
                print("in pin")
                print("old pin=",mylist[self.row_num][5])
                mylist[self.row_num][5] = self.pin
                print("new pin=",mylist[self.row_num][5])
            if detail[0] == "withdraw":
                mylist[self.row_num][6] = self.balance - self.withdraw_amount
            if detail[0] =="deposit":
                mylist[self.row_num][6] = self.balance + self.deposit_amount
        except:
            pass
        my_new_list = open(file, 'w', newline = '')
        csv_writer = csv.writer(my_new_list)
        csv_writer.writerows(mylist)
        my_new_list.close()


    def search_user(self,entered_card):

        with open(file,'r') as csv_file:
            data = csv.DictReader(csv_file)  
            in_row=0
            for user in data:
                in_row=in_row+1
                cards = user['CARD NO.']
                if (entered_card == cards):
                    self.row_num = in_row
                    #card_num = int(line['CARD NO.'])
                    #accont_num = int(line['ACCOUNT NO.'])
                    #name = line['NAME']
                    #dob = line['DOB']
                    self.pin = int(user['PIN'])
                    self.balance = float(user['BALANCE'])
                    self.pin_count = int(user['PIN COUNT'])
                    self.card_state = user['CARD STATE']
                    t_str = user['UNBLOCK TIME']
                    self.unblock_time = dt(int(t_str[0:4]),int(t_str[5:7]),int(t_str[8:10]),int(t_str[11:13]),int(t_str[14:16]),int(t_str[17:19]))
                    return 1
            
            return 0

    def menu(self):
        self.top4 = Toplevel()
        self.top4.attributes('-zoomed', True)
        self.top4.configure(background="#1ae8d3")
        #self.top4.geometry("400x300")
        btn1 = Button(self.top4,text="Withdraw",command=self.withdraw_win)
        btn2 = Button(self.top4,text="Deposit",command=self.deposit_win)
        btn3 = Button(self.top4,text="Change Pin",command=self.change_pin1)
        btn4 = Button(self.top4,text="Check Balance",command=self.check_balance)

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
        top5 = Toplevel()
        top5.geometry("400x300")
        top5.configure(background="#1ae8d3")
        label = Label(top5,text=self.balance)
        label.configure(background="#1ae8d3")
        label.pack()
        self.destroyTimer(10,top5)



atm = Atm(root)

root.mainloop()

print('after call')
