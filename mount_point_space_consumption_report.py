import os
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
import logging
import time
from datetime import date
import datetime


def Weekly_audit_lods_consumption(servers):
      messageArray=[]
      for node in servers:
        logging.info("Checking Audit Logs on "+node)
        out=subprocess.Popen(['ssh', 'user@'+node, 'df -h /yourmount/yourfolder'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = out.communicate()
        messageArray.append("Node : "+node)
        messageArray.append(out)
      send_email(messageArray)

def send_email(message):
      logging.info("Sending Email Alert!")
      me = "K8sBot@yourwebsite.com"
      you = "recerverEmail@yourwebsite.com"
      subject = "Space consumption report"
      
      finalArray=[]
      
      for i in range(len(message)):
          if "Node :" not in message[i]:
              tempMessage=message[i].split(" ")
              tempMessage=[x for x in tempMessage if x]
              finalArray.append(message[i-1]+"<br>"+tempMessage[8]+"/"+tempMessage[9]+" <br> Utilized Percentage : "+tempMessage[10])
          
      
      msg = MIMEMultipart('alternative')
      msg['Subject'] = subject
      msg['From'] = me
      msg['To'] = you      
      
      html = """\
      <html>
        <head>
        <title>Alert</title>
        <style>
        table, th, td {
            border: 1px solid blue;
            border-collapse: collapse;
        }
        th, td {
            padding: 5px;
        }
        strong {
          bgcolor: white;
          color: red;
        }
        </style>
        </head>
        <body>
        <table style='width:100%'>
        <tr>
            <th><strong>"""+subject+"""</strong></th>
          </tr>
          <tr>
            <td>"""+("<br><br>").join(finalArray)+"""</td>
          </tr>
        </table>
        </body></html>
      """
      part2 = MIMEText(html, 'html')
      msg.attach(part2)
      try:
        s = smtplib.SMTP('localhost')
        s.sendmail(me, you, msg.as_string())
        s.quit()         
        logging.info("Successfully sent email")
      except Exception:
       logging.error("Error: unable to send email")
      
  

def main():
  servers=["server 1","server 2","server 3"]
  Weekly_audit_lods_consumption(servers)
    
if __name__ == "__main__":
    main()
    
