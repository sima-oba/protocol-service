from http import HTTPStatus
from flask import Blueprint, jsonify, request
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import UnsupportedMediaType

from domain.service import ProtocolService

from ...schema import ProtocolSchema
from . import util

_FORM_MIMETYPES = ['application/x-www-form-urlencoded', 'multipart/form-data']


def _enforce_form_mimetype():
    if request.mimetype not in _FORM_MIMETYPES:
        raise UnsupportedMediaType()


def get_blueprint(service: ProtocolService) -> Blueprint:
    bp = Blueprint('Protocols', __name__)
    protocol_schema = ProtocolSchema()

    @bp.get('/protocols')
    def get_all():
        filter = request.args.to_dict()
        protocols = service.search_protocols(filter)
        return jsonify(protocols)

    @bp.get('/protocols/<string:_id>')
    def get_one(_id: str):
        protocol = service.get_protocol(_id)
        return jsonify(protocol)

    @bp.post('/protocols')
    def submit():
        _enforce_form_mimetype()

        if 'protocol' not in request.form.keys():
            raise ValidationError({'protocol': 'Missing form field'})

        data = protocol_schema.loads(request.form['protocol'])
        files = util.extract_all_files()
        protocol = service.create(data, files)

        return jsonify(protocol), HTTPStatus.CREATED

    @bp.put('/protocols/<string:_id>/accept')
    def accept(_id: str):
        return jsonify(service.accept(_id))

    @bp.put('/protocols/<string:_id>/cancel')
    def cancel(_id: str):
        _enforce_form_mimetype()

        message = request.form.get('message')
        files = util.extract_all_files()

        return jsonify(service.cancel(_id, message, files))

    @bp.put('/protocols/<string:_id>/complete')
    def complete(_id: str):
        _enforce_form_mimetype()

        message = request.form.get('message')
        files = util.extract_all_files()

        return jsonify(service.complete(_id, message, files))

    return bp
