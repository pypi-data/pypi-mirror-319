# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/modules/face_geometry/protos/environment.proto
# Protobuf Python Version: 4.25.5
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n8mediapipe/modules/face_geometry/protos/environment.proto\x12\x17mediapipe.face_geometry\"L\n\x11PerspectiveCamera\x12\x1c\n\x14vertical_fov_degrees\x18\x01 \x01(\x02\x12\x0c\n\x04near\x18\x02 \x01(\x02\x12\x0b\n\x03\x66\x61r\x18\x03 \x01(\x02\"\xa2\x01\n\x0b\x45nvironment\x12K\n\x15origin_point_location\x18\x01 \x01(\x0e\x32,.mediapipe.face_geometry.OriginPointLocation\x12\x46\n\x12perspective_camera\x18\x02 \x01(\x0b\x32*.mediapipe.face_geometry.PerspectiveCamera*B\n\x13OriginPointLocation\x12\x16\n\x12\x42OTTOM_LEFT_CORNER\x10\x01\x12\x13\n\x0fTOP_LEFT_CORNER\x10\x02\x42=\n)com.google.mediapipe.modules.facegeometryB\x10\x45nvironmentProto')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.modules.face_geometry.protos.environment_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n)com.google.mediapipe.modules.facegeometryB\020EnvironmentProto'
  _globals['_ORIGINPOINTLOCATION']._serialized_start=328
  _globals['_ORIGINPOINTLOCATION']._serialized_end=394
  _globals['_PERSPECTIVECAMERA']._serialized_start=85
  _globals['_PERSPECTIVECAMERA']._serialized_end=161
  _globals['_ENVIRONMENT']._serialized_start=164
  _globals['_ENVIRONMENT']._serialized_end=326
# @@protoc_insertion_point(module_scope)
