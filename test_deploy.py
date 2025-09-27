#!/usr/bin/env python3
"""
Script para testar se o deploy no Heroku funcionou corretamente
"""

import requests
import sys
import json

def test_endpoint(url, description):
    """Testa um endpoint da API"""
    try:
        print(f"🔄 Testando {description}...")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print(f"✅ {description} - OK")
            return True
        else:
            print(f"❌ {description} - Status: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ {description} - Erro: {e}")
        return False

def main():
    # Obter URL do app
    app_url = input("🌐 Digite a URL do seu app (ex: https://meu-app.herokuapp.com): ").strip()
    
    if not app_url:
        print("❌ URL é obrigatória!")
        return
    
    # Remover barra final se existir
    if app_url.endswith('/'):
        app_url = app_url[:-1]
    
    print(f"\n🧪 Testando deploy do app: {app_url}")
    print("=" * 50)
    
    # Testes
    tests = [
        (f"{app_url}/", "Página inicial"),
        (f"{app_url}/health", "Health check"),
        (f"{app_url}/docs", "Documentação da API"),
        (f"{app_url}/api/v1", "API v1"),
    ]
    
    passed = 0
    total = len(tests)
    
    for url, description in tests:
        if test_endpoint(url, description):
            passed += 1
        print()
    
    # Resultado
    print("=" * 50)
    print(f"📊 Resultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram! Deploy funcionando perfeitamente!")
        print(f"📚 Acesse a documentação em: {app_url}/docs")
    else:
        print("⚠️ Alguns testes falharam. Verifique os logs do Heroku:")
        print("   heroku logs --tail -a nome-do-seu-app")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
