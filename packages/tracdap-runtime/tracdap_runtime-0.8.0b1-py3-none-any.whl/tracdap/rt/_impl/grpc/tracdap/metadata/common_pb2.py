# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tracdap/rt/_impl/grpc/tracdap/metadata/common.proto
# Protobuf Python Version: 4.25.3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n3tracdap/rt/_impl/grpc/tracdap/metadata/common.proto\x12\x10tracdap.metadata\"5\n\nTenantInfo\x12\x12\n\ntenantCode\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t*L\n\x0eMetadataFormat\x12\x1b\n\x17METADATA_FORMAT_NOT_SET\x10\x00\x12\t\n\x05PROTO\x10\x01\x12\x08\n\x04JSON\x10\x02\x12\x08\n\x04YAML\x10\x03*H\n\x0fMetadataVersion\x12\x1c\n\x18METADATA_VERSION_NOT_SET\x10\x00\x12\x06\n\x02V1\x10\x01\x12\x0b\n\x07\x43URRENT\x10\x01\x1a\x02\x10\x01\x42\x1e\n\x1aorg.finos.tracdap.metadataP\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tracdap.rt._impl.grpc.tracdap.metadata.common_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\032org.finos.tracdap.metadataP\001'
  _globals['_METADATAVERSION']._options = None
  _globals['_METADATAVERSION']._serialized_options = b'\020\001'
  _globals['_METADATAFORMAT']._serialized_start=128
  _globals['_METADATAFORMAT']._serialized_end=204
  _globals['_METADATAVERSION']._serialized_start=206
  _globals['_METADATAVERSION']._serialized_end=278
  _globals['_TENANTINFO']._serialized_start=73
  _globals['_TENANTINFO']._serialized_end=126
# @@protoc_insertion_point(module_scope)
