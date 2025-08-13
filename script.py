import smtplib 
from email.mime.text import MIMETEXT #represent text of the email
from email.mime.mutlipart import MIMEMultipart #represent email message itself

import os

def send_mail(workflow_name, repo_name ,workflow_run_id):
    #Email details
    sender_email= os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    receiver_email= os.getenv('RECEIVER_EMAIL')

    #Email message
    subject=f"Workflow {workflow_name} has been failed in {repo_name}"
    body = f"""Hi, the workflow {workflow_name} has failed for repo {repo_name}.
    Please check the logs for more details.
    More details:
    Run ID: {workflow_run_id}"""

    msg= MIMEMultipart()
    msg["FROM"]=sender_email
    msg["TO"]=receiver_email
    msg["SUBJECT"]= subject
    msg.attach(MIMETEXT(body,'plain'))

    try:
        server= smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(sender_email,sender_password)
        text= msg.as_string()
        server.sendmail(sender_email,sender_password,text)
        server.quit()

        print("Email sent successfully")

    except Exception as e:
        print(f"Error: {e}")

#call the function

send_mail(os.getenv('WORKFLOW_NAME'), os.getenv('REPO_NAME'), os.getenv('WORKFLOW_RUN_ID'))