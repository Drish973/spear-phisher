from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    db.create_all()  # creates tables if they don't exist
    admin_email = "admin@example.com"

    # Avoid creating duplicate admin
    existing = User.query.filter_by(email=admin_email).first()
    if existing:
        print("Admin already exists:", existing.email)
    else:
        admin = User(email=admin_email)
        admin.set_password("strongpassword")
        db.session.add(admin)
        db.session.commit()
        print("Admin created:", admin.email)