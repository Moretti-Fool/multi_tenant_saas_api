import typer
from database import SessionLocal
from models import Admin
from utils.auth import get_password_hash

app = typer.Typer()  # Define the Typer application

@app.command("create-admin")  # Define the command explicitly
def create_admin(
    email: str = typer.Option(..., prompt=True),
    password: str = typer.Option(..., prompt=True, hide_input=True),
    superadmin: bool = typer.Option(False, "--superadmin")
):
    """Create a new admin user"""
    db = SessionLocal()
    try:
        hashed_pwd = get_password_hash(password)
        admin = Admin(
            email=email,
            hashed_password=hashed_pwd,
            is_superadmin=superadmin
        )
        db.add(admin)
        db.commit()
        typer.echo(f"Admin {email} created successfully!")
    except Exception as e:
        db.rollback()
        typer.echo(f"Error: {str(e)}")
    finally:
        db.close()

app.command()(create_admin)

if __name__ == "__main__":
    app()  # Run the Typer application
