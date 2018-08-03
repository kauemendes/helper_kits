from datetime import datetime


class DateKit:

    @staticmethod
    def convert_to_mysql_date_format(value):
        if value:
            return value.strftime("%Y-%m-%d %H:%M:%S")

        return None

    @staticmethod
    def convert_to_cedro_candle_date(value):
        if value:
            return value.strftime("%Y%m%d%H%M%S")

        return None

    @staticmethod
    def convert_date_to_cedro_arrow(value):
        if value:
            return value.strftime("%d-%m-%Y %H:%M:%S")

        return None

    @staticmethod
    def convert_to_date_from_format(value, format="%Y-%m-%d %H:%M:%S"):
        if value:
            return datetime.strptime(value, format)

        return None

    @staticmethod
    def convert_to_email_format(value):
        if value:
            return value.strftime("%d/%m/%Y %H:%M")

        return None

    @staticmethod
    def convert_to_url_calendar(value):
        if value:
            return value.strftime("%Y-%m-%d %H:%M:%S")

        return None

    @staticmethod
    def convert_cedro_date_to_date(value):
        """"Apr 9, 2018 12:00:00 AM """
        if value:
            return datetime.strptime(value, "%b %d, %Y %I:%M:%S %p")
        return None


    @staticmethod
    def hour_diff(
            date_1: datetime,
            date_2: datetime
    ):

        time_diff = abs(date_1.timestamp() - date_2.timestamp())
        return time_diff/60/60