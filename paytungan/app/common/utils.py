import dataclasses
from django.utils import timezone

import uuid
from dataclasses import fields
from datetime import datetime, time, date
from decimal import Decimal
from enum import Enum
from typing import Optional, Tuple, TypeVar, Type, List, Dict, Any, _GenericAlias

T = TypeVar("T")


class ObjectMapperUtil:
    @staticmethod
    def map(source_model_object, destination_domain_class: Type[T]) -> T:
        """
        This method will not raise error if the source object does not have attribute(s)
        required by the destination domain class.
        This method still can't handle Dict, Any, and Tuple for destination class
        """

        if isinstance(destination_domain_class, _GenericAlias):
            destination_domain_class = destination_domain_class.__args__[0]

        if isinstance(source_model_object, List):
            return [
                ObjectMapperUtil.map(obj, destination_domain_class)
                for obj in source_model_object
            ]

        is_dataclass = dataclasses.is_dataclass(destination_domain_class)
        source_same_type = type(source_model_object) is destination_domain_class

        # handle if primitive and same type
        if not is_dataclass or source_model_object is None or source_same_type:
            return source_model_object

        domain_fields = [field for field in fields(destination_domain_class)]

        if issubclass(type(source_model_object), dict):
            attributes = {}
            for field in domain_fields:
                key_exist = field.name in source_model_object.keys()
                if key_exist or field.default is dataclasses.MISSING:
                    value = source_model_object.get(field.name)
                    if value:
                        value = ObjectMapperUtil.map(value, field.type)

                    attributes[field.name] = value
        elif dataclasses.is_dataclass(source_model_object):
            return ObjectMapperUtil.map(
                dataclasses.asdict(source_model_object), destination_domain_class
            )
        else:
            attributes = {
                field.name: (
                    ObjectMapperUtil.map(
                        getattr(source_model_object, field.name, None), field.type
                    )
                )
                for field in domain_fields
            }

        return destination_domain_class(**attributes)

    @staticmethod
    def map_domain(source_model_object, destination_domain_class: Type[T]) -> T:
        result = ObjectMapperUtil.map(source_model_object, destination_domain_class)
        creation_dict = ObjectMapperUtil.default_domain_creation_params()

        objects = result if isinstance(result, List) else [result]
        for obj in objects:
            for attribute, value in creation_dict.items():
                if hasattr(obj, attribute) and getattr(obj, attribute) is None:
                    setattr(obj, attribute, value)

        return result

    @staticmethod
    def map_array(source_model_objects, destination_domain_class: Type[T]) -> List[T]:
        return [
            ObjectMapperUtil.map(source_model_object, destination_domain_class)
            for source_model_object in source_model_objects
        ]

    @staticmethod
    def default_domain_creation_params():
        time_now = timezone.now()
        return {
            "id": 0,
            "created_at": time_now,
            "updated_at": time_now,
        }

    # TODO: deprecate is_create
    @staticmethod
    def default_model_creation_params():
        time_now = timezone.now()
        params = {
            "updated_at": time_now,
            "created_at": time_now,
        }
        return params


class DictionaryUtil:
    @staticmethod
    def transform_into_jsonable_dictionary(
        data_object: Any, datetime_format: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        if dataclasses.is_dataclass(data_object):
            return DictionaryUtil.transform_into_jsonable_dictionary(
                dataclasses.asdict(data_object)
            )

        if not isinstance(data_object, Dict):
            return None

        def transform_data(data: T) -> T:
            if isinstance(data, Enum):
                data = data.value
            elif isinstance(data, Decimal):
                data = float(data)
            elif isinstance(data, uuid.UUID):
                data = str(data)
            elif isinstance(data, datetime):
                if datetime_format:
                    data = data.strftime(datetime_format)
                else:
                    data = data.astimezone().isoformat()
            elif isinstance(data, time):
                data = data.isoformat()
            elif isinstance(data, date):
                data = data.isoformat()
            elif isinstance(data, List):
                for index in range(len(data)):
                    data[index] = transform_data(data[index])
            elif isinstance(data, Dict):
                for key in data:
                    data[key] = transform_data(data[key])
            elif dataclasses.is_dataclass(data):
                data = transform_data(dataclasses.asdict(data))

            return data

        return transform_data(data_object)

    @staticmethod
    def transform_into_jsonable_array(
        data_array: List[Any], datetime_format: Optional[str] = None
    ) -> Optional[List[Any]]:
        results = []
        for data_object in data_array:
            if dataclasses.is_dataclass(data_object):
                data_object = dataclasses.asdict(data_object)

            results.append(
                DictionaryUtil.transform_into_jsonable_dictionary(
                    data_object, datetime_format
                )
            )

        return results


class StringUtil:
    @staticmethod
    def transform_enum_to_title(enum_value: str) -> str:
        return enum_value.replace("_", " ").title()


class EnumUtil:
    T = TypeVar("T")

    @staticmethod
    def extract_enum_values(enum_class: Type[Enum]):
        return [enum.value for enum in enum_class]

    @staticmethod
    def convert_string_to_enum(
        value: str, enum_class: Type[T], allow_null: bool = True
    ) -> Optional[T]:
        if value is not None or not allow_null:
            return enum_class(value)
        return None

    @staticmethod
    def is_valid(value: str, enum_class: Type[Enum]):
        return value in EnumUtil.extract_enum_values(enum_class)

    @staticmethod
    def transform_to_choice(enum_object: Type[Enum]) -> List[Tuple[str, str]]:
        return list(
            map(
                lambda enum_value: (
                    enum_value,
                    StringUtil.transform_enum_to_title(enum_value),
                ),
                EnumUtil.extract_enum_values(enum_object),
            )
        )

    @staticmethod
    def value_or_none(enum_object: Optional[Enum]) -> Optional[str]:
        return enum_object.value if enum_object else None
