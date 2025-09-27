#!/usr/bin/env python3
"""
Script para facilitar o deploy no Heroku
"""

import os
import subprocess
import sys
import secrets
import string

def generate_secret_key():
    """Gera uma chave secreta segura"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(50))

def run_command(command, description):
    """Executa um comando e mostra o resultado"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Sucesso!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Erro!")
        print(f"Erro: {e.stderr}")
        return False

def main():
    print("🚀 Deploy do IFC Monitoring System para Heroku")
    print("=" * 50)
    
    # Verificar se o Heroku CLI está instalado
    if not run_command("heroku --version", "Verificando Heroku CLI"):
        print("\n❌ Heroku CLI não encontrado!")
        print("Instale em: https://devcenter.heroku.com/articles/heroku-cli")
        return
    
    # Verificar se está logado
    if not run_command("heroku auth:whoami", "Verificando login no Heroku"):
        print("\n❌ Não está logado no Heroku!")
        print("Execute: heroku login")
        return
    
    # Obter nome do app
    app_name = input("\n📝 Digite o nome do seu app no Heroku: ").strip()
    if not app_name:
        print("❌ Nome do app é obrigatório!")
        return
    
    # Verificar se o app existe
    if not run_command(f"heroku apps:info {app_name}", f"Verificando app {app_name}"):
        print(f"\n❌ App '{app_name}' não encontrado!")
        create = input("Deseja criar o app? (y/n): ").strip().lower()
        if create == 'y':
            if not run_command(f"heroku create {app_name}", f"Criando app {app_name}"):
                return
        else:
            return
    
    # Gerar chave secreta
    secret_key = generate_secret_key()
    print(f"\n🔑 Chave secreta gerada: {secret_key[:10]}...")
    
    # Configurar variáveis de ambiente
    env_vars = {
        "SECRET_KEY": secret_key,
        "DEBUG": "False",
        "LOG_LEVEL": "INFO",
        "API_V1_STR": "/api/v1",
        "PROJECT_NAME": "IFC Monitoring System"
    }
    
    for key, value in env_vars.items():
        if not run_command(f"heroku config:set {key}='{value}' -a {app_name}", f"Configurando {key}"):
            return
    
    # Adicionar PostgreSQL
    print(f"\n🗄️ Adicionando PostgreSQL ao app {app_name}...")
    if not run_command(f"heroku addons:create heroku-postgresql:mini -a {app_name}", "Adicionando PostgreSQL"):
        print("⚠️ PostgreSQL já pode estar configurado ou erro ao adicionar")
    
    # Fazer deploy
    print(f"\n🚀 Fazendo deploy para {app_name}...")
    if not run_command(f"git push heroku main", "Deploy para Heroku"):
        return
    
    # Abrir o app
    print(f"\n🌐 Abrindo o app...")
    run_command(f"heroku open -a {app_name}", "Abrindo app no navegador")
    
    print(f"\n✅ Deploy concluído com sucesso!")
    print(f"🌐 Seu app está disponível em: https://{app_name}.herokuapp.com")
    print(f"📚 Documentação da API: https://{app_name}.herokuapp.com/docs")

if __name__ == "__main__":
    main()
