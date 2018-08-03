from app import db
from flask import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.attributes import QueryableAttribute

from helper_kits.string_kit import StringKit


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




class BaseModel(db.Model):
    __abstract__ = True

    def to_dict(self, show=None, _hide=[], _path=None):
        """Return a dictionary representation of this model."""

        show = show or []

        hidden = self._hidden_fields if hasattr(self, "_hidden_fields") else []
        default = self._default_fields if hasattr(self, "_default_fields") else []
        default.extend(['id', 'modified_at', 'created_at'])

        if not _path:
            _path = self.__tablename__.lower()

            def prepend_path(item):
                item = item.lower()
                if item.split(".", 1)[0] == _path:
                    return item
                if len(item) == 0:
                    return item
                if item[0] != ".":
                    item = ".%s" % item
                item = "%s%s" % (_path, item)
                return item

            _hide[:] = [prepend_path(x) for x in _hide]
            show[:] = [prepend_path(x) for x in show]

        columns = self.__table__.columns.keys()
        relationships = self.__mapper__.relationships.keys()
        properties = dir(self)

        ret_data = {}

        for key in columns:
            if key.startswith("_"):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                ret_data[key] = getattr(self, key)

        for key in relationships:
            if key.startswith("_"):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                _hide.append(check)
                is_list = self.__mapper__.relationships[key].uselist
                if is_list:
                    items = getattr(self, key)
                    if self.__mapper__.relationships[key].query_class is not None:
                        if hasattr(items, "all"):
                            items = items.all()
                    ret_data[key] = []
                    for item in items:
                        ret_data[key].append(
                            item.to_dict(
                                show=list(show),
                                _hide=list(_hide),
                                _path=("%s.%s" % (_path, key.lower())),
                            )
                        )
                else:
                    if (
                        self.__mapper__.relationships[key].query_class is not None
                        or self.__mapper__.relationships[key].instrument_class
                        is not None
                    ):
                        item = getattr(self, key)
                        if item is not None:
                            ret_data[key] = item.to_dict(
                                show=list(show),
                                _hide=list(_hide),
                                _path=("%s.%s" % (_path, key.lower())),
                            )
                        else:
                            ret_data[key] = None
                    else:
                        ret_data[key] = getattr(self, key)

        for key in list(set(properties) - set(columns) - set(relationships)):
            if key.startswith("_"):
                continue
            if not hasattr(self.__class__, key):
                continue
            attr = getattr(self.__class__, key)
            if not (isinstance(attr, property) or isinstance(attr, QueryableAttribute)):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                val = getattr(self, key)
                if hasattr(val, "to_dict"):
                    ret_data[key] = val.to_dict(
                        show=list(show),
                        _hide=list(_hide), _path=("%s.%s" % (_path, key.lower()))
                        _path=('%s.%s' % (path, key.lower())),
                    )
                else:
                    try:
                        ret_data[key] = json.loads(json.dumps(val))
                    except:
                        pass

        return ret_data