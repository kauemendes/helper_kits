
class ArrayKit:

    @staticmethod
    def append_string_to_values(values, append, prepend):
        result = []

        for value in values:
            result.append(prepend + str(value) + append)

        return result

    @staticmethod
    def get_item_or_none(values: list, index: int):
        if values is None:
            return None

        if index > len(values) - 1:
            return None

        return values[index]

    @staticmethod
    def check_array_zero_values(arr_values):
        if len(arr_values) > 0:
            i = 0
            j = 0
            for item in arr_values:
                if isinstance(item, int) or isinstance(item, float):
                    j += 1
                    if item <= 0:
                        i += 1
            if i > 0:
                raise TypeError('Value is zero or null, ' + str(i))
        return True
