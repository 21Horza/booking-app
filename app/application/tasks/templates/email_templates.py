from email.message import EmailMessage
from app.domain.shared.config.config import settings
from pydantic import EmailStr

def create_booking_confirmation_template(
        booking: dict,
        email_to: EmailStr,
):
    email = EmailMessage()

    email["Subject"] = "Booking confirmation"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
            <h1> Confirm booking </h1>
            You booked hotel from {booking["date_from"]} to {booking["date_to"]}
        """,
        subtype="html"
    )

    return email
