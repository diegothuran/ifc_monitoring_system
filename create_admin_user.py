#!/usr/bin/env python3
"""
Script to create a default admin user for the IFC Monitoring System
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.core.database import SessionLocal, engine
from backend.models import Base, User
from backend.models.user import UserRole
from backend.auth.security import get_password_hash
from sqlalchemy.orm import sessionmaker

def create_admin_user():
    """Create default admin user"""
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Check if admin user already exists
        existing_admin = db.query(User).filter(User.username == "admin").first()
        
        if existing_admin:
            print("✅ Usuário admin já existe!")
            print(f"Username: admin")
            print(f"Email: {existing_admin.email}")
            print(f"Role: {existing_admin.role}")
            return
        
        # Create admin user
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
        db.refresh(admin_user)
        
        print("✅ Usuário admin criado com sucesso!")
        print("=" * 50)
        print("🔐 CREDENCIAIS DE LOGIN:")
        print("Username: admin")
        print("Password: admin123")
        print("=" * 50)
        print("⚠️  IMPORTANTE: Altere a senha após o primeiro login!")
        
    except Exception as e:
        print(f"❌ Erro ao criar usuário admin: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()

