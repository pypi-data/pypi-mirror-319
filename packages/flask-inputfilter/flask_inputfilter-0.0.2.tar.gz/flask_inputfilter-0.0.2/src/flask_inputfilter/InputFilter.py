from typing import Dict, Any, Optional, List

from flask import request, Response, g

from .Exception import ValidationError
from .Filter import BaseFilter
from .Validator import BaseValidator


class InputFilter:
    """
    Base class for input filters.
    """

    def __init__(self) -> None:

        self.fields = {}

    def add(self,
            name: str,
            required: bool = True,
            filters: Optional[List[BaseFilter]] = None,
            validators: Optional[List[BaseValidator]] = None):
        """
        Add the field to the input filter.
        """

        self.fields[name] = {
            'required': required,
            'filters': filters or [],
            'validators': validators or []
        }

    def applyFilters(self, field_name: str, value: Any) -> Any:
        """
        Apply filters to the field value.
        """

        field = self.fields.get(field_name)

        if not field:
            return value

        for filter_ in field['filters']:
            value = filter_.apply(value)

        return value

    def validateField(self, fieldName: str, value: Any) -> None:
        """
        Validate the field value.
        """

        field = self.fields.get(fieldName)

        if not field:
            return

        for validator in field['validators']:
            validator.validate(value)

    def validateData(self, data: Dict[str, Any],
                     kwargs: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Validate the input data, considering both request data and
        URL parameters (kwargs).
        """

        if kwargs is None:
            kwargs = {}

        validatedData = {}

        combinedData = {**data, **kwargs}

        for fieldName, fieldInfo in self.fields.items():
            value = combinedData.get(fieldName)
            value = self.applyFilters(fieldName, value)

            if fieldInfo['required'] and value is None:
                raise ValidationError(f"Field '{fieldName}' is required.")

            if value is not None:
                self.validateField(fieldName, value)

            validatedData[fieldName] = value

        return validatedData

    @classmethod
    def validate(cls):
        """
        Decorator for validating input data in routes.
        """

        def decorator(f):
            def wrapper(*args, **kwargs):
                if request.method == 'GET':
                    data = request.args

                elif request.method in ['POST', 'PUT', 'DELETE']:
                    if not request.is_json:
                        data = request.args

                    else:
                        data = request.json

                else:
                    return Response(
                        status=415, response="Unsupported method Type")

                inputFilter = cls()

                try:
                    g.validatedData = inputFilter.validateData(data, kwargs)

                except ValidationError as e:
                    return Response(status=400, response=str(e))

                return f(*args, **kwargs)

            return wrapper
        return decorator
