#!/usr/bin/env python3
"""
Script to fix database enum issues
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import sqlite3
from backend.core.database import engine
from backend.models import Base
from backend.models.user import User, UserRole
from backend.auth.security import get_password_hash

def fix_database():
    """Fix database enum issues"""
    
    # Drop and recreate all tables
    print("🗑️  Removendo banco de dados antigo...")
    if os.path.exists("ifc_monitoring.db"):
        os.remove("ifc_monitoring.db")
    
    print("🏗️  Criando novo banco de dados...")
    Base.metadata.create_all(bind=engine)
    
    # Create admin user with correct enum
    from backend.core.database import SessionLocal
    db = SessionLocal()
    
    try:
        admin_user = User(
            username="admin",
            email="admin@ifcmonitoring.com",
            full_name="Administrador do Sistema",
            hashed_password=get_password_hash("admin123"),
            role=UserRole.ADMIN,
            is_active=True,
            is_superuser=True
        )
        
        db.add(admin_user)
        db.commit()
        
        print("✅ Usuário admin criado com sucesso!")
        print("=" * 50)
        print("🔐 CREDENCIAIS DE LOGIN:")
        print("Username: admin")
        print("Password: admin123")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Erro ao criar usuário admin: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_database()
