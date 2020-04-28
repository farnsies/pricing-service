__author__ = 'mrf'

import re
from passlib.hash import pbkdf2_sha512

EMAIL_RE = re.compile(r'^[\w-]+@([\w-]+\.)+[\w]+$')


class Utils:
    @staticmethod
    def email_is_valid(email: str) -> bool:
        return True if EMAIL_RE.match(email) else False

    @staticmethod
    def hash_password(password: str) -> str:
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password: str, hashed_password: str) -> bool:
        return pbkdf2_sha512.verify(password, hashed_password)
