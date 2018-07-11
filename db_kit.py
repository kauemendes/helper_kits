from app.helper_kit.string_kit import StringKit
from app.models.enums import ProcessTypeNames


class DBKit:

    @staticmethod
    def sanitize(value):
        return value

    @staticmethod
    def generate_filter_or_like(field, values, process_negatives=False):
        return DBKit.generate_filter_generic(field, values, True, process_negatives)

    @staticmethod
    def generate_filter_or_equal(field, values, process_negatives=False):
        return DBKit.generate_filter_generic(field, values, False, process_negatives)

    @staticmethod
    def generate_filter_generic(field, values, use_like=False, process_negatives=False):
        result = ""
        count_result = 0

        result_neg = ""
        count_result_neg = 0

        dict_values = {}

        # (id = 10 or id = 11) and (id is null or (id <> 8 and id <> 4)) traz apenas 10 e 11

        equal_connector = " LIKE " if use_like else " = "
        equal_connector_neg = " NOT LIKE " if use_like else " != "

        for i in range(len(values)):
            value_key = StringKit.random_key(12) + str(i)

            value_real = values[i]
            is_negative = False

            if process_negatives:
                if type(values[i]) is str:

                    if values[i].startswith("-"):
                        value_real = values[i][1:]
                        is_negative = True
                    elif values[i].startswith("\"-"):
                        # Condicao extremamente especial para a situacao da especialidade medica
                        value_real = "\"" + values[i][2:]
                        is_negative = True
                    elif values[i].startswith("#-"):
                        # Condicao extremamente especial para a situacao do dashboard
                        value_real = "#" + values[i][2:]
                        is_negative = True

                elif type(values[i]) is int or type(values[i]) is float:
                    if values[i] < 0:
                        value_real = values[i] * (-1)
                        is_negative = True

            if use_like:
                dict_values[value_key] = "%" + value_real + "%"
            else:
                dict_values[value_key] = value_real

            if is_negative:
                result_neg += (" AND " if count_result_neg > 0 else " ") + field
                result_neg += equal_connector_neg + " :" + value_key + " "
                count_result_neg += 1

            else:
                result += (" OR " if count_result > 0 else " ") + field
                result += equal_connector + " :" + value_key + " "
                count_result += 1

        final_result = " "

        if count_result > 0 and count_result_neg == 0:
            final_result = result
        elif count_result == 0 and count_result_neg > 0:
            final_result = " (" + field + " IS NULL OR (" + result_neg + ")) "
        elif count_result > 0 and count_result_neg > 0:
            final_result = " ( " + result + " ) and (" + field + " IS NULL OR (" + result_neg + ")) "

        return final_result, dict_values

    @staticmethod
    def generate_filter_for_process_pending(process_pending):
        result = ""
        dict_values = {}

        for process in process_pending:
            value_key = StringKit.random_key(10) + str(process)

            if result != "":
                result += " OR "

            if process == ProcessTypeNames.PROCESS_REQUEST.value:
                result += " s.process_type_request =  :"+value_key
                dict_values[value_key] = 0
            if process == ProcessTypeNames.PROCESS_APPROVAL.value:
                result += " s.process_type_approval = :"+value_key
                dict_values[value_key] = 0
            if process == ProcessTypeNames.PROCESS_PRE_ANESTHETIC.value:
                result += " s.process_type_pre_anesthetic = :"+value_key
                dict_values[value_key] = 0
            if process == ProcessTypeNames.PROCESS_SCHEDULING.value:
                result += " s.process_type_scheduling = :"+value_key
                dict_values[value_key] = 0
            if process == ProcessTypeNames.PROCESS_POST_SURGICAL.value:
                result += " s.process_type_post_surgical = :"+value_key
                dict_values[value_key] = 0

        return result, dict_values
