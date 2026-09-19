# Concept: why we need to seed roles before signup works
# User.role_id has nullable=False — every user MUST belong to a role.
# But nothing creates roles automatically. This script runs once,
# manually, to insert the starting roles so signup has something to assign.


from database import SessionLocal
from models import Role

db = SessionLocal()

for role_name in ["admin","user","hr"]:
    existing = db.query(Role).filter(Role.name== role_name).first()
    if not existing:
        db.add(Role(name=role_name))
        print(f"Added role: {role_name}")

db.commit()
db.close()
print("Done Seeding roles.")