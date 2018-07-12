from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from jinja2 import Environment, PackageLoader, select_autoescape

from config import Config
from database import FPIntegration


class Message:
    """
    Composes and sends email messages
    """
    def __init__(self):
        self.parser = FPIntegration
        self.html = None
        self.text = None

    def run(self) -> None:
        """
        Calls parser.run_search.  If there are results, composes and sends email
        using the credentials fetched from the database
        :return: None
        """
        hits = self.parser().run_search()
        if hits:
            self.render_html(hits)
            self.render_text(hits)
            sender, password, recipient = self.parser().credentials
            msg = MIMEMultipart('alternative')
            msg['Subject'] = 'Craigslist Post Matches'
            msg['From'] = sender

            text = MIMEText(self.text, 'plain')
            msg.attach(text)

            html = MIMEText(self.html, 'html')
            msg.attach(html)

            server = smtplib.SMTP(host=Config.HOSTNAME, port=Config.PORT)
            server.starttls()
            server.login(user=sender, password=password)
            server.sendmail(sender, recipient, msg.as_string())
            server.quit()

    def render_html(self, hits: list) -> None:
        """
        Renders HTML email body
        :param hits: list of FeedParserDicts
        :return: None
        """
        env = Environment(
            loader=PackageLoader('message', 'templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )
        template = env.get_template('base.html')
        self.html = template.render(listings=hits)

    def render_text(self, hits: list) -> None:
        """
        Renders text email body
        :param hits: list of FeedParserDicts
        :return: None
        """
        env = Environment(
            loader=PackageLoader('message', 'templates'),
            autoescape=select_autoescape(['.txt'])
        )
        template = env.get_template('base.txt')
        self.text = template.render(listings=hits)


