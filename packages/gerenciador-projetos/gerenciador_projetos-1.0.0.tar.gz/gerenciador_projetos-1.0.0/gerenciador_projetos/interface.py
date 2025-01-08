import os
import shutil
import zipfile
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

def determinar_caminho_zip(tipo_projeto, linguagem_projeto):
    caminhos = {
        "Back": {"java": "./boilerplates/projetos-backend/java.zip",
            "python": "./boilerplates/projetos-backend/python.zip",
            "ruby": "./boilerplates/projetos-backend/ruby.zip"},
        "Front": {"java": "./boilerplates/projetos-frontend/java.zip",
            "python": "./boilerplates/projetos-frontend/python.zip",
            "ruby": "./boilerplates/projetos-frontend/ruby.zip"},
        "Mobile": {"java": "./boilerplates/projetos-mobile/java.zip",
            "python": "./boilerplates/projetos-mobile/python.zip",
            "ruby": "./boilerplates/projetos-mobile/ruby.zip"},
    }
    return caminhos.get(tipo_projeto, {}).get(linguagem_projeto, "")

def verificar_arquivo_zip(caminho_zip):
    if not os.path.exists(caminho_zip):
        messagebox.showerror("Erro", "O arquivo ZIP não existe.")
        return False
    if not caminho_zip.endswith(".zip"):
        messagebox.showerror("Erro", "O arquivo não é um arquivo ZIP válido.")
        return False
    return True

def criar_diretorio_destino(caminho_destino):
    if not os.path.exists(caminho_destino):
        os.makedirs(caminho_destino)

def copiar_arquivo_zip(caminho_zip, caminho_destino):
    nome_arquivo = os.path.basename(caminho_zip)
    destino_zip = os.path.join(caminho_destino, nome_arquivo)
    shutil.copy(caminho_zip, destino_zip)
    return destino_zip

def extrair_zip(caminho_zip, caminho_destino):
    try:
        with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
            zip_ref.extractall(caminho_destino)
    except zipfile.BadZipFile:
        messagebox.showerror("Erro", "O arquivo ZIP está corrompido ou não é válido.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao extrair o arquivo ZIP: {e}")

def apagar_arquivo_zip(caminho_zip):
    if os.path.exists(caminho_zip):
        os.remove(caminho_zip)

def copiar_e_extrair_zip(tipo_projeto, linguagem_projeto, caminho_destino):
    caminho_zip = determinar_caminho_zip(tipo_projeto, linguagem_projeto)
    if not caminho_zip:
        messagebox.showerror("Erro", "Não foi possível determinar o caminho do ZIP.")
        return
    
    if verificar_arquivo_zip(caminho_zip):
        criar_diretorio_destino(caminho_destino)
        destino_zip = copiar_arquivo_zip(caminho_zip, caminho_destino)
        extrair_zip(destino_zip, caminho_destino)
        apagar_arquivo_zip(destino_zip)
        messagebox.showinfo("Sucesso", f"Conteúdo extraído em: {caminho_destino}")

# Interface gráfica
def criar_interface():
    def executar():
        tipo_projeto = combo_tipo_projeto.get()
        linguagem_projeto = combo_linguagem_projeto.get()
        caminho_destino = caminho_destino_var.get()
        
        if not caminho_destino:
            messagebox.showerror("Erro", "Selecione o diretório de destino.")
            return
        
        copiar_e_extrair_zip(tipo_projeto, linguagem_projeto, caminho_destino)
    
    def selecionar_diretorio():
        caminho = filedialog.askdirectory(title="Selecione o diretório de destino")
        if caminho:
            caminho_destino_var.set(caminho)
    
    # Configuração da janela
    janela = tk.Tk()
    janela.title("Quality Software Naldo")
    janela.geometry("500x500")
    janela.configure(bg="#000000")
    
    fonte_padrao = ("Arial", 12)
    
    tk.Label(janela, text="Assistente de Extração de Arquivo ZIP", font=fonte_padrao, bg="#000000", fg="#FFFFFF").pack(pady=10)
    
    # Tipo de projeto
    tk.Label(janela, text="Tipo de Projeto:", font=fonte_padrao, bg="#000000", fg="#FFFFFF").pack(pady=5)
    combo_tipo_projeto = ttk.Combobox(janela, values=["Back", "Front", "Mobile"], font=fonte_padrao, state="readonly")
    combo_tipo_projeto.set("Back")
    combo_tipo_projeto.pack(pady=5)
    
    # Linguagem do projeto
    tk.Label(janela, text="Linguagem do Projeto:", font=fonte_padrao, bg="#000000", fg="#FFFFFF").pack(pady=5)
    combo_linguagem_projeto = ttk.Combobox(janela, values=["java", "python", "ruby"], font=fonte_padrao, state="readonly")
    combo_linguagem_projeto.set("python")
    combo_linguagem_projeto.pack(pady=5)
    
    # Caminho de destino
    tk.Label(janela, text="Caminho de Destino:", font=fonte_padrao, bg="#000000", fg="#FFFFFF").pack(pady=5)
    caminho_destino_var = tk.StringVar()
    tk.Entry(janela, textvariable=caminho_destino_var, font=fonte_padrao, width=30).pack(pady=5)
    tk.Button(janela, text="Selecionar", command=selecionar_diretorio, font=fonte_padrao).pack(pady=5)
    
    # Botão de executar
    tk.Button(janela, text="Executar", command=executar, font=fonte_padrao, bg="#FFFFFF", fg="#000000").pack(pady=10)
    
    # Rodapé
    tk.Label(janela, text="Criado por Agnaldo Vilariano", font=("Arial", 10), bg="#000000", fg="#FFFFFF").pack(side=tk.BOTTOM, pady=10)
    
    janela.mainloop()

criar_interface()
