import asyncio
import json
import logging
import sys

import pika

from .exceptions import MessengerBusNotSentException
from .message_handler import DefaultCommand

from .stamp import (AmqpStamp, SendingStamp, AMQPBasicProperties, ReceivedStamp, BusStamp,
                    TransportStamp, SentStamp, NotSentStamp, SkipReceivedStamp)
from .envelope import (Envelope)

FORMAT = '%(asctime)s %(levelname)s:%(name)s:%(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('messenger_transport')
logger.setLevel(logging.DEBUG)


class TransportDefinitionInterface:
    def __init__(self,definition):
        self.name = definition.get("name")
        self.dsn = definition.get("dsn")
        self.options = definition.get("options", {})


class AMQPTransportDefinition(TransportDefinitionInterface):
    def __init__(self,definition:dict={}):
        super().__init__(definition)



class TransportInterface:
    """
    """
    def __init__(self, definition:TransportDefinitionInterface):
        self.definition = definition

    def dispatch(self, message,options) -> Envelope:
        """ permet d'envoyer un message dans le bus"""
        raise NotImplementedError

    def produce(self, envelope: Envelope) -> Envelope:
        """ envoi final en destination du broker message"""
        raise NotImplementedError



class SyncTransport(TransportInterface):
    def __init__(self,definition:TransportDefinitionInterface):
        super().__init__(definition)

    def dispatch(self, message, options) -> Envelope:
        """
        ceci est la methode public pour envoyer un message dans le bus
        format de message envoyer est le json
        """
        stamps = [
            SendingStamp()
        ] + options.get("stamps",[])

        envelope = Envelope(message, stamps)

        del options["stamps"]
        envelope = envelope.update(TransportStamp(self,options))
        stamp:BusStamp = envelope.last("BusStamp")
        _envelope = stamp.bus.run(envelope)
        return _envelope


    def produce(self, envelope: Envelope) -> Envelope:
        """ envoi final en destination du broker message"""

        stamps = [
            envelope.last("BusStamp"),
            envelope.last("TransportStamp"),
            ReceivedStamp()
        ]

        _envelope = Envelope(envelope.message, stamps)
        stamp:BusStamp = _envelope.last("BusStamp")
        _envelope = stamp.bus.run(_envelope)
        #_envelope = _envelope.update(SkipReceivedStamp())
        return _envelope


class ClientServerTransport(TransportInterface):
    def __init__(self,definition:TransportDefinitionInterface):
        super().__init__(definition)

    def create_connection(self, *args,**kwargs):
        raise NotImplementedError

    def _send(self, *args, **kwargs) -> Envelope:
        """ envoi un message """
        raise NotImplementedError

    def retry(self,*args, **kwargs):
        """ permet d'envoyer a nouveau les echecs"""
        raise NotImplementedError

    async def consume(self,*args,**kwargs):
        """ reception direct à partir du broker message"""
        raise NotImplementedError


class AMQPTransport(ClientServerTransport):
    def __init__(self,definition:AMQPTransportDefinition):
        super().__init__(definition)

        self._connection = None
        self._channel = None
        self._queue_name = None
        self._exchange_name = ""

    def create_connection(self, use_default_exchange=False, custom_queue_name:str = ""):

        if self._connection:
            return self._connection, self._channel, self._queue_name, self._exchange_name

        logger.debug("Connecting...")
        node1 = pika.URLParameters(self.definition.dsn)
        nodes = [node1]
        connection = pika.BlockingConnection(parameters=node1)
        logger.debug("Connection...OK")

        logger.debug("Creation channel, exchange, queue...")
        channel = connection.channel()
        channel.confirm_delivery()
        channel.basic_qos(prefetch_count=1)

        queue_name = custom_queue_name if custom_queue_name else self.definition.options.get('queue').get("name")
        exchange_name = self.definition.options.get('exchange').get("name")



        if not use_default_exchange:
            channel.exchange_declare(
                exchange=exchange_name,
                exchange_type=self.definition.options.get('exchange').get("type"),
                durable=self.definition.options.get('exchange').get("durable")
            )

            channel.queue_declare(
                queue_name,
                durable=self.definition.options.get('queue').get("durable"),
                arguments={"x-max-priority": 10}
            )

            logger.debug("Creation channel, exchange, queue...OK")

            logger.debug("Binding queue to exchange...")
            for binding_key in self.definition.options.get('queue').get("binding").split(" "):
                channel.queue_bind(
                    exchange=exchange_name,
                    queue=queue_name,
                    routing_key=binding_key
                )
            logger.debug("Binding queue to exchange...OK")
        else:
            exchange_name = ""

            if not custom_queue_name:
                rst = channel.queue_declare(queue="", exclusive=True)
                queue_name = rst.method.queue
            else:
                channel.queue_declare(queue=custom_queue_name, exclusive=True)

        self._connection, self._channel, self._queue_name, self._exchange_name = connection, channel, queue_name, exchange_name
        return (connection, channel, queue_name, exchange_name)


    def _send(self, message, options: dict) -> Envelope:
        """ envoi un message """

        routing_key = options.get("routing_key", "")
        properties = options.get("properties", {})

        attr = AMQPBasicProperties()
        attr.content_type = properties["content_type"] if "content_type" in properties else attr.content_type
        attr.content_encoding = properties[
            "content_encoding"] if "content_encoding" in properties else attr.content_encoding
        attr.headers = properties["headers"] if "headers" in properties else attr.headers
        attr.delivery_mode = properties["delivery_mode"] if "delivery_mode" in properties else attr.delivery_mode
        attr.priority = properties["priority"] if "priority" in properties else attr.priority
        attr.correlation_id = properties["correlation_id"] if "correlation_id" in properties else attr.correlation_id
        attr.reply_to = properties["reply_to"] if "reply_to" in properties else attr.reply_to
        attr.expiration = properties["expiration"] if "expiration" in properties else attr.expiration
        attr.message_id = properties["message_id"] if "message_id" in properties else attr.message_id
        attr.timestamp = properties["timestamp"] if "timestamp" in properties else attr.timestamp
        attr.type = properties["type"] if "type" in properties else attr.type
        attr.user_id = properties["user_id"] if "user_id" in properties else attr.user_id
        attr.app_id = properties["app_id"] if "app_id" in properties else attr.app_id
        attr.cluster_id = properties["cluster_id"] if "cluster_id" in properties else attr.cluster_id

        stamps = [
            AmqpStamp(routing_key, 2, attr),
            SendingStamp()
        ] + options.get("stamps",[])


        envelope = Envelope(message, stamps)
        stamp:BusStamp = envelope.last("BusStamp")
        bus = stamp.bus
        envelope = bus.run(envelope)
        return envelope

    def dispatch(self, message, options) -> Envelope:
        """
        ceci est la methode public pour envoyer un message dans le bus
        format de message envoyer est le json
        """
        properties = options.get("properties",{})

        default_properties = {
            "content_type": "application/json",
            "delivery_mode": pika.spec.PERSISTENT_DELIVERY_MODE,
            "headers": {}
        }
        default_properties.update(properties)
        options["properties"] = default_properties
        return self._send(message, options)

    def receive(self, body: str,properties):
        """
        reception d'un message en provenance du serveur,
        il est aussitôt envoyé dans le bus pour traitement
        """
        from .service_container import serializer
        from .stamp import BusStamp
        from .bus import MessageBus

        encoded_envelope = {
            "body": body,
            "headers": properties.get("headers",{}),
        }

        envelope = serializer.decode(encoded_envelope)

        attr = AMQPBasicProperties()
        attr.content_type = properties["content_type"] if "content_type" in properties else attr.content_type
        attr.content_encoding = properties[
            "content_encoding"] if "content_encoding" in properties else attr.content_encoding
        attr.headers = properties["headers"] if "headers" in properties else attr.headers
        attr.delivery_mode = properties["delivery_mode"] if "delivery_mode" in properties else attr.delivery_mode
        attr.priority = properties["priority"] if "priority" in properties else attr.priority
        attr.correlation_id = properties["correlation_id"] if "correlation_id" in properties else attr.correlation_id
        attr.reply_to = properties["reply_to"] if "reply_to" in properties else attr.reply_to
        attr.expiration = properties["expiration"] if "expiration" in properties else attr.expiration
        attr.message_id = properties["message_id"] if "message_id" in properties else attr.message_id
        attr.timestamp = properties["timestamp"] if "timestamp" in properties else attr.timestamp
        attr.type = properties["type"] if "type" in properties else attr.type
        attr.user_id = properties["user_id"] if "user_id" in properties else attr.user_id
        attr.app_id = properties["app_id"] if "app_id" in properties else attr.app_id
        attr.cluster_id = properties["cluster_id"] if "cluster_id" in properties else attr.cluster_id

        envelope = envelope.update(
            AmqpStamp(properties["headers"].get("x-routing-key",""), attributes=attr),
            ReceivedStamp()
        )
        stamp:BusStamp = envelope.last("BusStamp")
        bus:MessageBus = stamp.bus
        envelope = bus.run(envelope)
        return envelope

    def produce(self,envelope:Envelope) -> Envelope:
        from .service_container import serializer

        stamp: AmqpStamp = envelope.last("AmqpStamp")
        properties = stamp.attributes.__dict__
        routing_key = stamp.routing_key
        body = envelope.message

        if "headers" not in properties:
            properties["headers"] = {}

        properties["headers"]["x-useragent"] = "Aaz/producer:1.1.0-alpha"

        r = serializer.encode(envelope)

        if "body" in r:
            body = r["body"]

        if "headers" in r:
            properties["headers"].update(r['headers'])

        properties = {k: v for k, v in properties.items() if v != None}
        connection = None
        self._connection = None
        try:
            connection, channel, queue_name, exchange_name = self.create_connection()
            channel.basic_publish(
                exchange=exchange_name,
                routing_key=routing_key,
                body=body.encode(),
                properties=pika.BasicProperties(**properties)
            )
            envelope = envelope.update(SentStamp())
        except Exception as e:
            logger.debug(e)
            envelope = envelope.update(NotSentStamp())
            if "x-retry" not in properties["headers"]:
                # on enregistre le message en base de donnée en failed
                raise MessengerBusNotSentException(body,properties)

        finally:
            if connection:
                connection.close()

        return envelope

    async def consume(self, on_message_callback:callable = None, once:bool = False):
        # result = channel.queue_declare('', exclusive=True, durable=True)
        # queue_name = result.method.queue
        max_attempts = 100

        if not on_message_callback:
            on_message_callback = self._on_message

        while True:
            connection = None
            self._connection = None
            try:
                connection, channel, queue_name, exchange_name = self.create_connection()
                channel.basic_consume(queue=queue_name, on_message_callback=on_message_callback, auto_ack=False)

                try:
                    channel.start_consuming()
                except KeyboardInterrupt:
                    channel.stop_consuming()
                    if connection:
                        connection.close()
                    break

            except pika.exceptions.ConnectionClosedByBroker:
                # Uncomment this to make the example not attempt recovery
                # from server-initiated connection closure, including
                # when the node is stopped cleanly
                # except pika.exceptions.ConnectionClosedByBroker:
                #     pass
                logger.debug("Impossible de se connecter au serveur")

            except pika.exceptions.AMQPConnectionError as e:
                logger.debug("Impossible de se connecter au serveur")
                # Do not recover on channel errors

            except pika.exceptions.AMQPChannelError as err:
                logger.debug("Caught a channel error: {}, stopping...".format(err))
                print("Caught a channel error: {}, stopping...".format(err))

            except Exception as e:
                logger.debug(e)
                continue
            finally:
                logger.debug("Reconnection du service...")

            await asyncio.sleep(1)

            # max_attempts -= 1

    def _on_message(self, ch, method, properties, body):

        try:
            print(" [x] %r:%r" % (method.routing_key, body))
            # task = asyncio.create_task(message_bus.receive(body.decode(),properties.__dict__))
            self.receive(body.decode(), properties.__dict__)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            from .service_container import message_bus
            from .service_container import class_loader

            logger.debug(e)
            ch.basic_ack(delivery_tag=method.delivery_tag)

            try:
                _props = properties.__dict__
                message = json.loads(body.decode())
                _headers = {"x-retry": True, "x-retry-count": 0}

                if "x-retry-count" in properties.headers:
                    _headers["x-retry-count"] = properties.headers["x-retry-count"] + 1

                _props["headers"].update(_headers)

                options = {
                    "properties":_props,
                    "bus": _props["headers"].get("BusStamp","event.bus"),
                    "transport": _props["headers"].get("TransportStamp", "async"),
                }

                if "CommandInterface" in _props["headers"]:
                    _module = _props["headers"].get("CommandInterface").split(".")
                    _class_name = _module.pop()
                    _module = ".".join(_module)

                    try:
                        instance = class_loader(_module, _class_name)
                        instance._hydrate(message)
                        body = instance
                    except:
                        cmd = DefaultCommand()
                        for k, v in message.items():
                            setattr(cmd, k, v)
                        body = cmd

                else:
                    cmd = DefaultCommand()
                    for k, v in message.items():
                        setattr(cmd, k, v)
                    body = cmd

                message_bus.dispatch(body,options)
            except Exception as ee:
                logger.debug(ee)

    async def consume_once(self, queue_name:str):
        self._channel.queue_declare(queue=queue_name, exclusive=True)

        for method, properties, body in self._channel.consume(queue_name):
            # Display the message parts and acknowledge the message
            logger.debug(method)
            logger.debug(properties)
            logger.debug(body)
            self._channel.basic_ack(method.delivery_tag)

            # Escape out of the loop after 10 messages
            if method.delivery_tag == 10:
                break
            return json.loads(body.decode())





class TransportManager:
    """
    le transport manager, il sert a orchestrer tout les transport
    """
    def __init__(self, transports: dict):
        self._transports = {}

        transports["__default__"] = {
            "dsn":"sync://"
        }

        for k,transport_def in transports.items():
            transport_def["name"] = k
            self.add(transport_def)

    def __getitem__(self, item):
        return self.get(item)

    def get(self, name:str):
        return self._transports.get(name)

    def add(self, definition):
        """ ajoute un transport au manager"""
        dsn:str = definition.get("dsn")
        if dsn:
            v:list = dsn.split("://")
            protocol = v.pop(0).lower()

            if protocol not in ["amqp","amqps","sync"]:
                raise Exception("transport {} not supported".format(protocol))

            transport:TransportInterface = None
            if protocol in ["amqp","amqps"]:
                transport = AMQPTransport(AMQPTransportDefinition(definition))
            elif protocol == "sync":
                transport = SyncTransport(TransportDefinitionInterface(definition))

            self._transports[definition.get("name")] = transport
        return self

    def remove(self, transport_name:str):
        """ supprime un transport au manager"""
        del self._transports[transport_name]
        return self

