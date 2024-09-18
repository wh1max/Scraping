import requests
import xlwt
from xlwt import Workbook
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import *
import smtplib
from email.utils import COMMASPACE
from importlib.metadata import files
from optparse import Values
import time

URL = "https://remoteok.com/api/" # website API to be scraped.
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0' # User Agent can be changed depending on the browser you use.
REQUEST_HEADER = {
    'User-Agent': USER_AGENT,
    'Accept-Language': 'en-US, en;q=0.5'
}

def get_job_posting():
    print("Requesting Data ...")
    time.sleep(3)
    req = requests.get(url=URL, headers=REQUEST_HEADER)
    return req.json()

def output_jobs_to_xls(data):
    wb = Workbook()
    job_sheet = wb.add_sheet('Jobs')
    header = list(data[0].keys())
    for i in range(0, len(header)):
        job_sheet.write(0, i, header[i])
    for i in range(0, len(data)):
        job = data[i]
        values = list(job.values())
        for x in range(0, len(values)):
            job_sheet.write(i+1, x, values[x])
    print("Saving Data ..")
    time.sleep(3)
    wb.save('remote.xls')

def send_email(send_from, send_to, subject, text, files=None):
    assert isinstance(send_to, list)
    msg = MIMEMultipart()
    msg['FROM'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, 'rb') as fil:
            part = MIMEApplication(fil.read(), Name=basename(f))
        part['Content-Disposition'] = f'attachment; filename="{basename(f)}"'
        msg.attach(part)
    print("Sending Data .")
    time.sleep(2)
    smtp = smtplib.SMTP("Smtp Domain: Port")
    smtp.starttls()
    smtp.login(send_from, "Your Password")
    smtp.sendmail(send_from, send_to, msg.as_string())
    print("Data has been sent successfully.")
    smtp.close()

if __name__ == "__main__":
    json = get_job_posting()[1:] # Get the data from website starting from index 1.
    output_jobs_to_xls(json) # Save the data into xls format.
    send_email('send_from', ['send_to'], 'Subject',
               'Text', files=['remote.xls']) # Send the data to email.
