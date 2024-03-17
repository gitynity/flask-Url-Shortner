from flask import Flask
from .config import Config
from .models import db
from .urls import urls_bp
import redis

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database and Redis
db.init_app(app)
redis_client = redis.StrictRedis(
    host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'],
    db=app.config['REDIS_DB'])

# Register blueprint
app.register_blueprint(urls_bp, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True)
