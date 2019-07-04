import os

from flask import jsonify

from config import config
from app import create_app

flask_env = os.getenv('FLASK_ENV', 'production')
app = create_app(config=config[flask_env])


@app.route('/')
def status():
    return jsonify({
        'status': 'success',
        'message': 'up and running'
    })


if __name__ == "__main__":
    app.run()
