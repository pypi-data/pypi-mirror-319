# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/tasks/cc/vision/hand_detector/proto/hand_detector_result.proto
# Protobuf Python Version: 4.25.5
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mediapipe.framework.formats import detection_pb2 as mediapipe_dot_framework_dot_formats_dot_detection__pb2
from mediapipe.framework.formats import rect_pb2 as mediapipe_dot_framework_dot_formats_dot_rect__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nHmediapipe/tasks/cc/vision/hand_detector/proto/hand_detector_result.proto\x12*mediapipe.tasks.vision.hand_detector.proto\x1a+mediapipe/framework/formats/detection.proto\x1a&mediapipe/framework/formats/rect.proto\"m\n\x12HandDetectorResult\x12(\n\ndetections\x18\x01 \x03(\x0b\x32\x14.mediapipe.Detection\x12-\n\nhand_rects\x18\x02 \x03(\x0b\x32\x19.mediapipe.NormalizedRect\"f\n\x13HandDetectorResults\x12O\n\x07results\x18\x01 \x03(\x0b\x32>.mediapipe.tasks.vision.hand_detector.proto.HandDetectorResult')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.tasks.cc.vision.hand_detector.proto.hand_detector_result_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_HANDDETECTORRESULT']._serialized_start=205
  _globals['_HANDDETECTORRESULT']._serialized_end=314
  _globals['_HANDDETECTORRESULTS']._serialized_start=316
  _globals['_HANDDETECTORRESULTS']._serialized_end=418
# @@protoc_insertion_point(module_scope)
