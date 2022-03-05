from email.message import EmailMessage
from smtplib import SMTP_SSL
import ssl




class EmailSender:
    """
    This class is used for attaching the screenshots of the pages and sending them to an email
    """

    # Since this is a basic gmail account made specially for this purpose, e.g there is no sensitive data in it,
    # I'm allowing myself to hardcode the password. BUT in a real case scenario I would store it in a .env file
    # and read it as an environmental variable, so it is not visible. But no need for fancy stuff here.#

    user = "Xplora.mailbot@gmail.com"
    password = "Xplora16!"
    default_body = "Hey, Marketing Ninja. " \
                   "It's me the X_Bot and I'm sending you the" \
                   " requested ScreenCapture file. Enjoy!"

    # First we construct the mail and then we send it
    @classmethod
    def build_mail(cls, recipient, attachment, body=default_body):
        cls.message = EmailMessage()
        cls.message["From"] = cls.user
        cls.message["To"] = recipient
        cls.message['Subject'] = "Competitors Analysis"
        cls.message.set_content(body)
        cls._attach_file(attachment)

    @classmethod
    def send_mail(cls):
        context = ssl.create_default_context()
        mail_server = SMTP_SSL('smtp.gmail.com',465,context=context)
        mail_server.login(cls.user, cls.password)
        mail_server.send_message(cls.message)
        mail_server.quit()

    # Private method used only by the build_mail method for attaching of a file
    @classmethod
    def _attach_file(cls, attachment):
        with open(attachment,"rb") as file:
            cls.message.add_attachment(file.read(),
                                       maintype="application",
                                       subtype="pdf",
                                       filename="Competitor_Analysis")


if __name__ == "__main__":

    # Used for testing during development

    email_sender=EmailSender
    email_sender.build_mail(recipient="mussashi50@gmail.com",
                            attachment="D:\\Programming\\Work_Projects\\ScrenshotAppWEB\\Project\\Ad_library_screens/screenshots_14_01/Ads_Preview_14_01.pdf",
                             )
    email_sender.send_mail()

