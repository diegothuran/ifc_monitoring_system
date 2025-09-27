#!/usr/bin/env python3
"""
Script para configurar o banco de dados no Heroku
"""

import os
import sys
from sqlalchemy import create_engine
from backend.models import Base
from backend.core.database import engine

def setup_database():
    """Configura o banco de dados criando todas as tabelas"""
    try:
        print("🔄 Configurando banco de dados...")
        
        # Criar todas as tabelas
        Base.metadata.create_all(bind=engine)
        
        print("✅ Banco de dados configurado com sucesso!")
        print("📊 Tabelas criadas:")
        
        # Listar tabelas criadas
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        for table in tables:
            print(f"  - {table}")
            
        return True
        
    except Exception as e:
        print(f"❌ Erro ao configurar banco de dados: {e}")
        return False

if __name__ == "__main__":
    success = setup_database()
    sys.exit(0 if success else 1)
