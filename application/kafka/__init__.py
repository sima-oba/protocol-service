from domain.model import ProtocolType
from domain.service import ProtocolService
from domain.service.protocol_handler import NewUserHandler
from infrastructure import database
from infrastructure.messaging import KafkaPublisher
from infrastructure.repository import ProtocolRepository

from ..schema import ProtocolSchema
from .consumer import Consumer, ConsumerGroup


def start_consumer(config):
    db = database.get_database(config.MONGODB_SETTINGS)
    consumer_group = ConsumerGroup({
        'bootstrap.servers': config.KAFKA_SERVER,
        'group.id': 'PROTOCOL',
        'enable.auto.commit': False,
        'auto.offset.reset': 'earliest'
    })

    publisher = KafkaPublisher({
        'bootstrap.servers': config.KAFKA_SERVER,
        'client.id': 'PROTOCOL',
        'message.max.bytes': 4 * 1024 ** 2
    })

    protocol_repo = ProtocolRepository(db)
    protocol_svc = ProtocolService(protocol_repo)
    protocol_svc.add_handler(ProtocolType.NEW_USER, NewUserHandler(publisher))

    protocol_consumer = Consumer(ProtocolSchema(), protocol_svc.create)
    consumer_group.add(protocol_consumer, 'NEW_USER')
    consumer_group.wait()
