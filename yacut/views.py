from flask import render_template, flash, request, redirect

from . import app, db
from .constans import MAX_LENGTH
from .forms import URLform
from .models import URLMap
from .utils import get_unique_short_id, check_allowed_symbols


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLform()
    if form.validate_on_submit():
        short = form.custom_id.data
        if URLMap.query.filter_by(short=short).first() is not None:
            flash('Имя {} уже занято!'.format(short))
            return render_template('main.html', form=form)
        if short is not None and not check_allowed_symbols(short):
            flash('Указан недопустимый символ в короткой ссылке. '
                  'Достпустимые символы: A-z, 0-9.')
            return render_template('main.html', form=form)
        if not short:
            short = get_unique_short_id()
        if len(short) > MAX_LENGTH:
            flash('Короткая ссылка не должна привышать 16 символов')
            return render_template('main.html', form=form)

        url_map = URLMap(
            original=form.original_link.data,
            short=short
        )
        db.session.add(url_map)
        db.session.commit()
        new_url = f'{request.url_root}{short}'
        flash('Ваша новая ссылка готова:')

        return render_template('main.html', form=form, new_url=new_url)

    return render_template('main.html', form=form)


@app.route('/<short_id>')
def rederect_url(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_map.original)
