from typing import Any

from guardrails.validators import (
    Validator,
    PassResult,
    FailResult,
)
from guardrails.validator_base import register_validator

from utils.guardrails.presidio_config import (
    create_presidio_analyzer,
)


PII_ENTITIES = {
    "EMAIL_ADDRESS",
    "PHONE_NUMBER",
    "CREDIT_CARD",
    "IP_ADDRESS",
    "PERSON",
    "IN_PAN",
    "IN_AADHAAR",
    "IN_PASSPORT",
}


@register_validator(
    name="PIIValidator",
    data_type="string",
)
class PIIValidator(Validator):
    """
    Custom Guardrails validator for detecting PII.

    Uses our locally configured Presidio AnalyzerEngine
    with the lightweight en_core_web_sm model.
    """

    def __init__(self, on_fail: Any = "exception"):
        super().__init__(on_fail=on_fail)

        self.analyzer = create_presidio_analyzer()

    def validate(
        self,
        value: Any,
        metadata: dict | None = None,
    ):
        """
        Validate text and fail when configured PII is detected.
        """

        if not isinstance(value, str):
            return PassResult()

        results = self.analyzer.analyze(
            text=value,
            language="en",
        )

        detected_pii = [
            result
            for result in results
            if result.entity_type in PII_ENTITIES
        ]

        if not detected_pii:
            return PassResult()

        detected_types = sorted(
            {
                result.entity_type
                for result in detected_pii
            }
        )

        return FailResult(
            error_message=(
                 "Private information detected in content: "
                 + ", ".join(detected_types)
            )
        )