from tracdap.rt._impl.grpc.tracdap.metadata import object_id_pb2 as _object_id_pb2
from tracdap.rt._impl.grpc.tracdap.metadata import type_pb2 as _type_pb2
from tracdap.rt._impl.grpc.tracdap.metadata import data_pb2 as _data_pb2
from tracdap.rt._impl.grpc.tracdap.metadata import model_pb2 as _model_pb2
from tracdap.rt._impl.grpc.tracdap.metadata import flow_pb2 as _flow_pb2
from tracdap.rt._impl.grpc.tracdap.metadata import job_pb2 as _job_pb2
from tracdap.rt._impl.grpc.tracdap.metadata import file_pb2 as _file_pb2
from tracdap.rt._impl.grpc.tracdap.metadata import custom_pb2 as _custom_pb2
from tracdap.rt._impl.grpc.tracdap.metadata import stoarge_pb2 as _stoarge_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ObjectDefinition(_message.Message):
    __slots__ = ("objectType", "data", "model", "flow", "job", "file", "custom", "storage", "schema", "objectProps")
    class ObjectPropsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _type_pb2.Value
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_type_pb2.Value, _Mapping]] = ...) -> None: ...
    OBJECTTYPE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    FLOW_FIELD_NUMBER: _ClassVar[int]
    JOB_FIELD_NUMBER: _ClassVar[int]
    FILE_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_FIELD_NUMBER: _ClassVar[int]
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    OBJECTPROPS_FIELD_NUMBER: _ClassVar[int]
    objectType: _object_id_pb2.ObjectType
    data: _data_pb2.DataDefinition
    model: _model_pb2.ModelDefinition
    flow: _flow_pb2.FlowDefinition
    job: _job_pb2.JobDefinition
    file: _file_pb2.FileDefinition
    custom: _custom_pb2.CustomDefinition
    storage: _stoarge_pb2.StorageDefinition
    schema: _data_pb2.SchemaDefinition
    objectProps: _containers.MessageMap[str, _type_pb2.Value]
    def __init__(self, objectType: _Optional[_Union[_object_id_pb2.ObjectType, str]] = ..., data: _Optional[_Union[_data_pb2.DataDefinition, _Mapping]] = ..., model: _Optional[_Union[_model_pb2.ModelDefinition, _Mapping]] = ..., flow: _Optional[_Union[_flow_pb2.FlowDefinition, _Mapping]] = ..., job: _Optional[_Union[_job_pb2.JobDefinition, _Mapping]] = ..., file: _Optional[_Union[_file_pb2.FileDefinition, _Mapping]] = ..., custom: _Optional[_Union[_custom_pb2.CustomDefinition, _Mapping]] = ..., storage: _Optional[_Union[_stoarge_pb2.StorageDefinition, _Mapping]] = ..., schema: _Optional[_Union[_data_pb2.SchemaDefinition, _Mapping]] = ..., objectProps: _Optional[_Mapping[str, _type_pb2.Value]] = ...) -> None: ...
