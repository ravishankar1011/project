import dataclasses
from enum import Enum
from typing import Optional, List

@dataclasses.dataclass
class CreatePage:
    page_code: str
    page_name: str
    page_description: str
    show_in_menu: bool

    def get_dict(self):
        return {
            "page_code": self.page_code,
            "page_name": self.page_name,
            "page_description": self.page_description,
            "show_in_menu": self.show_in_menu
        }

class WidgetType(Enum):
    UNKNOWN_WIDGET = 0
    READ = 1
    CREATE = 2
    UPDATE = 3
    MAKER_CHECKER = 4


class WidgetSubType(Enum):
    UNKNOWN_SUB_WIDGET = 0
    DETAILED = 1
    PAGINATED = 2
    PAGINATED_NUMBERED = 3
    PAGINATED_TOKENIZED = 4
    HIERARCHY = 5
    HEADER = 6
    MENU = 7
    FORM = 8
    DYNAMIC_FORM = 9
    EDITABLE_DETAILED_FORM = 10
    PERMISSION = 11
    MAKER = 12

@dataclasses.dataclass
class WidgetLayoutProperties:
    no_of_columns: int

    def get_dict(self) -> dict:
        return {
            "no_of_columns": self.no_of_columns
        }

@dataclasses.dataclass
class AddWidgetDataSource:
    data_source_id: str
    operation_type: str
    field_codes_to_exclude: List[str]

    def get_dict(self) -> dict:
        return {
            "data_source_id": self.data_source_id,
            "operation_type": self.operation_type,
            "field_codes_to_exclude": self.field_codes_to_exclude
        }

@dataclasses.dataclass
class CreatePageWidgetConfig:
    page_widget_config_code: str
    column_offset: int
    row_span: int
    column_span: int
    row_offset: int
    config_order: Optional[int] = None

    def get_dict(self):
        return {
            "page_widget_config_code": self.page_widget_config_code,
            "layout_config": {
                "column_offset": self.column_offset,
                "row_span": self.row_span,
                "column_span": self.column_span,
                "row_offset": self.row_offset,
                "config_order": self.config_order
            }
        }

@dataclasses.dataclass
class CreateOperator:
    first_name: str
    last_name: str
    email: str
    phone_number: str
    customer_profile_id: Optional[str]
    role_id: Optional[str]
    group_id: Optional[str]

    def get_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "role_id": self.role_id,
            "group_id": self.group_id,
            "customer_profile_id": self.customer_profile_id
        }

@dataclasses.dataclass
class CreateGroup:
    group_name: str
    description: str
    customer_profile_id: Optional[str]
    role_id: Optional[str]

    def get_dict(self):
        return {
            "group_name": self.group_name,
            "description": self.description,
            "customer_profile_id": self.customer_profile_id,
            "role_id": self.role_id
        }
