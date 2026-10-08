# API de Tarefas

API simples de lista de tarefas feita com **FastAPI** e **SQLite**, como projeto de estudo de Python.

## Como executar

1. Crie e ative o ambiente virtual:

   **Windows (PowerShell)**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **Linux / macOS**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Inicie o servidor:
   ```bash
   uvicorn app.main:app --reload
   ```

Os passos 2 e 3 são iguais nos dois sistemas. Para sair do ambiente virtual, use `deactivate`.

> **Windows:** se o PowerShell bloquear a ativação ("execução de scripts desabilitada"), rode uma vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.
>
> **Linux (Debian/Ubuntu):** se `python3 -m venv` falhar, instale o módulo com `sudo apt install python3-venv`.

O banco `database.db` é criado automaticamente na primeira execução.

A documentação interativa fica em http://127.0.0.1:8000/docs.

## Endpoints

| Método | Rota | Descrição | Respostas |
|---|---|---|---|
| `POST` | `/tasks` | Cria uma tarefa | `201`, `409` (nome repetido), `422` |
| `GET` | `/tasks` | Lista todas as tarefas | `200` |
| `GET` | `/tasks/{task_id}` | Busca uma tarefa pelo id | `200`, `404` |
| `PUT` | `/tasks/{task_id}` | Atualiza uma tarefa | `200`, `404`, `409`, `422` |
| `DELETE` | `/tasks/{task_id}` | Remove uma tarefa | `204`, `404` |

### Corpo para `POST` e `PUT`

```json
{
  "name": "Estudar Python",
  "description": "Terminar o projeto da API",
  "status": 0
}
```

- `name`: obrigatório e único.
- `description`: opcional.
- `status`: opcional, `0` (pendente, padrão) ou `1` (concluída).

## Testando com o Bruno

O projeto inclui uma coleção do [Bruno](https://www.usebruno.com/) com uma requisição para cada endpoint, em `bruno/todo`.

1. Abra o Bruno e use **Open Collection** para selecionar a pasta `bruno/todo`.
2. No canto superior direito, selecione o environment `default_local`. Ele define `baseUrl` como `http://127.0.0.1:8000`.
3. Com o servidor rodando, envie as requisições da coleção.

## Estrutura

```
app/
├── main.py          # cria o app e registra as rotas
├── database.py      # conexão e criação da tabela
├── schemas.py       # modelos Pydantic
└── routers/
    └── tasks.py     # rotas de /tasks
bruno/
└── todo/            # coleção de requisições do Bruno
```
