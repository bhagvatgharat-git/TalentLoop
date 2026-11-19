"""Console input and pause utilities."""

from typing import Any, Callable, Optional


def prompt_validated_input(
    prompt_text: str,
    validator: Optional[Callable[[str], Any]] = None,
    default: Optional[Any] = None,
) -> Any:
    """Prompt user repeatedly until a valid input is received or default accepted."""
    while True:
        suffix = f" [{default}]" if default is not None else ""
        raw_val = input(f"{prompt_text}{suffix}: ").strip()
        if not raw_val and default is not None:
            return default
        if not raw_val:
            print("Error: Input cannot be empty. Please enter a value.")
            continue
        if validator:
            try:
                return validator(raw_val)
            except Exception as exc:
                print(f"Validation error: {exc}")
                continue
        return raw_val


def pause_for_user(message: str = "Press Enter to continue...") -> None:
    """Pause console display until the user presses Enter."""
    input(f"\n{message}")
