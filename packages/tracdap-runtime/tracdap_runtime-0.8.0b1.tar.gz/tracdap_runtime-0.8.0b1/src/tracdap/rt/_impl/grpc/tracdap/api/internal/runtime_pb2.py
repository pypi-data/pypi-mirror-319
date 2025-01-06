# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tracdap/rt/_impl/grpc/tracdap/api/internal/runtime.proto
# Protobuf Python Version: 4.25.3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from tracdap.rt._impl.grpc.tracdap.metadata import object_id_pb2 as tracdap_dot_rt_dot___impl_dot_grpc_dot_tracdap_dot_metadata_dot_object__id__pb2
from tracdap.rt._impl.grpc.tracdap.metadata import job_pb2 as tracdap_dot_rt_dot___impl_dot_grpc_dot_tracdap_dot_metadata_dot_job__pb2
from tracdap.rt._impl.grpc.tracdap.metadata import object_pb2 as tracdap_dot_rt_dot___impl_dot_grpc_dot_tracdap_dot_metadata_dot_object__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n8tracdap/rt/_impl/grpc/tracdap/api/internal/runtime.proto\x12\x14tracdap.api.internal\x1a\x36tracdap/rt/_impl/grpc/tracdap/metadata/object_id.proto\x1a\x30tracdap/rt/_impl/grpc/tracdap/metadata/job.proto\x1a\x33tracdap/rt/_impl/grpc/tracdap/metadata/object.proto\x1a\x1cgoogle/api/annotations.proto\"6\n\x16RuntimeListJobsRequest\x12\x12\n\x05limit\x18\x01 \x01(\rH\x00\x88\x01\x01\x42\x08\n\x06_limit\"O\n\x17RuntimeListJobsResponse\x12\x34\n\x04jobs\x18\x01 \x03(\x0b\x32&.tracdap.api.internal.RuntimeJobStatus\"f\n\x15RuntimeJobInfoRequest\x12\x34\n\x0bjobSelector\x18\x01 \x01(\x0b\x32\x1d.tracdap.metadata.TagSelectorH\x00\x12\x10\n\x06jobKey\x18\x02 \x01(\tH\x00\x42\x05\n\x03job\"\x9f\x01\n\x10RuntimeJobStatus\x12*\n\x05jobId\x18\x01 \x01(\x0b\x32\x1b.tracdap.metadata.TagHeader\x12\x33\n\nstatusCode\x18\x02 \x01(\x0e\x32\x1f.tracdap.metadata.JobStatusCode\x12\x15\n\rstatusMessage\x18\x03 \x01(\t\x12\x13\n\x0b\x65rrorDetail\x18\x04 \x01(\t\"\xa4\x02\n\x10RuntimeJobResult\x12*\n\x05jobId\x18\x01 \x01(\x0b\x32\x1b.tracdap.metadata.TagHeader\x12\x33\n\nstatusCode\x18\x02 \x01(\x0e\x32\x1f.tracdap.metadata.JobStatusCode\x12\x15\n\rstatusMessage\x18\x03 \x01(\t\x12\x44\n\x07results\x18\x04 \x03(\x0b\x32\x33.tracdap.api.internal.RuntimeJobResult.ResultsEntry\x1aR\n\x0cResultsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x31\n\x05value\x18\x02 \x01(\x0b\x32\".tracdap.metadata.ObjectDefinition:\x02\x38\x01\x32\x95\x03\n\x0eTracRuntimeApi\x12{\n\x08listJobs\x12,.tracdap.api.internal.RuntimeListJobsRequest\x1a-.tracdap.api.internal.RuntimeListJobsResponse\"\x12\x82\xd3\xe4\x93\x02\x0c\x12\n/list-jobs\x12\x81\x01\n\x0cgetJobStatus\x12+.tracdap.api.internal.RuntimeJobInfoRequest\x1a&.tracdap.api.internal.RuntimeJobStatus\"\x1c\x82\xd3\xe4\x93\x02\x16\x12\x14/job-status/{jobKey}\x12\x81\x01\n\x0cgetJobResult\x12+.tracdap.api.internal.RuntimeJobInfoRequest\x1a&.tracdap.api.internal.RuntimeJobResult\"\x1c\x82\xd3\xe4\x93\x02\x16\x12\x14/job-result/{jobKey}B\"\n\x1eorg.finos.tracdap.api.internalP\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tracdap.rt._impl.grpc.tracdap.api.internal.runtime_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\036org.finos.tracdap.api.internalP\001'
  _globals['_RUNTIMEJOBRESULT_RESULTSENTRY']._options = None
  _globals['_RUNTIMEJOBRESULT_RESULTSENTRY']._serialized_options = b'8\001'
  _globals['_TRACRUNTIMEAPI'].methods_by_name['listJobs']._options = None
  _globals['_TRACRUNTIMEAPI'].methods_by_name['listJobs']._serialized_options = b'\202\323\344\223\002\014\022\n/list-jobs'
  _globals['_TRACRUNTIMEAPI'].methods_by_name['getJobStatus']._options = None
  _globals['_TRACRUNTIMEAPI'].methods_by_name['getJobStatus']._serialized_options = b'\202\323\344\223\002\026\022\024/job-status/{jobKey}'
  _globals['_TRACRUNTIMEAPI'].methods_by_name['getJobResult']._options = None
  _globals['_TRACRUNTIMEAPI'].methods_by_name['getJobResult']._serialized_options = b'\202\323\344\223\002\026\022\024/job-result/{jobKey}'
  _globals['_RUNTIMELISTJOBSREQUEST']._serialized_start=271
  _globals['_RUNTIMELISTJOBSREQUEST']._serialized_end=325
  _globals['_RUNTIMELISTJOBSRESPONSE']._serialized_start=327
  _globals['_RUNTIMELISTJOBSRESPONSE']._serialized_end=406
  _globals['_RUNTIMEJOBINFOREQUEST']._serialized_start=408
  _globals['_RUNTIMEJOBINFOREQUEST']._serialized_end=510
  _globals['_RUNTIMEJOBSTATUS']._serialized_start=513
  _globals['_RUNTIMEJOBSTATUS']._serialized_end=672
  _globals['_RUNTIMEJOBRESULT']._serialized_start=675
  _globals['_RUNTIMEJOBRESULT']._serialized_end=967
  _globals['_RUNTIMEJOBRESULT_RESULTSENTRY']._serialized_start=885
  _globals['_RUNTIMEJOBRESULT_RESULTSENTRY']._serialized_end=967
  _globals['_TRACRUNTIMEAPI']._serialized_start=970
  _globals['_TRACRUNTIMEAPI']._serialized_end=1375
# @@protoc_insertion_point(module_scope)
