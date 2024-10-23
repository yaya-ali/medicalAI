from pydantic import AfterValidator
from functools import wraps
from typing import Annotated


def check_valid_patientId(func):
    """
    Check if the patientId is valid or not.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        patientId = args[0] if args else kwargs.get("patientId", None)

        # Don't validate None. routes with optional patientId
        if patientId is not None:
            # bug
            # result = PipelineRunner(
            #     pipeline=PipelineNames["Patient"],
            #     patientId=patientId,
            # ).run

            assert isinstance(patientId, str), Exception("Invalid patientId")
        return func(*args, **kwargs)

    return wrapper


@check_valid_patientId
def validate_patient_id(patientId):
    return patientId


PatientIdOptional = Annotated[str | None, AfterValidator(validate_patient_id)]
"""
PatientIdOptional: Annotated type for representing optional patient IDs.

This type allows a string value or None, and it includes a validation
step using the `check_valid_patient_id` decorator.

Attributes:
    validate_patient_id: A function for validating patient IDs.

Usage:
    This type is typically used in scenarios where patient IDs are optional,
    and the validation logic is important to ensure data integrity.

Example:
    ```python
    patientId: PatientIdOptional | None = Field(..., description="The patient ID.")
    ```
"""


PatientIdRequired = Annotated[str, AfterValidator(validate_patient_id)]
"""
PatientIdRequired: Annotated type for representing required patient IDs.

This type allows only a non-optional string value, and it includes a validation
step using the `check_valid_patient_id` decorator.

Attributes:
    validate_patient_id: A function for validating patient IDs.

Usage:
    This type is typically used in scenarios where patient IDs are required,
    and the validation logic is important to ensure data integrity.

Example:
    ```python
    patientId: PatientIdRequired | None = Field(..., description="The patient ID.")
    ```
"""
