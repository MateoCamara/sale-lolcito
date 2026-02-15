import time
import pyperclip
import pyautogui


def send_clipboard(message):
    """Envía un mensaje pegándolo en la ventana activa (WhatsApp Web/Desktop)."""
    try:
        pyperclip.copy(message)
        time.sleep(0.1)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.1)
        pyautogui.press("enter")
        print(f"  Clipboard OK: {message}")
    except Exception as e:
        print(f"  Clipboard error: {e}")
