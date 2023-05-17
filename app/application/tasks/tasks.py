from pydantic import EmailStr
from .templates.email_templates import create_booking_confirmation_template
from app.domain.shared.config.config import settings
from .celery import celery
from PIL import Image
from pathlib import Path
import smtplib

@celery.task
def process_img(
    path: str,
):
    img_path = Path(path)
    img = Image.open(img_path)
    img_resized_big = img.resize((1000, 500))
    img_resized_small = img.resize((200, 100))
    img_resized_big.save(f"app/presentation/static/images/img_big_{img_path.name}")
    img_resized_small.save(f"app/presentation/static/images/img_small_{img_path.name}")

@celery.task
def send_booking_confirmation(
    booking: dict,
    email_to: EmailStr,
):
    email_to_mock = settings.SMTP_USER
    msg_content = create_booking_confirmation_template(booking, email_to_mock)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PWD)
        server.send_message(msg_content)