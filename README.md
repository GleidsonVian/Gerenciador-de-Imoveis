# 🏠 Sistema de Gestão de Aluguel de Imóveis

Sistema web para gerenciamento de imóveis, inquilinos e pagamentos de aluguel, desenvolvido com FastAPI + MySQL + Jinja2.

---

## 🚀 Tecnologias

- **Python 3.13**
- **FastAPI** — framework web
- **SQLAlchemy** — ORM
- **MySQL** — banco de dados
- **Jinja2** — templates HTML
- **Bootstrap 5** — estilização
- **APScheduler** — tarefas agendadas
- **python-jose** — autenticação JWT
- **passlib (argon2)** — hash de senhas

---

## 📁 Estrutura do Projeto

```
app/
├── models/
│   ├── imovel.py
│   ├── inquilino.py
│   ├── pagamento.py
│   └── usuario.py
├── routes/
│   ├── imoveis.py
│   ├── inquilinos.py
│   ├── pagamentos.py
│   └── auth.py
├── schemas/
│   └── imovel.py
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── auth/
│   │   ├── login.html
│   │   └── registro.html
│   ├── imoveis/
│   │   ├── listar.html
│   │   └── form.html
│   ├── inquilinos/
│   │   ├── listar.html
│   │   └── form.html
│   └── pagamentos/
│       ├── listar.html
│       └── form.html
├── static/css/
├── auth.py
├── database.py
├── dependencies.py
├── main.py
└── scheduler.py
.env
requirements.txt
```

---

## ⚙️ Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/gestao-aluguel.git
cd gestao-aluguel
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure o arquivo `.env`

Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=mysql+pymysql://root:SUA_SENHA@localhost:3306/aluguel
SECRET_KEY=sua-chave-secreta-aqui
```

### 4. Crie o banco de dados

No MySQL (via DBeaver ou terminal):

```sql
CREATE DATABASE aluguel CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Crie as tabelas

```bash
python create_tables.py
```

### 6. Inicie o servidor

```bash
uvicorn app.main:app --reload
```

Acesse: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📦 Dependências (`requirements.txt`)

```
fastapi
uvicorn
sqlalchemy
pymysql
python-dotenv
jinja2
python-multipart
apscheduler
python-jose[cryptography]
passlib[bcrypt]
argon2-cffi
```

---

## 🔐 Autenticação

O sistema usa **JWT via cookie** para autenticação. Ao acessar qualquer rota protegida sem estar logado, o usuário é redirecionado para `/login`.

Para criar sua conta, acesse `/registro`.

---

## 📋 Funcionalidades

### Imóveis
- Cadastrar, editar e deletar imóveis
- Tipos: casa, apartamento, comercial
- Status: disponível ou alugado (atualizado automaticamente)

### Inquilinos
- Cadastrar, editar e deletar inquilinos
- Vinculação com imóvel disponível
- Ao vincular um inquilino, o imóvel é marcado como **alugado** automaticamente
- Ao deletar um inquilino, o imóvel volta para **disponível**

### Pagamentos
- Registrar pagamentos com data de vencimento
- Marcar pagamento como **pago** com um clique
- Status: pendente, pago, atrasado

### Dashboard
- Visão geral de imóveis, inquilinos e pagamentos
- Contagem de pagamentos pendentes, pagos e atrasados

### Scheduler (Automação)
- Roda automaticamente ao iniciar o servidor
- Verifica pagamentos vencidos a cada **1 hora**
- Marca como **atrasado** qualquer pagamento com `data_vencimento < hoje` e status `pendente`

---

## 🗄️ Modelo do Banco de Dados

```
Imovel
├── id, endereco, tipo, valor_aluguel, status, descricao

Inquilino
├── id, nome, cpf, email, telefone
└── imovel_id (FK → Imovel)

Pagamento
├── id, valor, data_vencimento, data_pagamento, status
├── inquilino_id (FK → Inquilino)
└── imovel_id (FK → Imovel)

Usuario
└── id, nome, email, senha_hash
```

---

## 🛣️ Rotas Principais

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/` | Dashboard |
| GET | `/login` | Página de login |
| GET | `/registro` | Página de cadastro |
| GET | `/logout` | Encerrar sessão |
| GET/POST | `/imoveis/` | Listar / criar imóveis |
| GET/POST | `/imoveis/novo` | Formulário novo imóvel |
| GET/POST | `/imoveis/{id}/editar` | Editar imóvel |
| POST | `/imoveis/{id}/deletar` | Deletar imóvel |
| GET/POST | `/inquilinos/` | Listar / criar inquilinos |
| GET/POST | `/pagamentos/` | Listar / criar pagamentos |
| POST | `/pagamentos/{id}/pagar` | Marcar como pago |

---

## 📌 Próximos Passos (Roadmap)

- [ ] Geração de recibo em PDF
- [ ] Controle de contratos de locação
- [ ] Notificações de vencimento por email
- [ ] Deploy com Docker
- [ ] Filtros e busca nas listagens

---

## 👤 Autor

Desenvolvido por **Gleidson**
