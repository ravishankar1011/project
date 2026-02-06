from dataclasses import is_dataclass
import ast
from datetime import datetime, timedelta
import dataclasses
from dacite import Config, from_dict
from dacite.types import extract_optional, is_optional
from setuptools._distutils.util import strtobool


class DataClassParser(object):
    @staticmethod
    def parse_rows(rows, data_class):
        result = []
        for row in rows:
            result.append(DataClassParser.parse_row(row, data_class))
        return result

    @staticmethod
    def parse_row(row, data_class):
        attribute_data = {}
        for heading, cell_text in row.items():  # SEE CLASS: behave.model.Row
            attribute_type = DataClassParser.__select_attribute_parser(
                heading, data_class
            )
            if attribute_type is None:
                continue

            cell_value = DataClassParser.__parse_attribute(cell_text, attribute_type)
            attribute_data[heading] = cell_value

        return DataClassParser.dict_to_object(attribute_data, data_class)

    @staticmethod
    def dict_to_object(data, data_class):
        # Create a data_object from a dict with attribute names and values
        return from_dict(
            data_class=data_class, data=data, config=Config(check_types=False)
        )

    @staticmethod
    def __select_attribute_parser(attribute_name, data_class):
        for field in dataclasses.fields(data_class):
            if field.name == attribute_name:
                if is_optional(field.type):
                    target_type = extract_optional(field.type)
                else:
                    target_type = field.type
                return target_type

        return None

    @staticmethod
    def __parse_attribute(cell_text, attribute_type):
        try:
            if cell_text is None or str(cell_text).strip() == "":
                return None
            if is_dataclass(attribute_type):
                inner_dict = ast.literal_eval(str(cell_text))
                return from_dict(
                    data_class=attribute_type,
                    data=inner_dict,
                    config=Config(check_types=False),
                )
            elif attribute_type.__name__ == "bool":
                return bool(strtobool(cell_text))
            elif attribute_type.__name__ == "dict":
                return ast.literal_eval(str(cell_text))
            elif attribute_type.__name__ == "float":
                return float(cell_text) if cell_text.strip() else None
            elif attribute_type.__name__ == "int":
                return int(cell_text) if cell_text.strip() else None
            elif attribute_type.__name__ == "str":
                return str(cell_text)
            elif attribute_type.__name__ == "datetime":
                if not cell_text.strip():
                    return None
                lowered = cell_text.strip().lower()
                if lowered.startswith("today"):
                    if "+" in lowered:
                        offset = int(lowered.split("+")[1])
                        return datetime.today() + timedelta(days=offset)
                    else:
                        return datetime.today()
                for fmt in ("%Y-%m-%d", "%d %B %Y"):
                    try:
                        return datetime.strptime(cell_text.strip(), fmt)
                    except ValueError:
                        continue
                raise ValueError(
                    f"Failed to parse '{cell_text}' as datetime. "
                    f"Supported formats: YYYY-MM-DD or DD Month YYYY"
                )
            else:
                return attribute_type(cell_text)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Failed to parse '{cell_text}' as {attribute_type}: {e}")


def parse_rows_as_dict(table_rows):
    rows = []
    for table_row in table_rows:
        attribute_data = {}
        for heading, cell_text in table_row.items():
            attribute_data[heading] = cell_text
        rows.append(attribute_data)
    return rows


def check_status(response, expected_status):
    status_code = response["headers"]["status_code"]
    assert status_code == str(expected_status), (
        f"\nExpect headers.status_code: {expected_status}"
        f"\nActual headers.status_code: {status_code}"
    )
