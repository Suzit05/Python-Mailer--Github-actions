import smtplib
from email.mime.text import MIMEText  # Corrected import
from email.mime.multipart import MIMEMultipart  # Corrected typo
import os

def send_mail(workflow_name, repo_name, workflow_run_id):
    # Email details
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    receiver_email = os.getenv('RECEIVER_EMAIL')

    # Email message
    subject = f"Workflow {workflow_name} has failed in {repo_name}"
    body = f"""Hi, the workflow {workflow_name} has failed for repo {repo_name}.
Please check the logs for more details.

More details:
Run ID: {workflow_run_id}
"""

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, 'plain'))  # Fixed class name

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)  # Fixed argument
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

# Call the function
send_mail(
    os.getenv('WORKFLOW_NAME'),
    os.getenv('REPO_NAME'),
    os.getenv('WORKFLOW_RUN_ID')
)
