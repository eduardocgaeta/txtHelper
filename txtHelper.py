import keyboard
import pyperclip
import time

texto_predefinido = """Atenciosamente,
Eduardo"""

gatilho = "/assinatura"

buffer = ""

def monitorar(event):
    global buffer

    if len(event.name) == 1:
        buffer += event.name

        if len(buffer) > len(gatilho) + 5:
            buffer = buffer[-(len(gatilho)+5):]

        if buffer.endswith(gatilho):
            for _ in range(len(gatilho)):
                keyboard.press_and_release("backspace")

            pyperclip.copy(texto_predefinido)
            keyboard.press_and_release("ctrl+v")
            buffer = ""

keyboard.on_press(monitorar)

keyboard.wait()