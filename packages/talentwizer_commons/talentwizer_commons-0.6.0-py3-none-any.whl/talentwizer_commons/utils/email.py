import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.message import EmailMessage
from urllib.parse import unquote
from pydantic import BaseModel, EmailStr
from google.oauth2.credentials import Credentials
from google.auth.exceptions import RefreshError
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from msal import ConfidentialClientApplication
import requests
from talentwizer_commons.app.engine import get_chat_engine
from llama_index.core.chat_engine.types import BaseChatEngine
from google.auth.transport.requests import Request
from fastapi import APIRouter, HTTPException, Request, Depends
from dotenv import load_dotenv
from typing import List, Optional
import base64
import os
load_dotenv()
import logging

email_router = e = APIRouter()

class TokenData(BaseModel):
    accessToken: str
    refreshToken: str
    clientId: str
    clientSecret: str
    idToken: str
    userEmail: str
    scope: str

class EmailPayload(BaseModel):
    from_email: Optional[EmailStr] = None
    to_email: Optional[List[EmailStr]] = None
    cc: Optional[List[EmailStr]] = None
    subject: Optional[str] = None
    body: Optional[str] = None
    attachments: Optional[List[str]] = None

@e.post("/send/admin")    
async def send_email_by_admin_account(emailPayload: EmailPayload):
    from_email = os.getenv("ADMIN_EMAIL")
    if not from_email:
        logging.error("Admin email is not set in environment variables")
        return False

    to_email = emailPayload.to_email
    subject = emailPayload.subject
    body = emailPayload.body
    attachments = emailPayload.attachments

    comma_separated_emails = ",".join(to_email) if to_email else ""
    if not comma_separated_emails:
        logging.error("Recipient email addresses are empty or malformed")
        return False

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = unquote(comma_separated_emails)

    if subject:
        msg['Subject'] = subject
    else:
        logging.warning("Email subject is empty")

    if body:
        msg.attach(MIMEText(body, 'plain'))
    else:
        logging.warning("Email body is empty")

    # Attach files if any
    if attachments:
        for attachment_path in attachments:
            try:
                with open(attachment_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    filename = os.path.basename(attachment_path)
                    part.add_header('Content-Disposition', f'attachment; filename={filename}')
                    msg.attach(part)
            except FileNotFoundError:
                logging.error(f"Attachment file not found: {attachment_path}")
            except PermissionError:
                logging.error(f"Permission denied for attachment file: {attachment_path}")
            except Exception as e:
                logging.error(f"Unexpected error attaching file {attachment_path}: {e}")
    
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(from_email, os.getenv("ADMIN_EMAIL_PASSWORD"))
        s.sendmail(from_email, unquote(comma_separated_emails), msg.as_string())
        s.quit()
        logging.info("Email sent successfully through admin email")
        return True
    except smtplib.SMTPAuthenticationError:
        logging.error("SMTP authentication failed. Check ADMIN_EMAIL and ADMIN_EMAIL_PASSWORD")
    except smtplib.SMTPConnectError as e:
        logging.error(f"SMTP connection error: {e}")
    except smtplib.SMTPRecipientsRefused:
        logging.error(f"All recipients were refused: {comma_separated_emails}")
    except smtplib.SMTPException as e:
        logging.error(f"SMTP error occurred: {e}")
    except Exception as e:
        logging.error(f"Unexpected error while sending email: {e}")
    return False
        
def create_message(emailPayload):
    sender = emailPayload.from_email
    to = emailPayload.to_email
    subject = emailPayload.subject
    message_text = emailPayload.body

    # Ensure the message_text is properly formatted as HTML
    message_text = f"""
    <html>
    <head></head>
    <body>
        {message_text}
    </body>
    </html>
    """

    # Convert the list of to_email addresses to a comma-separated string
    to_emails = ', '.join(to) if to else ''

    # Create the email message
    message = MIMEMultipart('alternative')
    message['to'] = to_emails
    message['from'] = sender
    message['subject'] = subject

    print("original msg :: " + message_text)

    # Attach the message text as HTML
    html_part = MIMEText(message_text, 'html', 'utf-8')
    message.attach(html_part)

    print("html msg :: " + str(message))

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw_message}


def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        logging.info('Message Id: %s' % message['id'])
        logging.info('Message Id: %s' % message['id'])
        return message
    except HttpError as error:
        logging.error('An error occurred: %s' % error)
        return None

@e.post("/send")
async def send_email_from_user_email(tokenData: dict, emailPayload: EmailPayload):
    def send_message_gmail(service, user_id, message):
        # Send email via Gmail API
        service.users().messages().send(userId=user_id, body=message).execute()

    def send_message_microsoft(access_token, payload):
        # Ensure payload is converted to a dictionary or JSON
        url = "https://graph.microsoft.com/v1.0/me/sendMail"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        # Convert EmailPayload to a dictionary if it's not already
        if isinstance(payload, EmailPayload):
            payload_dict = {
                "message": {
                    "subject": payload.subject,
                    "body": {
                        "contentType": "HTML",  # Ensure content type is HTML
                        "content": payload.body
                    },
                    "toRecipients": [{"emailAddress": {"address": email}} for email in payload.to_email]
                }
            }
            if payload.cc:
                payload_dict["message"]["ccRecipients"] = [
                    {"emailAddress": {"address": email}} for email in payload.cc
                ]
            if payload.attachments:
                payload_dict["message"]["attachments"] = payload.attachments
        else:
            payload_dict = payload  # Assume it's already in a serializable format

        response = requests.post(url, headers=headers, json=payload_dict)
        if response.status_code not in (200, 202):
            raise RuntimeError(f"Error sending email via Microsoft Graph API: {response.text}")

    try:
        # Determine the provider based on scopes
        if "https://www.googleapis.com/auth/gmail.send" in tokenData.get("scope", ""):
            # Handle Gmail account
            SCOPES = tokenData["scope"].split()
            creds = Credentials(
                token=tokenData["accessToken"],
                refresh_token=tokenData["refreshToken"],
                token_uri="https://oauth2.googleapis.com/token",
                client_id=tokenData["clientId"],
                client_secret=tokenData["clientSecret"],
                scopes=SCOPES
            )
            try:
                gmail_service = build('gmail', 'v1', credentials=creds)
                message = create_message(emailPayload)
                send_message_gmail(gmail_service, 'me', message)
                return {"status_code": 200, "message": "Email sent successfully."}
            except RefreshError:
                # Refresh token logic for Gmail
                creds.refresh(Request())
                tokenData["accessToken"] = creds.token
                tokenData["refreshToken"] = creds.refresh_token
                gmail_service = build('gmail', 'v1', credentials=creds)
                message = create_message(emailPayload)
                send_message_gmail(gmail_service, 'me', message)
                return {"status_code": 200, "message": "Email sent successfully after token refresh."}

        elif "Mail.Send" in tokenData.get("scope", ""):
            # Handle Microsoft account
            access_token = tokenData["accessToken"]
            refresh_token = tokenData["refreshToken"]
            client_id = tokenData["clientId"]
            client_secret = tokenData["clientSecret"]
            authority = tokenData.get("authority", "https://login.microsoftonline.com/common")

            try:
                send_message_microsoft(access_token, emailPayload)
                return {"status_code": 200, "message": "Email sent successfully."}
            except RuntimeError:
                # Refresh token logic for Microsoft
                app = ConfidentialClientApplication(
                    client_id, authority=authority, client_credential=client_secret
                )
                result = app.acquire_token_by_refresh_token(refresh_token, scopes=["Mail.Send"])
                if "access_token" in result:
                    tokenData["accessToken"] = result["access_token"]
                    send_message_microsoft(result["access_token"], emailPayload)
                    return {"status_code": 200, "message": "Email sent successfully after token refresh."}
                else:
                    raise RuntimeError("Failed to refresh Microsoft token.")

        else:
            raise ValueError("Unsupported email provider or missing scope in tokenData.")

    except Exception as e:
        logging.error("Unexpected error while sending email", exc_info=True)
        raise RuntimeError(f"Unexpected error: {str(e)}") from e


@e.get("/generate")
async def generate_personalised_email(
    company_name:str,
    person_name: str,
    person_summary: str,
    title: str,
    chat_engine: BaseChatEngine = Depends(get_chat_engine),
):
    prompt = "You are an expert recruiter and co-pilot for recruitment industry. "
    prompt += "Help generate a Email based on Job Title, Person Summary and Person Name to be sent to the potential candidate. " 
    prompt+= "Company Name: " + company_name +"\n"
    
    if(person_name!=""):
      prompt += "Person Name: " + str(person_name) + "\n"
      
    prompt += "Person Summary:" + str(person_summary) + "\n"
    prompt += "Job Title:" + str(title) + "\n"
    
    prompt += "Try to Write like this: Hi Based on your description your profile is being shortlisted/rejeected etc. Try to Write in about 150 words. Do not Add Any Types Of Salutations. At Ending Just Write Recruiting Team and There Company Name"
    response=chat_engine.chat(prompt)
    return response.response


@e.get("/generate/summary")
async def generate_summary(
    job_title: str,
    person_summary: str
):
    chat_engine: Optional[BaseChatEngine] = None
    try:
        # Validate inputs
        if not job_title.strip():
            raise ValueError("Job title cannot be empty.")
        if not person_summary.strip():
            raise ValueError("Person summary cannot be empty.")

        # Prepare the prompt
        prompt = (
            "You are an expert recruiter and co-pilot for the recruitment industry. "
            f"Job Title: {job_title}\n"
            f"Person Summary: {person_summary}\n"
            "Summarise person's experience and expertise based on the given Person Summary "
            "in the context of an interview mail. Personalise the content as if you are "
            "writing an email or talking to the candidate directly to show him/her as the best fit for the job. \n"
            "The email should be concise and engaging.\n"
            "Example:  based on your experience and expertise, you are a perfect fit for the job. "
            "Do not write full email content but just a summary of the candidate's experience with "
            "regard to the given job title. Try to summarise in about 50 to 60 words."
        )

        # Resolve chat_engine if not provided
        if chat_engine is None:
            chat_engine = get_chat_engine()

        # Call the chat engine
        response = chat_engine.chat(prompt)
        
        # Ensure the response is valid
        if not response or not hasattr(response, "response"):
            raise ValueError("Chat engine did not return a valid response.")

        return response.response

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while generating the summary.")


# Utility function to replace placeholders in the email template
async def populate_template_v1(template: str, person: dict, job_title: str) -> str:
    """
    Populates a template with data from the provided person and job title. 

    Args:
        template: The template string with placeholders.
        person: A dictionary containing information about the person.
        job_title: The target job title.

    Returns:
        The populated template string.

    Raises:
        ValueError: If the input parameters are invalid.
        HTTPException: If an error occurs during template population.
    """

    try:
        # Validate inputs
        if not isinstance(template, str) or not template.strip():
            raise ValueError("Template must be a non-empty string.")
        if not isinstance(person, dict):
            raise ValueError("Person must be a dictionary.")
        if not isinstance(job_title, str) or not job_title.strip():
            raise ValueError("Job title must be a non-empty string.")

        # Generate the brief summary
        brief_summary: Optional[str] = await generate_summary(job_title, person.get("summary", ""))

        if not brief_summary:
            raise ValueError("Failed to generate a brief summary for the candidate.")

        # Replace placeholders conditionally
        populated_template = template

        if "{{First Name}}" in template:
            populated_template = populated_template.replace("{{First Name}}", person.get("name", "Candidate"))

        if "{{Current Company}}" in template:
            populated_template = populated_template.replace("{{Current Company}}", person.get("work_experience", [{}])[0].get("company_name", "Company")) 

        if "{{Current Job Title}}" in template:
            # populated_template = populated_template.replace("{{Current Job Title}}", person.get("occupation", "Job Title"))
             populated_template = populated_template.replace("{{Current Job Title}}", person.get("work_experience", [{}])[0].get("designation", "Job Title")) 
        if "{*Brief mention of the candidate’s relevant skills.*}" in template:
            populated_template = populated_template.replace("{*Brief mention of the candidate’s relevant skills.*}", brief_summary)

        return populated_template

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while populating the template.")

async def populate_template_v2(template: str, person: dict, job_title: str) -> str:
    try:
        # Validate inputs
        if not isinstance(template, str) or not template.strip():
            raise ValueError("Template must be a non-empty string.")
        if not isinstance(person, dict):
            raise ValueError("Person must be a dictionary.")
        if not isinstance(job_title, str) or not job_title.strip():
            raise ValueError("Job title must be a non-empty string.")

        # Fetch values with defaults
        full_name = person.get("full_name", "Candidate")
        current_company = person.get("experience", [{}])[0].get("company_name", "Company")
        person_job_title = person.get("experience", [{}])[0].get("title", "Title")
        summary = person.get("summary", "skills and experience")

        # Generate the brief summary
        brief_summary: Optional[str] = await generate_summary(job_title, summary)

        if not brief_summary:
            raise ValueError("Failed to generate a brief summary for the candidate.")

        # Replace placeholders in the template
        populated_template = (
            template.replace("{{Full Name}}", full_name)
            .replace("{{Current Company}}", current_company)
            .replace("{{Current Job Title}}", person_job_title)
            .replace("{{Client Company}}", "our company")
            .replace("{*Brief mention of the candidate’s relevant skills.*}", brief_summary)
            .replace("{{Client Job Title}}", job_title)
        )

        return populated_template

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while populating the template.")
    
async def send_failure_report(reports: List[dict]):
    try:
        for report in reports:
            report_payload = EmailPayload(
                to_email=[report["to_email"]],
                subject=report["subject"],
                body=report["body"]
            )
            await send_email_by_admin_account(report_payload)
    except Exception as e:
        logging.error("Failed to send failure report emails", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to send failure report emails: {str(e)}")
