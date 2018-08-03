import os

from app import app, mailer, mail


class EmailKit:

    @staticmethod
    def message_dispatch_sendgrid(email_to: list, subject: str, body: str, *args, **kwargs) -> object:

        # converting it to array
        if type(email_to) == str:
            email_to = [email_to]

        # apenas o ambiente de development
        if os.getenv('APP_SETTINGS') == "config.DevelopmentConfig" or \
           os.getenv('APP_SETTINGS') == "config.DevelopmentContainerConfig" or \
           app.config["DEBUG"]:

            # replace for email.com.br emails with debug true making sure we are sending not to production
            for i, val in enumerate(email_to):
                val = val.split("@")[0] + "@email.com.br"
                email_to[i] = val

        to_email = []
        for m in email_to:
            key = "email"
            to_email.append({key: m})

        from_email = kwargs["from_email"] if "from_email" in kwargs else app.config['SENDGRID_DEFAULT_FROM']

        if "from_email" in kwargs:
            kwargs.pop("from_email")

        try:
            mail.send_email(
                from_email=from_email,
                to_email=to_email,
                subject=subject,
                html="<html><body><b> This is something default content </body></html>",
                *args,
                **kwargs
            )
            return True
        except Exception as e:
            raise e
