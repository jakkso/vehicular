"""
Contains utility functions
"""
import smtplib

from vehicular.config import Config


def credential_validation(user: str, pw: str) -> bool:
    """
    Creates a simple smtp server and attempts to log in to server using the
    provided credentials. If the login attempt was successful, returns True,
    False otherwise
    :return: bool
    """
    server = smtplib.SMTP(host=Config.hostname, port=Config.port)
    server.starttls()
    try:
        status_code, *_ = server.login(user=user, password=pw)
        server.quit()
        if status_code == 235:
            return True
    except smtplib.SMTPAuthenticationError:
        pass
    return False
