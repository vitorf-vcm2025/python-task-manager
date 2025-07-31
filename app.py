import customtkinter as ctk
import tkinter
from tkinter import font
import sqlite3
import os

# --- Classe Principal da Aplicação ---


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()  # Esconde a janela principal inicialmente
        self.setup_splash_screen()

    def setup_splash_screen(self):
        # Cria a janela de splash screen
        self.splash = ctk.CTkToplevel(self.root)
        self.splash.geometry("400x250")
        self.splash.overrideredirect(True)
        self.splash.attributes("-topmost", True)

        # Centraliza a splash screen
        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        x = (screen_width / 2) - (400 / 2)
        y = (screen_height / 2) - (250 / 2)
        self.splash.geometry(f'+{int(x)}+{int(y)}')

        splash_frame = ctk.CTkFrame(
            self.splash, corner_radius=15, fg_color="#F0F0F0")
        splash_frame.pack(expand=True, fill="both", padx=10, pady=10)

        icon_label = ctk.CTkLabel(
            splash_frame, text="✅", font=ctk.CTkFont(size=60), text_color="#00796B")
        icon_label.pack(pady=(30, 10))
        title_label = ctk.CTkLabel(splash_frame, text="Gestor de Tarefas", font=ctk.CTkFont(
            size=24, weight="bold"), text_color="black")
        title_label.pack(pady=5)
        version_label = ctk.CTkLabel(
            splash_frame, text="Versão 1.0", font=ctk.CTkFont(size=12), text_color="#505050")
        version_label.pack(pady=5)

        self.splash.update()
        self.splash.after(3000, self.show_main_window)

    def show_main_window(self):
        self.splash.destroy()
        self.root.deiconify()
        self.setup_main_ui()

    def setup_main_ui(self):
        # --- Configuração da Janela Principal ---
        self.root.title("Gestor de Tarefas")
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        # --- Fontes ---
        self.font_normal = font.Font(family="Inter", size=14)
        self.font_concluida = font.Font(
            family="Inter", size=14, overstrike=True)

        # --- Título da Aplicação ---
        title_label = ctk.CTkLabel(
            self.root, text="Minhas Tarefas", font=ctk.CTkFont(size=28, weight="bold"))
        title_label.pack(pady=(20, 10))

        # --- Frame para Adicionar Tarefas ---
        add_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        add_frame.pack(pady=10, padx=20, fill="x")

        self.task_entry = ctk.CTkEntry(
            add_frame, placeholder_text="Escreva uma nova tarefa...", height=40)
        self.task_entry.pack(side="left", expand=True, fill="x")

        self.add_button = ctk.CTkButton(
            add_frame, text="Adicionar", width=100, height=40, command=self.adicionar_tarefa)
        self.add_button.pack(side="left", padx=(10, 0))

        # --- Frame para a Lista de Tarefas ---
        tasks_list_frame = ctk.CTkFrame(self.root, corner_radius=10)
        tasks_list_frame.pack(pady=10, padx=20, expand=True, fill="both")

        self.tasks_listbox = tkinter.Listbox(
            tasks_list_frame, font=self.font_normal, bg="#333333", fg="white",
            selectbackground="#565B5E", selectforeground="white", borderwidth=0,
            highlightthickness=0, activestyle="none"
        )
        self.tasks_listbox.pack(expand=True, fill="both", padx=10, pady=10)
        self.tasks_listbox.bind("<Double-1>", self.abrir_janela_edicao)

        # --- Frame para os Botões de Ação ---
        action_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        action_frame.pack(pady=(0, 10), padx=20, fill="x")
        action_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.complete_button = ctk.CTkButton(
            action_frame, text="Concluir/Reabrir", command=self.alterar_status_tarefa, fg_color="#00796B", hover_color="#004D40")
        self.complete_button.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.edit_button = ctk.CTkButton(
            action_frame, text="Editar Tarefa", command=self.abrir_janela_edicao)
        self.edit_button.grid(row=0, column=1, sticky="ew", padx=5)
        self.delete_button = ctk.CTkButton(
            action_frame, text="Apagar Tarefa", command=self.apagar_tarefa, fg_color="#D32F2F", hover_color="#B71C1C")
        self.delete_button.grid(row=0, column=2, sticky="ew", padx=(5, 0))

        # --- Carrega as tarefas existentes ---
        self.inicializar_db()
        self.carregar_tarefas()

    def inicializar_db(self):
        self.conn = sqlite3.connect('tarefas.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tarefas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descricao TEXT NOT NULL UNIQUE,
                status TEXT NOT NULL DEFAULT 'pendente'
            )
        ''')
        self.conn.commit()

    def carregar_tarefas(self):
        self.tasks_listbox.delete(0, tkinter.END)
        self.cursor.execute("SELECT descricao, status FROM tarefas")
        for i, (descricao, status) in enumerate(self.cursor.fetchall()):
            if status == 'concluida':
                self.tasks_listbox.insert(tkinter.END, f"✅ {descricao}")
                self.tasks_listbox.itemconfig(i, {'fg': 'gray'})
            else:
                self.tasks_listbox.insert(tkinter.END, f"   {descricao}")
                self.tasks_listbox.itemconfig(i, {'fg': 'white'})

    def adicionar_tarefa(self):
        tarefa = self.task_entry.get()
        if tarefa:
            try:
                self.cursor.execute(
                    "INSERT INTO tarefas (descricao) VALUES (?)", (tarefa,))
                self.conn.commit()
            except sqlite3.IntegrityError:
                print(f"A tarefa '{tarefa}' já existe.")
            self.task_entry.delete(0, ctk.END)
            self.carregar_tarefas()

    def apagar_tarefa(self):
        try:
            tarefa_texto_completo = self.tasks_listbox.get(
                self.tasks_listbox.curselection()[0])
            tarefa_a_apagar = tarefa_texto_completo.strip().lstrip('✅ ')
            self.cursor.execute(
                "DELETE FROM tarefas WHERE descricao = ?", (tarefa_a_apagar,))
            self.conn.commit()
            self.carregar_tarefas()
        except IndexError:
            print("Nenhuma tarefa selecionada para apagar.")

    def alterar_status_tarefa(self):
        try:
            tarefa_texto_completo = self.tasks_listbox.get(
                self.tasks_listbox.curselection()[0])
            tarefa_selecionada = tarefa_texto_completo.strip().lstrip('✅ ')
            self.cursor.execute(
                "SELECT status FROM tarefas WHERE descricao = ?", (tarefa_selecionada,))
            status_atual = self.cursor.fetchone()[0]
            novo_status = 'pendente' if status_atual == 'concluida' else 'concluida'
            self.cursor.execute(
                "UPDATE tarefas SET status = ? WHERE descricao = ?", (novo_status, tarefa_selecionada))
            self.conn.commit()
            self.carregar_tarefas()
        except IndexError:
            print("Nenhuma tarefa selecionada para alterar o status.")

    def abrir_janela_edicao(self, event=None):
        try:
            tarefa_texto_completo = self.tasks_listbox.get(
                self.tasks_listbox.curselection()[0])
            tarefa_antiga = tarefa_texto_completo.strip().lstrip('✅ ')

            janela_edicao = ctk.CTkToplevel(self.root)
            janela_edicao.title("Editar Tarefa")
            janela_edicao.geometry("400x150")
            janela_edicao.transient(self.root)
            janela_edicao.grab_set()

            edit_entry = ctk.CTkEntry(janela_edicao, width=360, height=40)
            edit_entry.pack(pady=20, padx=20)
            edit_entry.insert(0, tarefa_antiga)

            save_button = ctk.CTkButton(
                janela_edicao, text="Salvar Alterações",
                command=lambda: self.salvar_edicao(
                    tarefa_antiga, edit_entry.get(), janela_edicao)
            )
            save_button.pack(pady=10)
        except IndexError:
            print("Nenhuma tarefa selecionada para editar.")

    def salvar_edicao(self, tarefa_antiga, tarefa_nova, janela_edicao):
        if tarefa_nova and tarefa_nova != tarefa_antiga:
            self.cursor.execute(
                "UPDATE tarefas SET descricao = ?, status = 'pendente' WHERE descricao = ?", (tarefa_nova, tarefa_antiga))
            self.conn.commit()
            self.carregar_tarefas()
        janela_edicao.destroy()


# --- Ponto de Entrada da Aplicação ---
if __name__ == "__main__":
    root = ctk.CTk()
    app = TodoApp(root)
    root.mainloop()
