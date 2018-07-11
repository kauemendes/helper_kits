from app.models.enums import ProcessTypeNames


class ValidationKit:

    @staticmethod
    def is_valid_process_type(process_type_value: str) -> bool:

        try:
            ProcessTypeNames(process_type_value)
            return True
        except Exception as e:
            return False

    @staticmethod
    def is_object(value) -> bool:
        if value is not None and isinstance(value, dict):
            return True

        return False

    @staticmethod
    def is_valid_string(value: str, min_char: int = 1):
        if value is not None and isinstance(value, str) and len(value) >= min_char:
            return True

        return False

    @staticmethod
    def is_valid_int(value: int, min_value: int = None, max_value: int = None):

        if value is not None and isinstance(value, int):

            if min_value is not None and value < min_value:
                return False

            if max_value is not None and value > max_value:
                return False

            return True

        return False

    @staticmethod
    def is_valid_list(value: list):

        if value is not None and isinstance(value, list):
            return True

        return False
