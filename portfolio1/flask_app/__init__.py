import os
from flask import Flask

MODEL_FILEPATH = os.path.join(os.path.dirname(__file__), 'model.pkl')

def create_app():
    app = Flask(__name__)
    
    from flask_app.views.main_views import main_bp
    
    app.register_blueprint(main_bp)
    
    return app

create_app().run()