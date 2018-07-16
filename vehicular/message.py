"""
Contains Message class
"""
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from typing import List

from feedparser import FeedParserDict
from jinja2 import Environment, PackageLoader, select_autoescape

from vehicular.config import Config


class Message:
    """
    Composes and sends email messages
    """
    def __init__(self, username: str,
                 password: str,
                 recipient: str,
                 hits: List[FeedParserDict]):
        """

        :param username:
        :param password:
        :param hits: list of FeedParserDicts, which are new search hits.
        """
        self.username = username
        self.password = password
        self.recipient = recipient
        self.hits = hits
        self.html = None
        self.text = None

    def send(self) -> None:
        """
        Composes and sends email using the credentials supplied in __init__
        :return: None
        """
        self.render_html()
        self.render_text()
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Craigslist Post Matches'
        msg['From'] = self.username

        text = MIMEText(self.text, 'plain')
        msg.attach(text)

        html = MIMEText(self.html, 'html')
        msg.attach(html)

        server = smtplib.SMTP(host=Config.hostname, port=Config.port)
        server.starttls()
        server.login(user=self.username, password=self.password)
        server.sendmail(self.username, self.recipient, msg.as_string())
        server.quit()

    def render_html(self) -> None:
        """
        Renders HTML email body
        :return: None
        """
        env = Environment(
            loader=PackageLoader('vehicular', 'templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )
        template = env.get_template('base.html')
        self.html = template.render(listings=self.hits)

    def render_text(self) -> None:
        """
        Renders text email body
        :return: None
        """
        env = Environment(
            loader=PackageLoader('vehicular', 'templates'),
            autoescape=select_autoescape(['.txt'])
        )
        template = env.get_template('base.txt')
        self.text = template.render(listings=self.hits)
