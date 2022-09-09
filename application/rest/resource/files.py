from http import HTTPStatus
from flask import Blueprint, request, send_file, abort


from domain.repository import IStorage


def get_blueprint(storage: IStorage) -> Blueprint:
    bp = Blueprint('Files', __name__)

    @bp.get('/files/<string:key>')
    def get_file(key: str):
        file = storage.open(key)
        as_attachment = bool(request.args.get('as_attachment', False))

        if file is None:
            abort(HTTPStatus.NOT_FOUND)

        return send_file(
            file.stream,
            file.mimetype,
            attachment_filename=file.filename,
            as_attachment=as_attachment
        )

    return bp
