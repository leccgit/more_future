# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: 01_protobufs_search_demo.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1e\x30\x31_protobufs_search_demo.proto\"N\n\x0fSearchRequest01\x12\r\n\x05query\x18\x01 \x01(\t\x12\x13\n\x0bpage_number\x18\x02 \x01(\x05\x12\x17\n\x0fresult_per_page\x18\x03 \x01(\x05\"\xd3\x01\n\x0fSearchRequest02\x12\r\n\x05query\x18\x01 \x01(\t\x12\x13\n\x0bpage_number\x18\x02 \x01(\x05\x12\x17\n\x0fresult_per_page\x18\x03 \x01(\x05\x12\'\n\x06\x63orpus\x18\x04 \x01(\x0e\x32\x17.SearchRequest02.Corpus\"Z\n\x06\x43orpus\x12\r\n\tUNIVERSAL\x10\x00\x12\x07\n\x03WEB\x10\x01\x12\n\n\x06IMAGES\x10\x02\x12\t\n\x05LOCAL\x10\x03\x12\x08\n\x04NEWS\x10\x04\x12\x0c\n\x08PRODUCTS\x10\x05\x12\t\n\x05VIDEO\x10\x06\"\xd3\x01\n\x0fSearchRequest03\x12\r\n\x05query\x18\x01 \x01(\t\x12\x13\n\x0bpage_number\x18\x02 \x01(\x05\x12\x17\n\x0fresult_per_page\x18\x03 \x01(\x05\x12\'\n\x06\x63orpus\x18\x04 \x01(\x0e\x32\x17.SearchRequest03.Corpus\"Z\n\x06\x43orpus\x12\r\n\tUNIVERSAL\x10\x00\x12\x07\n\x03WEB\x10\x01\x12\n\n\x06IMAGES\x10\x02\x12\t\n\x05LOCAL\x10\x03\x12\x08\n\x04NEWS\x10\x04\x12\x0c\n\x08PRODUCTS\x10\x05\x12\t\n\x05VIDEO\x10\x06\x62\x06proto3')



_SEARCHREQUEST01 = DESCRIPTOR.message_types_by_name['SearchRequest01']
_SEARCHREQUEST02 = DESCRIPTOR.message_types_by_name['SearchRequest02']
_SEARCHREQUEST03 = DESCRIPTOR.message_types_by_name['SearchRequest03']
_SEARCHREQUEST02_CORPUS = _SEARCHREQUEST02.enum_types_by_name['Corpus']
_SEARCHREQUEST03_CORPUS = _SEARCHREQUEST03.enum_types_by_name['Corpus']
SearchRequest01 = _reflection.GeneratedProtocolMessageType('SearchRequest01', (_message.Message,), {
  'DESCRIPTOR' : _SEARCHREQUEST01,
  '__module__' : '01_protobufs_search_demo_pb2'
  # @@protoc_insertion_point(class_scope:SearchRequest01)
  })
_sym_db.RegisterMessage(SearchRequest01)

SearchRequest02 = _reflection.GeneratedProtocolMessageType('SearchRequest02', (_message.Message,), {
  'DESCRIPTOR' : _SEARCHREQUEST02,
  '__module__' : '01_protobufs_search_demo_pb2'
  # @@protoc_insertion_point(class_scope:SearchRequest02)
  })
_sym_db.RegisterMessage(SearchRequest02)

SearchRequest03 = _reflection.GeneratedProtocolMessageType('SearchRequest03', (_message.Message,), {
  'DESCRIPTOR' : _SEARCHREQUEST03,
  '__module__' : '01_protobufs_search_demo_pb2'
  # @@protoc_insertion_point(class_scope:SearchRequest03)
  })
_sym_db.RegisterMessage(SearchRequest03)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _SEARCHREQUEST01._serialized_start=34
  _SEARCHREQUEST01._serialized_end=112
  _SEARCHREQUEST02._serialized_start=115
  _SEARCHREQUEST02._serialized_end=326
  _SEARCHREQUEST02_CORPUS._serialized_start=236
  _SEARCHREQUEST02_CORPUS._serialized_end=326
  _SEARCHREQUEST03._serialized_start=329
  _SEARCHREQUEST03._serialized_end=540
  _SEARCHREQUEST03_CORPUS._serialized_start=236
  _SEARCHREQUEST03_CORPUS._serialized_end=326
# @@protoc_insertion_point(module_scope)