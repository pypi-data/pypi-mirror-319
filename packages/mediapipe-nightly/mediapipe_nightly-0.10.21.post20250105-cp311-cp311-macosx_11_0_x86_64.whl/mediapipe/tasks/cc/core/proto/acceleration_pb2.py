# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/tasks/cc/core/proto/acceleration.proto
# Protobuf Python Version: 4.25.5
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mediapipe.calculators.tensor import inference_calculator_pb2 as mediapipe_dot_calculators_dot_tensor_dot_inference__calculator__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n0mediapipe/tasks/cc/core/proto/acceleration.proto\x12\x1amediapipe.tasks.core.proto\x1a\x37mediapipe/calculators/tensor/inference_calculator.proto\"\xb8\x02\n\x0c\x41\x63\x63\x65leration\x12I\n\x07xnnpack\x18\x01 \x01(\x0b\x32\x36.mediapipe.InferenceCalculatorOptions.Delegate.XnnpackH\x00\x12\x41\n\x03gpu\x18\x02 \x01(\x0b\x32\x32.mediapipe.InferenceCalculatorOptions.Delegate.GpuH\x00\x12G\n\x06tflite\x18\x04 \x01(\x0b\x32\x35.mediapipe.InferenceCalculatorOptions.Delegate.TfLiteH\x00\x12\x45\n\x05nnapi\x18\x05 \x01(\x0b\x32\x34.mediapipe.InferenceCalculatorOptions.Delegate.NnapiH\x00\x42\n\n\x08\x64\x65legateB:\n%com.google.mediapipe.tasks.core.protoB\x11\x41\x63\x63\x65lerationProto')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.tasks.cc.core.proto.acceleration_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n%com.google.mediapipe.tasks.core.protoB\021AccelerationProto'
  _globals['_ACCELERATION']._serialized_start=138
  _globals['_ACCELERATION']._serialized_end=450
# @@protoc_insertion_point(module_scope)
