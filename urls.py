# urls.py
from flask import Blueprint, request, redirect, jsonify
import redis
from config import Config
from models import db, URL
from helpers import generate_short_url

urls_blueprint = Blueprint('urls', __name__)

redis_client = redis.StrictRedis(
    host=Config.REDIS_HOST, port=Config.REDIS_PORT, decode_responses=True)


@urls_blueprint.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.json.get('url')
    if not original_url:
        return jsonify({'error': 'URL is required'}), 400

    url_entry = URL.query.filter_by(original_url=original_url).first()
    if url_entry:
        short_url = url_entry.short_url
    else:
        short_url = generate_short_url()
        url_entry = URL(original_url=original_url, short_url=short_url)
        db.session.add(url_entry)
        db.session.commit()

    redis_client.set(short_url, original_url)
    return jsonify({'short_url': short_url}), 201


@urls_blueprint.route('/<short_url>')
def redirect_to_original(short_url):
    original_url = redis_client.get(short_url)
    if original_url:
        return redirect(original_url, code=302)
    else:
        return jsonify({'error': 'Short URL not found'}), 404

