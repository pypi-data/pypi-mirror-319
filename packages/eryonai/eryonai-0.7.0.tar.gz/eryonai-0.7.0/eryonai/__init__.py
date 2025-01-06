# eryonai/__init__.py
import sys
import atexit
from .model import EryonModel, EryonConfig, EryonMessages, show_messages

__version__ = "1.0.0"

# Show welcome message on package import
EryonMessages.show_welcome_message()

def __getattr__(name):
    """Trigger welcome message when accessing main components"""
    if name in ["EryonModel", "EryonConfig"]:
        show_messages()
        return globals()[name]
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

# Register cleanup and ensure messages show on exit
def cleanup():
    show_messages()
    sys.stdout.flush()  # Ensure all messages are displayed

atexit.register(cleanup)

# Export public interface
__all__ = [
    "EryonModel",
    "EryonConfig",
    "show_messages",
    "__version__"
]