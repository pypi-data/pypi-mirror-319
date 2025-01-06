# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/calculators/image/recolor_calculator.proto
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
from mediapipe.util import color_pb2 as mediapipe_dot_util_dot_color__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n4mediapipe/calculators/image/recolor_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\x1a\x1amediapipe/util/color.proto\"\xcb\x02\n\x18RecolorCalculatorOptions\x12J\n\x0cmask_channel\x18\x01 \x01(\x0e\x32/.mediapipe.RecolorCalculatorOptions.MaskChannel:\x03RED\x12\x1f\n\x05\x63olor\x18\x02 \x01(\x0b\x32\x10.mediapipe.Color\x12\x1a\n\x0binvert_mask\x18\x03 \x01(\x08:\x05\x66\x61lse\x12#\n\x15\x61\x64just_with_luminance\x18\x04 \x01(\x08:\x04true\".\n\x0bMaskChannel\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x07\n\x03RED\x10\x01\x12\t\n\x05\x41LPHA\x10\x02\x32Q\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\x8d\x84\xb5x \x01(\x0b\x32#.mediapipe.RecolorCalculatorOptions')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.calculators.image.recolor_calculator_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_RECOLORCALCULATOROPTIONS']._serialized_start=134
  _globals['_RECOLORCALCULATOROPTIONS']._serialized_end=465
  _globals['_RECOLORCALCULATOROPTIONS_MASKCHANNEL']._serialized_start=336
  _globals['_RECOLORCALCULATOROPTIONS_MASKCHANNEL']._serialized_end=382
# @@protoc_insertion_point(module_scope)
