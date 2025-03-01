import os
import datetime
from PySide6.QtWidgets import QFileDialog


def export_messages(parent):
    """Exports messages from `Msg_window` to a .txt file in the 'log_history' folder with a timestamped filename."""
    
    # Get the message text
    messages = parent.ui.Msg_window.toPlainText()
    
    if not messages.strip():
        parent.ui.Msg_window.appendPlainText("No messages to export.")
        return
    
    # Create the 'log_history' folder if it doesn't exist
    log_folder = "log_history"
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # Generate a timestamped filename in AM/PM format
    timestamp = datetime.datetime.now().strftime("log-date-%m-%d-%Y-time-%I-%M-%S-%p.txt")
    log_path = os.path.join(log_folder, timestamp)

    # Save the messages to the file
    with open(log_path, "w", encoding="utf-8") as file:
        file.write(messages)
    
    parent.ui.Msg_window.appendPlainText(f"Messages exported to: {log_path}")


def clear_messages(parent):
    """Clears all messages from `Msg_window`."""
    parent.ui.Msg_window.clear()
