# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/calculators/util/detection_label_id_to_text_calculator.proto
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
from mediapipe.util import label_map_pb2 as mediapipe_dot_util_dot_label__map__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\nFmediapipe/calculators/util/detection_label_id_to_text_calculator.proto\x12\tmediapipe\x1a$mediapipe/framework/calculator.proto\x1a\x1emediapipe/util/label_map.proto\"\xee\x02\n\'DetectionLabelIdToTextCalculatorOptions\x12\x16\n\x0elabel_map_path\x18\x01 \x01(\t\x12\r\n\x05label\x18\x02 \x03(\t\x12\x15\n\rkeep_label_id\x18\x03 \x01(\x08\x12W\n\x0blabel_items\x18\x04 \x03(\x0b\x32\x42.mediapipe.DetectionLabelIdToTextCalculatorOptions.LabelItemsEntry\x1aJ\n\x0fLabelItemsEntry\x12\x0b\n\x03key\x18\x01 \x01(\x03\x12&\n\x05value\x18\x02 \x01(\x0b\x32\x17.mediapipe.LabelMapItem:\x02\x38\x01\x32`\n\x03\x65xt\x12\x1c.mediapipe.CalculatorOptions\x18\xb0\x8b\x8ex \x01(\x0b\x32\x32.mediapipe.DetectionLabelIdToTextCalculatorOptions')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.calculators.util.detection_label_id_to_text_calculator_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_DETECTIONLABELIDTOTEXTCALCULATOROPTIONS_LABELITEMSENTRY']._options = None
  _globals['_DETECTIONLABELIDTOTEXTCALCULATOROPTIONS_LABELITEMSENTRY']._serialized_options = b'8\001'
  _globals['_DETECTIONLABELIDTOTEXTCALCULATOROPTIONS']._serialized_start=156
  _globals['_DETECTIONLABELIDTOTEXTCALCULATOROPTIONS']._serialized_end=522
  _globals['_DETECTIONLABELIDTOTEXTCALCULATOROPTIONS_LABELITEMSENTRY']._serialized_start=350
  _globals['_DETECTIONLABELIDTOTEXTCALCULATOROPTIONS_LABELITEMSENTRY']._serialized_end=424
# @@protoc_insertion_point(module_scope)
