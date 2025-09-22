import tkinter as tk
from tkinter import messagebox
import json
import os

# Nome do arquivo para salvar os atalhos
ARQUIVO_JSON = "atalhos.json"

# Carrega atalhos do JSON (se existir)
def carregar_atalhos():
    if os.path.exists(ARQUIVO_JSON):
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# Salva atalhos no JSON
def salvar_atalhos():
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(atalhos, f, ensure_ascii=False, indent=4)

# Adicionar um novo atalho
def adicionar_atalho():
    gatilho = entry_gatilho.get().strip()
    texto = text_predefinido.get("1.0", tk.END).strip()

    if not gatilho or not texto:
        messagebox.showwarning("Aviso", "Preencha o gatilho e o texto!")
        return

    atalhos[gatilho] = texto
    salvar_atalhos()
    atualizar_lista()

    entry_gatilho.delete(0, tk.END)
    text_predefinido.delete("1.0", tk.END)

# Editar um atalho existente
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

# Remover um atalho
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

# Preenche os campos quando selecionar na lista
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

# Atualiza a listbox com os atalhos cadastrados
def atualizar_lista():
    listbox.delete(0, tk.END)
    for gatilho, texto in atalhos.items():
        listbox.insert(tk.END, f"{gatilho} -> {texto[:30]}...")

# --- INÍCIO DO PROGRAMA ---
atalhos = carregar_atalhos()

janela = tk.Tk()
janela.title("Gerenciador de Atalhos")
janela.geometry("450x450")

# Campo de gatilho
label_gatilho = tk.Label(janela, text="Gatilho:")
label_gatilho.pack()
entry_gatilho = tk.Entry(janela, width=30)
entry_gatilho.pack()

# Campo de texto predefinido
label_texto = tk.Label(janela, text="Texto predefinido:")
label_texto.pack()
text_predefinido = tk.Text(janela, height=5, width=40)
text_predefinido.pack()

# Botões
frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=5)

btn_adicionar = tk.Button(frame_botoes, text="Adicionar", command=adicionar_atalho)
btn_adicionar.grid(row=0, column=0, padx=5)

btn_editar = tk.Button(frame_botoes, text="Editar", command=editar_atalho)
btn_editar.grid(row=0, column=1, padx=5)

btn_remover = tk.Button(frame_botoes, text="Remover", command=remover_atalho)
btn_remover.grid(row=0, column=2, padx=5)

# Lista de atalhos
label_lista = tk.Label(janela, text="Atalhos cadastrados:")
label_lista.pack()
listbox = tk.Listbox(janela, width=60)
listbox.pack(fill=tk.BOTH, expand=True)

listbox.bind("<<ListboxSelect>>", selecionar_item)

# Atualiza a lista com atalhos carregados
atualizar_lista()

janela.mainloop()
