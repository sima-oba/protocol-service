from flask import Flask
from flask_cors import CORS

from domain.model import ProtocolType
from domain.service import ProtocolService
from domain.service.protocol_handler import (
    NewUserHandler,
    DefaultHandler,
    PlantingAnticipationHandler
)
from infrastructure import database
from infrastructure.messaging import KafkaPublisher
from infrastructure.repository import ProtocolRepository, MongoStorage
from .encoder import CustomJsonEncoder
from .error import error_bp
from .security import Authorization, Role
from .resource import protocols, files


URL_PREFIX = '/api/v1/protocol'


def create_server(config):
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['JSON_SORT_KEYS'] = False
    app.json_encoder = CustomJsonEncoder
    app.register_blueprint(error_bp)

    db = database.get_database(config.MONGODB_SETTINGS)
    storage = MongoStorage(db, URL_PREFIX + '/files')

    CORS(app)
    auth = Authorization(config.INTROSPECTION_URI)
    auth.grant_role_for_any_request(Role.DEFAULT)
    # auth.require_authorization_for_any_request(app)

    publisher = KafkaPublisher({
        'bootstrap.servers': config.KAFKA_SERVER,
        'client.id': 'PROTOCOL',
        'message.max.bytes': 33554432
    })

    protocol_repo = ProtocolRepository(db)
    protocol_svc = ProtocolService(protocol_repo)
    protocol_svc.add_handler(ProtocolType.OTHER, DefaultHandler(storage))
    protocol_svc.add_handler(ProtocolType.NEW_USER, NewUserHandler(publisher))
    protocol_svc.add_handler(
        ProtocolType.PLANTING_ANTICIPATION,
        PlantingAnticipationHandler(storage)
    )

    protocol_bp = protocols.get_blueprint(protocol_svc)
    app.register_blueprint(protocol_bp, url_prefix=URL_PREFIX)

    files_bp = files.get_blueprint(storage)
    app.register_blueprint(files_bp, url_prefix=URL_PREFIX)

    return app
