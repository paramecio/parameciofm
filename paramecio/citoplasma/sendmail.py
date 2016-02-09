#!/usr/bin/python3

import smtplib
import mimetypes
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class SendMail:
    
    port=25
    
    host='localhost'
    
    username=''
    
    password=''

    ssl=False
    
    txt_error=''

    def __init__(self):

        self.smtp=smtplib.SMTP(host=self.host, port=self.port)
    
    def send(self, from_address, to_address, subject, message, content_type='plain', attachments=[]):
        
        if self.ssl==True:
            
            try:
            
                self.smtp.starttls()
                
            except SMTPHeloError:
                
                self.txt_error='Error: cannot make HELO to this server'
                
                return False
            
            except SMTPNotSupportedError:
                
                self.txt_error='Error: SSL/TLS is not supported'
                
                return False
        
            except RuntimeError:
                
                self.txt_error='Error: SSL/TLS is not supported in your python interpreter'
                
                return False
        
        if self.username!='':
            
            try:
            
                self.smtp.login(self.username, self.password)
                
            except SMTPHeloError:
                
                self.txt_error='Error: cannot make HELO to this server'
                
                return False
            
            except SMTPAuthenticationError:
                
                self.txt_error='Error: cannot login. Wrong username or password'
                
                return False
                
            except SMTPNotSupportedError:
                
                self.txt_error='Error: AUTH is not supported'
                
                return False
            
            except SMTPException:
                
                self.txt_error='Error: any method for login is avaliable'
                
                return False

        COMMASPACE=', '

        if len(attachments)==0:
            
            msg=MIMEText(message, content_type)
            
            msg['Subject']=subject
            msg['From']=from_address
            
            msg['To']=COMMASPACE.join(to_address)
            
            self.smtp.send_message(msg)
            
            return True
            
    