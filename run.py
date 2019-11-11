from app import create_app, db
from app.models import User, Stock, Todo, Embed


app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Stock': Stock,
        'Todo': Todo,
        'Embed': Embed}
