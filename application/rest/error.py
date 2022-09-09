from http import HTTPStatus
from flask import Blueprint, jsonify
from marshmallow import ValidationError

from domain.exception import (
    EntityNotFoundError,
    InvalidStateError,
    MissingFileError,
    WrongFileTypeError
)


error_bp = Blueprint('Error Handling', __name__)


@error_bp.app_errorhandler(ValidationError)
def handle_validation_error(error: ValidationError):
    return jsonify(error.messages), HTTPStatus.BAD_REQUEST


@error_bp.app_errorhandler(EntityNotFoundError)
def handle_entity_not_found(error: EntityNotFoundError):
    return jsonify({'error': str(error)}), HTTPStatus.NOT_FOUND


@error_bp.app_errorhandler(InvalidStateError)
def handle_invalid_state(error: InvalidStateError):
    return jsonify({'error': str(error)}), HTTPStatus.CONFLICT


@error_bp.app_errorhandler(WrongFileTypeError)
def handle_wrong_file_type(error: WrongFileTypeError):
    return jsonify({'error': str(error)}), HTTPStatus.BAD_REQUEST


@error_bp.app_errorhandler(MissingFileError)
def handle_missing_file(error: MissingFileError):
    return jsonify({'error': str(error)}), HTTPStatus.BAD_REQUEST
