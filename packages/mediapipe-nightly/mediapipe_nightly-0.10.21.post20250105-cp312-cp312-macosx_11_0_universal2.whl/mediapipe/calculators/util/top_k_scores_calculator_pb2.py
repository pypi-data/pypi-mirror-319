# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/calculators/util/top_k_scores_calculator.proto
# Protobuf Python Version: 4.25.5
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mediapipe.framework import calculator_pb2 as mediapipe_dot_framework_dot_calculator__pb2
try:
  mediapipe_dot_framework_dot_calculator__options__pb2 = mediapipe_dot_framework_dot_calculator__pb2.mediapipe_dot_framework_dot_calculator__options__pb2
except AttributeError:
  mediapipe_dot_framework_dot_calculator__options__pb2 = mediapipe_dot_framework_dot_calculator__pb2.mediapipe.framework.calculator_options_pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n8mediapipe/calculators/util/top_k_scores_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\"\xae\x01\n\x1bTopKScoresCalculatorOptions\x12\r\n\x05top_k\x18\x01 \x01(\x05\x12\x11\n\tthreshold\x18\x02 \x01(\x02\x12\x16\n\x0elabel_map_path\x18\x03 \x01(\t2U\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\x8c\xba\xa9\x81\x01 \x01(\x0b\x32&.mediapipe.TopKScoresCalculatorOptions')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.calculators.util.top_k_scores_calculator_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_TOPKSCORESCALCULATOROPTIONS']._serialized_start=110
  _globals['_TOPKSCORESCALCULATOROPTIONS']._serialized_end=284
# @@protoc_insertion_point(module_scope)
