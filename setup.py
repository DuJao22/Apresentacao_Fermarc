#!/usr/bin/env python3
"""
Script de instalação e configuração do Fermarc E-commerce
Automatiza o processo de setup do projeto
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path


def print_header(message):
    """Imprime cabeçalho formatado"""
    print("\n" + "=" * 60)
    print(f"  {message}")
    print("=" * 60 + "\n")


def print_step(step, message):
    """Imprime passo da instalação"""
    print(f"\n[{step}] {message}...")


def check_python_version():
    """Verifica se a versão do Python é compatível"""
    print_step("1/7", "Verificando versão do Python")
    
    if sys.version_info < (3, 8):
        print("❌ Erro: Python 3.8 ou superior é necessário")
        print(f"   Versão atual: {sys.version}")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} detectado")


def create_env_file():
    """Cria arquivo .env a partir do .env.example"""
    print_step("2/7", "Configurando arquivo .env")
    
    if os.path.exists('.env'):
        response = input("   Arquivo .env já existe. Deseja sobrescrever? (s/n): ")
        if response.lower() != 's':
            print("   ⏭️  Mantendo arquivo .env existente")
            return
    
    if os.path.exists('.env.example'):
        shutil.copy('.env.example', '.env')
        print("✅ Arquivo .env criado com sucesso")
        print("⚠️  IMPORTANTE: Edite o arquivo .env com suas configurações!")
    else:
        print("❌ Arquivo .env.example não encontrado")


def install_dependencies():
    """Instala dependências do projeto"""
    print_step("3/7", "Instalando dependências")
    
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            check=True
        )
        print("✅ Dependências instaladas com sucesso")
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar dependências")
        sys.exit(1)


def setup_database():
    """Configura o banco de dados"""
    print_step("4/7", "Configurando banco de dados")
    
    # Verifica se já existe uma pasta migrations
    migrations_exists = os.path.exists('migrations') and os.path.exists('migrations/versions')
    
    if migrations_exists:
        print("   ℹ️  Migrations já configuradas")
        
        # Aplica migrations existentes
        try:
            result = subprocess.run(
                [sys.executable, "-m", "flask", "db", "upgrade"],
                env={**os.environ, 'FLASK_APP': 'run.py'},
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("✅ Migrations aplicadas com sucesso")
            else:
                print(f"⚠️  Aviso: {result.stderr}")
        except Exception as e:
            print(f"⚠️  Aviso ao aplicar migrations: {e}")
    else:
        print("   ℹ️  Inicializando migrations pela primeira vez")
        try:
            # Inicializa migrations
            subprocess.run(
                [sys.executable, "-m", "flask", "db", "init"],
                env={**os.environ, 'FLASK_APP': 'run.py'},
                check=True
            )
            
            # Cria migration inicial
            subprocess.run(
                [sys.executable, "-m", "flask", "db", "migrate", "-m", "Initial migration"],
                env={**os.environ, 'FLASK_APP': 'run.py'},
                check=True
            )
            
            # Aplica migration
            subprocess.run(
                [sys.executable, "-m", "flask", "db", "upgrade"],
                env={**os.environ, 'FLASK_APP': 'run.py'},
                check=True
            )
            
            print("✅ Banco de dados configurado com sucesso")
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao configurar banco de dados: {e}")
            sys.exit(1)


def populate_database():
    """Popula banco de dados com dados de exemplo"""
    print_step("5/7", "Populando banco de dados com dados de exemplo")
    
    response = input("   Deseja popular o banco com dados de exemplo? (s/n): ")
    
    if response.lower() == 's':
        try:
            subprocess.run(
                [sys.executable, "-m", "flask", "init-db"],
                env={**os.environ, 'FLASK_APP': 'run.py'},
                check=True
            )
            print("✅ Dados de exemplo inseridos com sucesso")
            print("\n   📋 Credenciais de acesso:")
            print("   Admin - Email: admin@fermarc.com.br | Senha: admin123")
            print("   Cliente - Email: cliente@example.com | Senha: cliente123")
        except subprocess.CalledProcessError:
            print("⚠️  Dados já existem ou erro ao popular banco")
    else:
        print("   ⏭️  Banco de dados não populado")


def create_upload_folder():
    """Cria pasta de uploads se não existir"""
    print_step("6/7", "Verificando pastas necessárias")
    
    upload_folder = Path("app/static/uploads/products")
    upload_folder.mkdir(parents=True, exist_ok=True)
    
    print("✅ Pastas criadas/verificadas")


def print_success():
    """Imprime mensagem de sucesso"""
    print_step("7/7", "Finalização")
    
    print_header("🎉 INSTALAÇÃO CONCLUÍDA COM SUCESSO! 🎉")
    
    print("""
📝 Próximos passos:

1. Edite o arquivo .env com suas configurações:
   - SECRET_KEY (IMPORTANTE para produção!)
   - DATABASE_URL (se usar PostgreSQL)
   - Configurações de email (opcional)
   - Chaves de pagamento (opcional)

2. Execute o servidor de desenvolvimento:
   python run.py

3. Acesse a aplicação em:
   http://localhost:5000

4. Acesse o painel administrativo em:
   http://localhost:5000/admin
   
   Credenciais padrão:
   Email: admin@fermarc.com.br
   Senha: admin123

⚠️  IMPORTANTE: 
   - Altere as senhas padrão em produção
   - Configure uma SECRET_KEY forte em produção
   - Use PostgreSQL em produção (não SQLite)

📚 Documentação completa: README.md

Desenvolvido por João Lion
""")


def main():
    """Função principal"""
    print_header("FERMARC E-COMMERCE - INSTALAÇÃO")
    print("Sistema de e-commerce completo em Flask\n")
    
    try:
        check_python_version()
        create_env_file()
        install_dependencies()
        setup_database()
        populate_database()
        create_upload_folder()
        print_success()
        
    except KeyboardInterrupt:
        print("\n\n❌ Instalação cancelada pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Erro inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
