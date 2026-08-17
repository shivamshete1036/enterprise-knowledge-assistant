from guardrails import Guard

from utils.guardrails.pii_validator import (
    PIIValidator,
)


class InputGuard:
    """
    Guardrails-based input protection.

    User input is validated for PII before it is sent
    to any LLM.
    """

    def __init__(self):
        validator = PIIValidator(
            on_fail="exception",
        )

        self.guard = Guard().use(validator)

    def validate(self, user_input: str) -> str:
        """
        Validate user input.

        Returns the original input if safe.

        Raises an exception if PII is detected.
        """

        result = self.guard.validate(user_input)

        return result.validated_output