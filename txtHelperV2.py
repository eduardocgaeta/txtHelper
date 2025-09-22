import tkinter as tk
from tkinter import messagebox
import json
import os
import keyboard
import pyperclip
import threading
import time

# Nome do arquivo para salvar os atalhos
ARQUIVO_JSON = "atalhos.json"

# --- Funções para JSON ---
def carregar_atalhos():
    if os.path.exists(ARQUIVO_JSON):
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_atalhos():
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(atalhos, f, ensure_ascii=False, indent=4)

# --- Funções da UI ---
def adicionar_atalho():
    gatilho = entry_gatilho.get().strip()
    texto = text_predefinido.get("1.0", tk.END).strip()

    if not gatilho or not texto:
        messagebox.showwarning("Aviso", "Preencha o gatilho e o texto!")
        return

    atalhos[gatilho] = texto
    salvar_atalhos()
    atualizar_lista()
    atualizar_buffer_monitor()
    entry_gatilho.delete(0, tk.END)
    text_predefinido.delete("1.0", tk.END)

def editar_atalho():
    selecionado = listbox.curselection()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um atalho para editar!")
        return

    gatilho = entry_gatilho.get().strip()
    texto = text_predefinido.get("1.0", tk.END).strip()

    if not gatilho or not texto:
        messagebox.showwarning("Aviso", "Preencha o gatilho e o texto!")
        return

    atalhos[gatilho] = texto
    salvar_atalhos()
    atualizar_lista()
    atualizar_buffer_monitor()

def remover_atalho():
    selecionado = listbox.curselection()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um atalho para remover!")
        return

    linha = listbox.get(selecionado)
    gatilho = linha.split(" -> ")[0]

    if gatilho in atalhos:
        del atalhos[gatilho]
        salvar_atalhos()
        atualizar_lista()
        atualizar_buffer_monitor()

def selecionar_item(event):
    selecionado = listbox.curselection()
    if selecionado:
        linha = listbox.get(selecionado)
        gatilho = linha.split(" -> ")[0]
        texto = atalhos[gatilho]

        entry_gatilho.delete(0, tk.END)
        entry_gatilho.insert(0, gatilho)

        text_predefinido.delete("1.0", tk.END)
        text_predefinido.insert("1.0", texto)

def atualizar_lista():
    listbox.delete(0, tk.END)
    for gatilho, texto in atalhos.items():
        listbox.insert(tk.END, f"{gatilho} -> {texto[:30]}...")

# --- Monitoramento em tempo real ---
buffer = ""
monitor_ativo = True
monitor_atalhos = {}

def atualizar_buffer_monitor():
    global monitor_atalhos
    monitor_atalhos = atalhos.copy()

def monitor():
    global buffer
    while monitor_ativo:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN and len(event.name) == 1:
            buffer += event.name

            # Limita tamanho do buffer
            max_len = max([len(k) for k in monitor_atalhos.keys()] + [0])
            if len(buffer) > max_len + 5:
                buffer = buffer[-(max_len + 5):]

            # Verifica se algum gatilho corresponde ao final do buffer
            for gatilho, texto in monitor_atalhos.items():
                if buffer.endswith(gatilho):
                    # Apaga o gatilho digitado
                    for _ in range(len(gatilho)):
                        keyboard.press_and_release("backspace")
                    # Cola o texto
                    pyperclip.copy(texto)
                    keyboard.press_and_release("ctrl+v")
                    buffer = ""
                    break
        time.sleep(0.01)

# --- INÍCIO DO PROGRAMA ---
atalhos = carregar_atalhos()
monitor_atalhos = atalhos.copy()

# UI
janela = tk.Tk()
janela.title("Gerenciador de Atalhos")
janela.geometry("500x500")

label_gatilho = tk.Label(janela, text="Gatilho:")
label_gatilho.pack()
entry_gatilho = tk.Entry(janela, width=30)
entry_gatilho.pack()

label_texto = tk.Label(janela, text="Texto predefinido:")
label_texto.pack()
text_predefinido = tk.Text(janela, height=5, width=50)
text_predefinido.pack()

frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=5)

btn_adicionar = tk.Button(frame_botoes, text="Adicionar", command=adicionar_atalho)
btn_adicionar.grid(row=0, column=0, padx=5)
btn_editar = tk.Button(frame_botoes, text="Editar", command=editar_atalho)
btn_editar.grid(row=0, column=1, padx=5)
btn_remover = tk.Button(frame_botoes, text="Remover", command=remover_atalho)
btn_remover.grid(row=0, column=2, padx=5)

label_lista = tk.Label(janela, text="Atalhos cadastrados:")
label_lista.pack()
listbox = tk.Listbox(janela, width=70)
listbox.pack(fill=tk.BOTH, expand=True)
listbox.bind("<<ListboxSelect>>", selecionar_item)

atualizar_lista()

# Thread do monitor
t = threading.Thread(target=monitor, daemon=True)
t.start()

janela.mainloop()

# Para quando fechar a UI
monitor_ativo = False
