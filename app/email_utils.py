import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import url_for, current_app
from .models import CampaignTarget

def send_phishing_email(app, campaign_target: CampaignTarget):
    with app.app_context():
        target = campaign_target.target
        campaign = campaign_target.campaign
        template = campaign.template

        open_url = url_for("tracking.track_open", token=campaign_target.unique_token, _external=True)
        click_url = url_for("tracking.track_click", token=campaign_target.unique_token, _external=True)

        # Plain text and HTML bodies from your template
        body_text = template.body_text.format(
            name=target.name or "",
            bank_name=target.bank_name or "",
            upi_id=target.upi_id or "",
            click_url=click_url,
            open_url=open_url,
        )

        body_html = template.body_html.format(
            name=target.name or "",
            bank_name=target.bank_name or "",
            upi_id=target.upi_id or "",
            click_url=click_url,
            open_url=open_url,
        )

        msg = MIMEMultipart("alternative")
        msg["Subject"] = template.subject.format(
            name=target.name or "",
            bank_name=target.bank_name or ""
        )
        msg["From"] = "training@upi-phishsim.local"
        msg["To"] = target.email
        msg["Date"] = email.utils.formatdate(localtime=True)
        msg["Message-Id"] = email.utils.make_msgid()

        # Attach text and HTML
        part_text = MIMEText(body_text, "plain")
        part_html = MIMEText(body_html, "html")

        msg.attach(part_text)
        msg.attach(part_html)

        server = smtplib.SMTP(current_app.config["MAIL_SERVER"], current_app.config["MAIL_PORT"])
        if current_app.config.get("MAIL_USE_TLS"):
            server.starttls()
        server.login(current_app.config["MAIL_USERNAME"], current_app.config["MAIL_PASSWORD"])
        server.send_message(msg)
        server.quit()