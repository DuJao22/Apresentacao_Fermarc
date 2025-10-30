# Fermarc E-commerce

**Sistema completo de e-commerce em Flask**  
Desenvolvido por **João Lion**

---

## 🎯 Sobre o Projeto

Fermarc é uma plataforma de e-commerce completa e profissional desenvolvida em Python/Flask, focada em robótica e componentes eletrônicos. O sistema foi projetado com as melhores práticas de desenvolvimento, segurança e experiência do usuário.

### 🌟 Funcionalidades Principais

**Para Clientes:**
- ✅ Cadastro e autenticação de usuários
- ✅ Busca avançada de produtos com filtros
- ✅ Carrinho de compras persistente
- ✅ Sistema de checkout completo
- ✅ Histórico de pedidos
- ✅ Gerenciamento de endereços
- ✅ Sistema de cupons de desconto
- ✅ Cálculo de frete dinâmico

**Para Administradores:**
- ✅ Dashboard com métricas em tempo real
- ✅ CRUD completo de produtos, categorias e cupons
- ✅ Gerenciamento de pedidos e status
- ✅ Upload de imagens de produtos
- ✅ Importação/exportação de dados em CSV
- ✅ Relatórios de vendas

**SEO e Marketing:**
- ✅ URLs amigáveis (slugs)
- ✅ Meta tags dinâmicas
- ✅ Sitemap.xml automático
- ✅ Sistema de cupons promocionais

---

## 🚀 Tecnologias Utilizadas

### Backend
- **Python 3.11+**
- **Flask 3.0** - Framework web
- **SQLAlchemy** - ORM para banco de dados
- **Flask-Migrate** - Migrations de banco de dados
- **Flask-Login** - Gerenciamento de sessões
- **Flask-WTF** - Formulários e validação
- **Flask-Limiter** - Rate limiting
- **Werkzeug** - Segurança de senhas

### Frontend
- **Bootstrap 5** - Framework CSS responsivo
- **Font Awesome 6** - Ícones
- **Jinja2** - Template engine
- **JavaScript vanilla** - Interatividade

### Banco de Dados
- **SQLite** (desenvolvimento)
- **PostgreSQL** (produção)

---

## 📦 Instalação e Configuração

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação Automática (Recomendado)

**A forma mais fácil e rápida de instalar:**

```bash
# Clone o repositório
git clone <seu-repositorio>
cd fermarc-ecommerce

# Execute o script de instalação automática
python setup.py
```

O script `setup.py` irá:
- ✅ Verificar a versão do Python
- ✅ Criar o arquivo `.env` automaticamente
- ✅ Instalar todas as dependências
- ✅ Configurar o banco de dados
- ✅ Popular com dados de exemplo (opcional)
- ✅ Criar pastas necessárias

Após a instalação, basta executar:
```bash
python run.py
```

### Instalação Manual

Se preferir instalar manualmente:

1. **Clone o repositório:**
```bash
git clone <seu-repositorio>
cd fermarc-ecommerce
```

2. **Crie um ambiente virtual (opcional mas recomendado):**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente:**
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. **Inicialize o banco de dados:**
```bash
# As migrations já existem, então apenas aplique:
flask db upgrade

# Popular com dados de exemplo (opcional):
FLASK_APP=run.py flask init-db
```

6. **Execute o servidor de desenvolvimento:**
```bash
python run.py
```

A aplicação estará disponível em `http://localhost:5000`

### 🔧 Solução de Problemas Comuns

**Erro: "No module named 'flask'"**
- Solução: Execute `pip install -r requirements.txt`

**Erro: "relation 'products' does not exist"**
- Solução: Execute `flask db upgrade` para criar as tabelas

**Erro: "No such command 'init-db'"**
- Solução: Use `FLASK_APP=run.py flask init-db`

**Erro ao conectar ao banco de dados**
- Solução: Verifique se a variável `DATABASE_URL` no `.env` está correta

---

## 🔐 Credenciais Padrão

Após executar `flask init-db`, você terá:

**Admin:**
- Email: admin@fermarc.com.br
- Senha: admin123

**Cliente:**
- Email: cliente@example.com
- Senha: cliente123

⚠️ **IMPORTANTE:** Altere estas senhas em produção!

---

## 🌐 Deploy no Render

### 1. Preparação

Certifique-se de que seu repositório Git está atualizado com todos os arquivos do projeto.

### 2. Criar Serviço no Render

1. Acesse [Render.com](https://render.com) e faça login
2. Clique em "New +" e selecione "Web Service"
3. Conecte seu repositório GitHub
4. Configure:
   - **Name:** fermarc-ecommerce
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn run:app`

### 3. Configurar Variáveis de Ambiente

No painel do Render, adicione as seguintes variáveis:

```
FLASK_ENV=production
SECRET_KEY=<sua-chave-secreta-forte-aqui>
DATABASE_URL=<url-do-postgres-render>
```

### 4. Criar Banco de Dados PostgreSQL

1. No Render, crie um novo PostgreSQL database
2. Copie a "Internal Database URL"
3. Cole na variável `DATABASE_URL` do seu web service

### 5. Executar Migrations

Após o primeiro deploy, acesse o Shell do Render e execute:

```bash
flask db upgrade
flask init-db
```

### 6. Deploy!

O Render fará o deploy automaticamente. Acesse a URL fornecida!

---

## 📁 Estrutura do Projeto

```
fermarc-ecommerce/
├── app/
│   ├── __init__.py           # Application factory
│   ├── config.py             # Configurações
│   ├── models.py             # Modelos do banco de dados
│   ├── forms.py              # Formulários WTF
│   ├── utils.py              # Funções utilitárias
│   ├── routes/               # Blueprints
│   │   ├── public.py         # Rotas públicas
│   │   ├── auth.py           # Autenticação
│   │   ├── cart.py           # Carrinho e checkout
│   │   ├── admin.py          # Painel administrativo
│   │   └── api.py            # API REST
│   ├── templates/            # Templates Jinja2
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── shop.html
│   │   ├── product.html
│   │   ├── cart.html
│   │   ├── checkout.html
│   │   ├── account/
│   │   ├── admin/
│   │   └── errors/
│   └── static/               # Arquivos estáticos
│       ├── css/
│       ├── js/
│       └── uploads/
├── migrations/               # Migrations do banco
├── tests/                    # Testes
├── .env.example             # Exemplo de variáveis de ambiente
├── .gitignore
├── Procfile                 # Configuração para deploy
├── requirements.txt         # Dependências Python
├── run.py                   # Ponto de entrada
├── LICENSE                  # Licença MIT
└── README.md               # Este arquivo
```

---

## 🔒 Segurança

O sistema implementa diversas camadas de segurança:

- ✅ **CSRF Protection** - Proteção contra Cross-Site Request Forgery
- ✅ **Password Hashing** - Senhas criptografadas com Werkzeug
- ✅ **Session Security** - Cookies HTTPOnly e Secure
- ✅ **Rate Limiting** - Proteção contra brute force
- ✅ **Input Validation** - Sanitização de entradas
- ✅ **Secure File Uploads** - Validação de tipos de arquivo
- ✅ **Environment Variables** - Secrets não hardcoded

---

## 🧪 Testes

Execute os testes com pytest:

```bash
pytest
pytest --cov=app  # Com cobertura de código
```

---

## 📚 API REST

O sistema inclui uma API REST básica em `/api`:

- `GET /api/products` - Lista produtos (JSON)
- `GET /api/product/<slug>` - Detalhes do produto
- `GET /api/categories` - Lista categorias
- `GET /api/health` - Health check

---

## 🛠️ Configuração de Pagamentos

O sistema está preparado para integração com:

### Stripe (Cartão de Crédito)

Configure no `.env`:
```
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
```

### PayPal

Configure no `.env`:
```
PAYPAL_CLIENT_ID=seu_client_id
PAYPAL_SECRET=seu_secret
PAYPAL_MODE=sandbox
```

⚠️ **Nota:** Em desenvolvimento, o sistema usa modo sandbox (teste).

---

## 📧 Configuração de Email

Para envio de emails (recuperação de senha, confirmação de pedidos):

```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=seu-email@gmail.com
MAIL_PASSWORD=sua-senha-app
```

---

## 🎨 Personalização

### Cores e Estilo

Edite `app/static/css/styles.css` para personalizar o tema:

```css
:root {
    --color-primary: #111111;
    --color-red: #DC143C;
    --color-red-dark: #C41230;
}
```

### Logo e Imagens

Substitua os ícones em `app/templates/base.html` e adicione suas imagens em `app/static/uploads/`.

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 👨‍💻 Desenvolvedor

**João Lion**

Sistema desenvolvido como solução de referência para e-commerce profissional em Flask.

---

## 📞 Suporte

Para dúvidas ou suporte:
- Email: contato@fermarc.com.br
- Telefone: (11) 99999-9999

---

## 🎯 Roadmap

Funcionalidades planejadas para futuras versões:

- [ ] Integração com Correios para cálculo real de frete
- [ ] Sistema de avaliações e comentários de produtos
- [ ] Wishlist (lista de desejos)
- [ ] Notificações por email
- [ ] Painel de analytics avançado
- [ ] Suporte multi-idioma (i18n)
- [ ] App mobile (PWA)
- [ ] Integração com redes sociais (login social)
- [ ] Sistema de recomendação de produtos
- [ ] Chat de suporte em tempo real

---

<div align="center">

**Fermarc E-commerce**  
*Sistema open-source de e-commerce profissional*  
Desenvolvido por **João Lion** © 2025

</div>
