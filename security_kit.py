from itsdangerous import URLSafeTimedSerializer

from app import app


class SecurityKit:

    @staticmethod
    def crypt_decode(data, expiration=86400):
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

        try:
            return serializer.loads(
                data,
                salt=app.config['SECURITY_PASSWORD_SALT'],
                max_age=expiration
            )
        except Exception as e:
            return None

    @staticmethod
    def crypt_encode(value):
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

        return serializer.dumps(value, salt=app.config['SECURITY_PASSWORD_SALT'])
