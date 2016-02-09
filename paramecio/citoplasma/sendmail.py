#!/usr/bin/python3
import os
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

    ssl=True
    
    txt_error=''

    def __init__(self):

        self.smtp=smtplib.SMTP(host=self.host, port=self.port)
    
    def send(self, from_address, to_address, subject, message, content_type='plain', attachments=[]):
        
        if self.ssl==True:
            
            try:
            
                self.smtp.starttls()
                
            except smtplib.SMTPHeloError:
                
                self.txt_error='Error: cannot make HELO to this server'
                
                return False

            except RuntimeError:
                
                self.txt_error='Error: SSL/TLS is not supported in your python interpreter'
                
                return False
            
            except smtplib.SMTPException as e:
                
                self.txt_error=e.__str__
                
                return False
            
            """
            except smtplib.SMTPNotSupportedError:
                
                self.txt_error='Error: SSL/TLS is not supported'
                
                return False
            """
        
        if self.username!='':
            
            try:
            
                self.smtp.login(self.username, self.password)
                
            except smtplib.SMTPHeloError:
                
                self.txt_error='Error: cannot make HELO to this server'
                
                return False
            
            except smtplib.SMTPAuthenticationError:
                
                self.txt_error='Error: cannot login. Wrong username or password'
                
                return False
            
            except smtplib.SMTPException:
                
                self.txt_error='Error: any method for login is avaliable'
                
                return False
            
            """
            except smtplib.SMTPNotSupportedError:
                
                self.txt_error='Error: AUTH is not supported'
                
                return False
            """

        COMMASPACE=', '

        if len(attachments)==0:
            
            msg=MIMEText(message, content_type)
            
            msg['Subject']=subject
            msg['From']=from_address
            
            msg['To']=COMMASPACE.join(to_address)
            
            self.smtp.send_message(msg)
            
            return True

        else:
            
            outer=MIMEMultipart()
            
            outer['Subject']=subject
            outer['From']=from_address
            
            outer['To']=COMMASPACE.join(to_address)
            
            # Attach message text
            
            msg=MIMEText(message, content_type)
            
            outer.attach(msg)
            
            for path in attachments:
                
                ctype, encoding = mimetypes.guess_type(path)
                
                if ctype is None or encoding is not None:
                    # No guess could be made, or the file is encoded (compressed), so
                    # use a generic bag-of-bits type.
                    ctype = 'application/octet-stream'
                    
                maintype, subtype = ctype.split('/', 1)
                
                if maintype == 'text':
                    with open(path) as fp:
                            # Note: we should handle calculating the charset
                        msg = MIMEText(fp.read(), _subtype=subtype)
                        
                elif maintype == 'image':
                    with open(path, 'rb') as fp:
                        msg = MIMEImage(fp.read(), _subtype=subtype)
                
                elif maintype == 'audio':
                    with open(path, 'rb') as fp:
                        msg = MIMEAudio(fp.read(), _subtype=subtype)
                
                else:
                    with open(path, 'rb') as fp:
                        msg = MIMEBase(maintype, subtype)
                        msg.set_payload(fp.read())
                    # Encode the payload using Base64
                    encoders.encode_base64(msg)
                
                # Set the filename parameter
                msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(path))
                    
                outer.attach(msg)
            
            self.smtp.send_message(outer)
            
            return True
        
    def quit(self):
        
        self.smtp.quit()
            