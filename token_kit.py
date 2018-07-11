import hashlib
from datetime import datetime
from math import floor


class TokenKit:

    @staticmethod
    def get_token(datetime_value: datetime, requested_data: str):

        salt_value = TokenKit.get_salt(datetime_value.month)

        value_to_hash = datetime_value.strftime("%Y %m %d %H %M ")
        second_to_hash = str(floor(datetime_value.second / 5))

        if len(second_to_hash) == 1:
            second_to_hash = "0" + second_to_hash

        value_to_hash = value_to_hash + second_to_hash
        value_to_hash = salt_value + ":" + value_to_hash + ":" + requested_data

        print(value_to_hash)

        return hashlib.sha1(value_to_hash.encode('utf-8')).hexdigest()

    @staticmethod
    def get_salt(month_hash_value: int):

        if month_hash_value == 1:
            return "bUo8qaXKSmwtv9VntQDQ"
        elif month_hash_value == 2:
            return "YOP9rJYEcpfn2KNvDye5"
        elif month_hash_value == 3:
            return "3WI5JGh4qJOtYVpyyQzA"
        elif month_hash_value == 4:
            return "8XVVF2SnYIDZpnd6KvnO"
        elif month_hash_value == 5:
            return "sqIVUkeYXFvls9GqeQLw"
        elif month_hash_value == 6:
            return "OmSbqVwLiTXalOzC1qaB"
        elif month_hash_value == 7:
            return "M9HYEPBvL0Le29jjNPqK"
        elif month_hash_value == 8:
            return "OT7EDYtS4eiBevKxAz8b"
        elif month_hash_value == 9:
            return "Frd6ovsBE1sgfgwctjrH"
        elif month_hash_value == 10:
            return "eJUIwqkr2jXkHUOte8tg"
        elif month_hash_value == 11:
            return "CL2iZSoU8l37GUX1HKUf"
        elif month_hash_value == 12:
            return "w8rEJW51b9ESg1KataIX"

