#!/usr/bin/env python3
"""
Simple script to create admin user
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.core.database import SessionLocal, engine
from backend.models import Base, User
from backend.models.user import UserRole
from backend.auth.security import get_password_hash

def create_admin_user():
    """Create default admin user"""
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Create admin user directly
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
    create_admin_user()


