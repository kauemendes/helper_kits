import hashlib
import random
import re
import string
import unicodedata

from itsdangerous import URLSafeTimedSerializer

from Crypto import Random
from Crypto.Cipher import AES
import base64

from app import app


class StringKit:

    @staticmethod
    def random_key(size):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))

    @staticmethod
    def has_any_substring(value, substrings: list):
        if not value:
            return False

        for substring in substrings:
            if value.find(substring) >= 0:
                return True

        return False

    @staticmethod
    def has_all_substring(value, substrings: list):
        if not value:
            return False

        for substring in substrings:
            if not value.find(substring) >= 0:
                return False

        return True

    @staticmethod
    def string_sha1(value: str):
        hash_to_make = hashlib.sha1()
        hash_to_make.update((value + app.config['SECRET_KEY']).encode())
        return hash_to_make.hexdigest()

    @staticmethod
    def string_sha2(value: str):
        hash_to_make = hashlib.sha256()
        hash_to_make.update((value + app.config['SECRET_KEY']).encode())
        return hash_to_make.hexdigest()

    @staticmethod
    def string_md5(value: str):
        hash_to_make = hashlib.md5()
        hash_to_make.update((value + app.config['SECRET_KEY']).encode())
        return hash_to_make.hexdigest()

    @staticmethod
    def normalize_string(text):
        return ''.join((c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')).lower()

    @staticmethod
    def generate_confirmation_token(email):
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

    @staticmethod
    def confirm_token(token, expiration=3600):
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        try:
            email = serializer.loads(
                token,
                salt=app.config['SECURITY_PASSWORD_SALT'],
                max_age=expiration
            )
        except:
            return False
        return email

    @staticmethod
    def password_check(password):
        """
        Verify the strength of 'password'
        Returns a dict indicating the wrong criteria
        A password is considered strong if:
            8 characters length or more
            1 digit or more
            1 symbol or more
            1 uppercase letter or more
            1 lowercase letter or more
        """

        # calculating the length
        length_error = len(password) < 6

        # searching for digits
        digit_error = re.search(r"\d", password) is None

        # searching for uppercase
        uppercase_error = re.search(r"[A-Z]", password) is None

        # searching for lowercase
        lowercase_error = re.search(r"[a-z]", password) is None

        # searching for symbols
        symbol_error = re.search(r"\W", password) is None

        # overall result
        password_ok = not (length_error or digit_error or uppercase_error or lowercase_error or symbol_error)

        return {
            'length_error': length_error,
            'digit_error': digit_error,
            'uppercase_error': uppercase_error,
            'lowercase_error': lowercase_error,
            'symbol_error': symbol_error,
        }

    @staticmethod
    def _pad(s):
        return s + (32 - len(s) % 32) * chr(32 - len(s) % 32)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]

    @staticmethod
    def encrypt(raw):
        raw = StringKit._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(app.config['SECRET_KEY'], AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    @staticmethod
    def decrypt(enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(app.config['SECRET_KEY'], AES.MODE_CBC, iv)
        return StringKit._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    @staticmethod
    def encode_b64(msg_text):
        # transform into 64 bits
        msg_text = msg_text.rjust(32)
        cipher = AES.new(app.config['SECRET_KEY'], AES.MODE_ECB)
        encoded = base64.b64encode(cipher.encrypt(msg_text))
        return encoded

    @staticmethod
    def decode_b64(encoded_text):
        cipher = AES.new(app.config['SECRET_KEY'], AES.MODE_ECB)
        decoded = cipher.decrypt(base64.b64decode(encoded_text))

        return decoded.strip()

    @staticmethod
    def encode(value):
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        return serializer.dumps(value, salt=app.config['SECURITY_PASSWORD_SALT'])

    @staticmethod
    def decode(token, expiration=432000):
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        try:
            value = serializer.loads(
                token,
                salt=app.config['SECURITY_PASSWORD_SALT'],
                max_age=expiration
            )
        except:
            return False
        return value

    @staticmethod
    def mask_email(email):
        str_spt = email.split("@")
        email = str_spt[0]
        str_len = len(email)

        first = email[0]
        last = email[str_len - 1]

        return first + last + "@" + str_spt[1]