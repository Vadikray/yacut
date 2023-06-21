from flask import jsonify, request
from http import HTTPStatus


from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id, check_allowed_symbols


@app.route('/api/id/', methods=['POST'])
def craate_short_url():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса', HTTPStatus.BAD_REQUEST)
    if 'url' not in data or data['url'] == '':
        raise InvalidAPIUsage('\"url\" является обязательным полем!', HTTPStatus.BAD_REQUEST)
    if 'custom_id' not in data or data['custom_id'] == '' or data['custom_id'] is None:
        data['custom_id'] = get_unique_short_id()
    if URLMap.query.filter_by(short=data['custom_id']).first() is not None:
        raise InvalidAPIUsage('Имя "{}" уже занято.'.format(data['custom_id']), HTTPStatus.BAD_REQUEST)
    if len(data['custom_id']) > 16 or not check_allowed_symbols(data['custom_id']):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки', HTTPStatus.BAD_REQUEST)

    url_map = URLMap()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_url(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK
