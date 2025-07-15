# 📄 Módulo de CRUD de Fichas – SOLO RPG

Este serviço gerencia a criação, leitura, atualização e exclusão (CRUD) de **fichas de personagem** para diferentes sistemas de RPG. Ele se comunica com o módulo de **Templates** para validar e estruturar os dados dinamicamente, conforme o sistema selecionado (D&D 5e, Tormenta20, etc.).


## 🚀 Como rodar localmente

1. Clone o repositório:
   git clone https://github.com/seu-usuario/solo-rpg-crud-sheets.git
   cd solo-rpg-crud-sheets

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Defina as variáveis de ambiente em um `.env`:

   ```
   MONGO_URI=mongodb+srv://<user>:<senha>@cluster.mongodb.net/?retryWrites=true&w=majority
   DATABASE_NAME=solo_rpg
   TEMPLATES_SERVICE_URL=http://localhost:8000/api/templates/
   ```

4. Inicie o servidor:

   ```bash
   uvicorn app.main:app --reload --port 8001
   ```

---

## 🧠 O que este serviço faz?

* Cria fichas com base em templates externos.
* Lista, atualiza, deleta e busca fichas por ID ou por dono.
* Se integra com o **serviço de templates** para validar campos dinamicamente.

---

## 🔗 Endpoints disponíveis

### 📄 Fichas

| Método | Rota                               | Descrição             |
| ------ | ---------------------------------- | --------------------- |
| GET    | `/api/sheets/`                     | Lista todas as fichas |
| GET    | `/api/sheets/{sheet_id}`           | Busca ficha por ID    |
| GET    | `/api/sheets/by-user_id/{user_id}` | Lista fichas por dono |
| POST   | `/api/sheets/`                     | Cria nova ficha       |
| PUT    | `/api/sheets/{sheet_id}`           | Atualiza ficha        |
| DELETE | `/api/sheets/{sheet_id}`           | Deleta ficha          |

---

## 📐 Estrutura dos Dados

As fichas são armazenadas com base em `templates` dinâmicos. Cada campo é armazenado como um objeto `SheetField` com a seguinte estrutura:

```json
{
  "value": <valor preenchido>,
  "required": true,
  "options": ["op1", "op2"]  // se aplicável
}
```

---

## 🧱 Arquitetura e Integrações

* Conexão com MongoDB via Motor (async).
* Requisições HTTP para o serviço de Templates via `httpx`.
* Roteamento com FastAPI.

---

## ⚙️ Estrutura de Arquivos

```
crud-sheets/
├── app/
│   ├── routers/
│   │   └── sheets.py         # Endpoints da API
│   ├── sheets_rules.py       # Lógica de montagem e validação das fichas
│   ├── models.py             # Modelos de dados (Pydantic)
│   ├── config.py             # Configurações e variáveis de ambiente
│   ├── dependencies.py       # Acesso a serviços e banco de dados
│   ├── database.py           # Conexão com MongoDB
│   └── main.py               # Entrada principal da aplicação
```

---

## 🧪 Swagger / Documentação da API

* A documentação interativa está disponível automaticamente em:

  ```
  http://localhost:8001/docs
  ```

* Ela permite testar endpoints com exemplos diretamente no navegador.

