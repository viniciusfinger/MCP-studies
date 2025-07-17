from enum import Enum

class MessageRole(str, Enum):
    HUMAN = "human"
    AI = "ai"
    SYSTEM = "system"

    @classmethod
    def from_str(cls, value: str) -> "MessageRole":
        """
        Builds a MessageRole object from a string.

        Args:
            value (str): The string value of the message role.

        Returns:
            MessageRole: The corresponding enum value.

        Raises:
            ValueError: If the value does not correspond to any valid role.
        """
        try:
            return cls(value)
        except ValueError:
            raise ValueError(f"Invalid value for MessageRole: {value}")