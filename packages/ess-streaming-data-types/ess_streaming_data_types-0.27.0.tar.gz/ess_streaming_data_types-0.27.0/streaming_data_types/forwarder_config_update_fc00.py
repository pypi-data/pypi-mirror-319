from collections import namedtuple
from typing import List, Union

import flatbuffers
from flatbuffers.packer import struct as flatbuffer_struct

from streaming_data_types.fbschemas.forwarder_config_update_fc00 import (
    Protocol,
    Stream,
    UpdateType,
    fc00_ConfigUpdate,
)
from streaming_data_types.utils import check_schema_identifier

FILE_IDENTIFIER = b"fc00"

ConfigurationUpdate = namedtuple("ConfigurationUpdate", ("config_change", "streams"))

StreamInfo = namedtuple(
    "StreamInfo", ("channel", "schema", "topic", "protocol", "periodic")
)


def deserialise_fc00(buffer: Union[bytearray, bytes]) -> ConfigurationUpdate:
    """
    Deserialise FlatBuffer fc00.

    :param buffer: The FlatBuffers buffer.
    :return: The deserialised data.
    """
    check_schema_identifier(buffer, FILE_IDENTIFIER)

    config_message = fc00_ConfigUpdate.fc00_ConfigUpdate.GetRootAsfc00_ConfigUpdate(
        buffer, 0
    )

    streams = []
    try:
        for i in range(config_message.StreamsLength()):
            stream_message = config_message.Streams(i)
            streams.append(
                StreamInfo(
                    (
                        stream_message.Channel().decode("utf-8")
                        if stream_message.Channel()
                        else ""
                    ),
                    (
                        stream_message.Schema().decode("utf-8")
                        if stream_message.Schema()
                        else ""
                    ),
                    (
                        stream_message.Topic().decode("utf-8")
                        if stream_message.Topic()
                        else ""
                    ),
                    stream_message.Protocol(),
                    stream_message.Periodic() if stream_message.Periodic() else 0,
                )
            )
    except flatbuffer_struct.error:
        pass  # No streams in buffer

    return ConfigurationUpdate(config_message.ConfigChange(), streams)


def serialise_stream(
    builder: flatbuffers.Builder,
    protocol: Protocol,
    channel_offset: int,
    schema_offset: int,
    topic_offset: int,
    periodic_offset: int,
) -> int:
    Stream.StreamStart(builder)
    Stream.StreamAddProtocol(builder, protocol)
    Stream.StreamAddTopic(builder, topic_offset)
    Stream.StreamAddSchema(builder, schema_offset)
    Stream.StreamAddChannel(builder, channel_offset)
    Stream.StreamAddPeriodic(builder, periodic_offset)
    return Stream.StreamEnd(builder)


def serialise_fc00(config_change: UpdateType, streams: List[StreamInfo]) -> bytes:
    """
    Serialise config update message as an fc00 FlatBuffers message.

    :param config_change:
    :param streams: channel, schema and output topic configurations
    :return:
    """
    builder = flatbuffers.Builder(1024)
    builder.ForceDefaults(True)

    if streams:
        # We have to use multiple loops/list comprehensions here because we cannot create strings after we have
        # called StreamStart and cannot create streams after we have called StartVector
        stream_field_offsets = [
            (
                builder.CreateString(stream.channel),
                builder.CreateString(stream.schema),
                builder.CreateString(stream.topic),
            )
            for stream in streams
        ]
        stream_offsets = [
            serialise_stream(builder, stream.protocol, *stream_fields, stream.periodic)
            for stream, stream_fields in zip(streams, stream_field_offsets)
        ]

        fc00_ConfigUpdate.fc00_ConfigUpdateStartStreamsVector(builder, len(streams))
        for stream_offset in stream_offsets:
            builder.PrependUOffsetTRelative(stream_offset)
        streams_offset = builder.EndVector()

    # Build the actual buffer
    fc00_ConfigUpdate.fc00_ConfigUpdateStart(builder)
    if streams:
        fc00_ConfigUpdate.fc00_ConfigUpdateAddStreams(builder, streams_offset)
    fc00_ConfigUpdate.fc00_ConfigUpdateAddConfigChange(builder, config_change)
    data = fc00_ConfigUpdate.fc00_ConfigUpdateEnd(builder)

    builder.Finish(data, file_identifier=FILE_IDENTIFIER)
    return bytes(builder.Output())
