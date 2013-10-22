from flask_script import Server, Manager
from main import app

manager = Manager(app)

if __name__ == "__main__":
    manager.run()
