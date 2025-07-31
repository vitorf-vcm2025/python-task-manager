 Gestor de Tarefas
Uma aplicação de desktop completa para a gestão de tarefas (To-Do List), construída com Python, CustomTkinter e uma base de dados SQLite. Este projeto demonstra a implementação das quatro operações fundamentais de uma base de dados (CRUD: Criar, Ler, Atualizar, Apagar).

🎬 Demonstração
![demosntração](https://github.com/user-attachments/assets/6996ab44-8edb-4e28-ae73-6154ca20ba4f)


✨ Funcionalidades Principais
Interface Gráfica Intuitiva: Construído com CustomTkinter para uma aparência moderna e fácil de usar.

Persistência de Dados: As tarefas são guardadas numa base de dados SQLite (tarefas.db), garantindo que a informação não se perde quando a aplicação é fechada.

Gestão Completa de Tarefas (CRUD):

Criar: Adicionar novas tarefas através de um campo de texto.

Ler: Carregar e exibir todas as tarefas guardadas ao iniciar.

Atualizar: Editar o texto de uma tarefa existente através de uma janela de edição.

Apagar: Remover permanentemente uma tarefa da lista e da base de dados.

Estado das Tarefas:

Marcar tarefas como concluídas, alterando a sua aparência visual (cor e prefixo ✅).

Reabrir tarefas concluídas, revertendo o seu estado para "pendente".

Atalhos: Use um duplo clique numa tarefa para a editar rapidamente.

🛠️ Tecnologias Utilizadas
Linguagem: Python

Interface Gráfica (GUI): CustomTkinter

Base de Dados: SQLite3 (biblioteca padrão do Python)

Manipulação de Ícones: Biblioteca Pillow (PIL)

🚀 Como Executar
Clone este repositório.

Instale as dependências necessárias:

pip install customtkinter Pillow

Execute o script principal. Uma base de dados tarefas.db será criada automaticamente no primeiro arranque.

python app.py

