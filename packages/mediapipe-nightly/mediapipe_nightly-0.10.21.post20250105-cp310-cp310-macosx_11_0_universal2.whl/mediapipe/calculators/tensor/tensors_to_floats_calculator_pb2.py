# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/calculators/tensor/tensors_to_floats_calculator.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n?mediapipe/calculators/tensor/tensors_to_floats_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\"\xf5\x01\n TensorsToFloatsCalculatorOptions\x12P\n\nactivation\x18\x01 \x01(\x0e\x32\x36.mediapipe.TensorsToFloatsCalculatorOptions.Activation:\x04NONE\"#\n\nActivation\x12\x08\n\x04NONE\x10\x00\x12\x0b\n\x07SIGMOID\x10\x01\x32Z\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\xeb\xc2\xe5\xa3\x01 \x01(\x0b\x32+.mediapipe.TensorsToFloatsCalculatorOptions')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.calculators.tensor.tensors_to_floats_calculator_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_TENSORSTOFLOATSCALCULATOROPTIONS']._serialized_start=117
  _globals['_TENSORSTOFLOATSCALCULATOROPTIONS']._serialized_end=362
  _globals['_TENSORSTOFLOATSCALCULATOROPTIONS_ACTIVATION']._serialized_start=235
  _globals['_TENSORSTOFLOATSCALCULATOROPTIONS_ACTIVATION']._serialized_end=270
# @@protoc_insertion_point(module_scope)
