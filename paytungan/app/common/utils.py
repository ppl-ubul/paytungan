import dataclasses
from django.utils import timezone

import uuid
from dataclasses import fields
from datetime import datetime, time, date
from decimal import Decimal
from enum import Enum
from typing import Optional, TypeVar, Type, List, Dict, Any, _GenericAlias

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
    def map_domain(
        source_model_object,
        destination_domain_class: Type[T],
        channel: str,
        modifier: str,
    ) -> T:
        result = ObjectMapperUtil.map(source_model_object, destination_domain_class)
        creation_dict = ObjectMapperUtil.default_domain_creation_params(
            channel=channel, modifier=modifier
        )

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
    def default_domain_creation_params(
        channel: str,
        modifier: str,
        is_active: bool = True,
    ):
        time_now = datetime.now()
        return {
            "id": 0,
            "created_at": time_now,
            "created_by": modifier,
            "updated_at": time_now,
            "updated_by": modifier,
            "deleted": None,
            "deleted_by": None,
            "modified_from": channel,
            "is_active": is_active,
        }

    # TODO: deprecate is_create
    @staticmethod
    def default_model_creation_params(channel: str, is_create: bool, modifier: str):
        time_now = timezone.now()
        params = {
            "updated_at": time_now,
            "updated_by": modifier,
            "modified_from": channel,
            "created_at": time_now,
            "created_by": modifier,
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
