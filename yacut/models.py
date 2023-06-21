from datetime import datetime
from flask import request

from yacut import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, unique=True)
    short = db.Column(db.String(16))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=request.url_root + self.short,
        )

    def from_dict(self, data):
        setattr(self, 'original', data['url'])
        setattr(self, 'short', data['custom_id'])