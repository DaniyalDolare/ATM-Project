# Python code to illustrate Sending mail with attachments 
# from your Gmail account  
  
# libraries to be imported 
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

class Mailer():

        def mail(self,toaddr,*detail):

            print("writing the mail....")
            # print(detail)

            fromaddr = "atmproject321@gmail.com"
            #toaddr = "daniyal.dolare@gmail.com"
            
            # instance of MIMEMultipart 
            msg = MIMEMultipart() 
            
            # storing the senders email address   
            msg['From'] = fromaddr 
            
            # storing the receivers email address  
            msg['To'] = toaddr 
            
            # storing the subject  
            msg['Subject'] = "ATM Transaction Details"
            
            # string to store the body of the mail
            if detail[0]=="wrong pin":
                body = "Dear customer, someone has just accessed your account and entered wrong pin"
            elif detail[0]=="block":
                body = "Dear customer, you just entered wrong pin for 3 times, hence your card is blocked"
            elif detail[0]=="pin":
                body = "Dear customer, someone has just accessed your account and changed the pin"
            elif detail[0]=="withdraw":
                body = "Dear customer, someone has just accessed your account and debited amount="+str(detail[1])
            elif detail[0]=="deposit":
                body = "Dear customer, someone has just accessed your account and credited amount="+str(detail[1])
            elif detail[0] == "check balance":
                body = "Dear customer, someone has just accessed your account and checked balance"


            # attach the body with the msg instance 
            msg.attach(MIMEText(body, 'plain')) 
            
            # open the file to be sent  
            filename = "face.jpg"
            attachment = open("face.jpg", "rb") 
            
            # instance of MIMEBase and named as p 
            p = MIMEBase('application', 'octet-stream') 
            
            # To change the payload into encoded form 
            p.set_payload((attachment).read()) 
            
            # encode into base64 
            encoders.encode_base64(p) 
            
            p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
            
            # attach the instance 'p' to instance 'msg' 
            msg.attach(p) 
            
            # creates SMTP session 
            s = smtplib.SMTP('smtp.gmail.com', 587) 
            
            # start TLS for security 
            s.starttls() 
            
            # Authentication 
            s.login(fromaddr, "project@atm123") 
            
            # Converts the Multipart msg into a string 
            text = msg.as_string() 
            
            # sending the mail 
            s.sendmail(fromaddr, toaddr, text) 

            print("mail sent")
            
            # terminating the session 
            s.quit() 

# Mailer.mail(Mailer,"daniyal.dolare@gmail.com","check balance",)