# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/calculators/image/opencv_image_encoder_calculator.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nAmediapipe/calculators/image/opencv_image_encoder_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\"\x94\x01\n#OpenCvImageEncoderCalculatorOptions\x12\x0f\n\x07quality\x18\x01 \x01(\x05\x32\\\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\xfe\xb0\xc1l \x01(\x0b\x32..mediapipe.OpenCvImageEncoderCalculatorOptions\"\xdd\x01\n#OpenCvImageEncoderCalculatorResults\x12\x15\n\rencoded_image\x18\x01 \x01(\x0c\x12\x0e\n\x06height\x18\x02 \x01(\x05\x12\r\n\x05width\x18\x03 \x01(\x05\x12M\n\ncolorspace\x18\x04 \x01(\x0e\x32\x39.mediapipe.OpenCvImageEncoderCalculatorResults.ColorSpace\"1\n\nColorSpace\x12\x0b\n\x07UNKNOWN\x10\x00\x12\r\n\tGRAYSCALE\x10\x01\x12\x07\n\x03RGB\x10\x02')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.calculators.image.opencv_image_encoder_calculator_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_OPENCVIMAGEENCODERCALCULATOROPTIONS']._serialized_start=119
  _globals['_OPENCVIMAGEENCODERCALCULATOROPTIONS']._serialized_end=267
  _globals['_OPENCVIMAGEENCODERCALCULATORRESULTS']._serialized_start=270
  _globals['_OPENCVIMAGEENCODERCALCULATORRESULTS']._serialized_end=491
  _globals['_OPENCVIMAGEENCODERCALCULATORRESULTS_COLORSPACE']._serialized_start=442
  _globals['_OPENCVIMAGEENCODERCALCULATORRESULTS_COLORSPACE']._serialized_end=491
# @@protoc_insertion_point(module_scope)
