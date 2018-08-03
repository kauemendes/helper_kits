from helper_kits.email_kit import EmailKit

class EmailModel:
    pass


class MessageKit:

    _emailkit = None

    @staticmethod
    def dispatcher(email_to_send: object = None, email_type: EmailModel = None):
        """
        :param email_to_send:
        :param email_type:
        :param user_registration_id:
        :param push_notification_type:
        :return:
        """

        if isinstance(email_to_send, str):
            email_to_send = [email_to_send]

        MessageKit._emailkit = EmailKit()

        lOk = True

        if email_to_send and email_type:
            try:
                lOk = MessageKit._emailkit.message_dispatch(email_to_send, email_type._TEMPLATE_SUBJECT_, email_type._TEMPLATE_RENDER_)
            except Exception as e:
                return False

        return lOk
