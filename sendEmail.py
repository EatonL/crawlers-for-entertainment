import smtplib 
from email.header import Header 
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart
import io
import os
import sys 
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8') 


class sendEmail(object):
    def __init__(self,sender,receiver,password,smtpServer='smtp.qq.com',title=None,content=None,*annex):
        self._sender=sender
        self._receiver=receiver
        self._smtpServer=smtpServer
        self._password=password
        self._title=title
        self._content=content
        self._annex=annex

    def sendMail(self):
        # 创建一个带附件的实例 
        message = MIMEMultipart() 
        message['From'] = self._sender 
        message['To'] = self._receiver 
        message['Subject'] = Header(self._title, 'utf-8') 
  
        # 邮件正文内容 
        message.attach(MIMEText(self._content, 'plain', 'utf-8')) 
        # 构造附件（附件为TXT格式的文本）
        for i in range(len(self._annex)): 
            if os.path.isfile(self._annex[i]):
                att = MIMEText(open(self._annex[i], 'rb').read(), 'base64', 'utf-8') 
                att["Content-Type"] = 'application/octet-stream'
                print(self._annex[i].encode())
                att.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', self._annex[i]))
                message.attach(att)
            else:
                print("%s does not exist!" % self._annex[i]) 
                sys.exit(1)
                
        server = smtplib.SMTP(self._smtpServer, 587) # SMTP协议默认端口是25
        server.starttls()
        #server.set_debuglevel(1)
        server.login(self._sender, self._password) 
        server.sendmail(self._sender, self._receiver, message.as_string()) 
        print("Mail sent successfully!") 
        server.quit()

def main():
    Mail=sendEmail('XXXXX@qq.com','XXXXXX@qq.com','XXXXX','smtp.qq.com',None,'ok','XXXXXX')
    Mail.sendMail()

if __name__=='__main__':
    main()
