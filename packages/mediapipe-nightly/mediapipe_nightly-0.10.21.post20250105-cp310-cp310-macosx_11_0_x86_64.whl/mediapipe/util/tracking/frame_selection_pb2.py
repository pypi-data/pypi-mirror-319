# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mediapipe/util/tracking/frame_selection.proto
# Protobuf Python Version: 4.25.5
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from mediapipe.util.tracking import camera_motion_pb2 as mediapipe_dot_util_dot_tracking_dot_camera__motion__pb2
from mediapipe.util.tracking import frame_selection_solution_evaluator_pb2 as mediapipe_dot_util_dot_tracking_dot_frame__selection__solution__evaluator__pb2
from mediapipe.util.tracking import region_flow_pb2 as mediapipe_dot_util_dot_tracking_dot_region__flow__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n-mediapipe/util/tracking/frame_selection.proto\x12\tmediapipe\x1a+mediapipe/util/tracking/camera_motion.proto\x1a@mediapipe/util/tracking/frame_selection_solution_evaluator.proto\x1a)mediapipe/util/tracking/region_flow.proto\"e\n\x17\x46rameSelectionTimestamp\x12\x11\n\ttimestamp\x18\x01 \x01(\x03\x12\x11\n\tframe_idx\x18\x02 \x01(\x05\x12$\n\x18processed_from_timestamp\x18\x03 \x01(\x03:\x02-1\"\xc6\x01\n\x14\x46rameSelectionResult\x12\x11\n\ttimestamp\x18\x01 \x01(\x03\x12\x11\n\tframe_idx\x18\x02 \x01(\x05\x12.\n\rcamera_motion\x18\x03 \x01(\x0b\x32\x17.mediapipe.CameraMotion\x12\x32\n\x08\x66\x65\x61tures\x18\x04 \x01(\x0b\x32 .mediapipe.RegionFlowFeatureList\x12$\n\x18processed_from_timestamp\x18\x05 \x01(\x03:\x02-1\"\xdc\x01\n\x17\x46rameSelectionCriterion\x12\x18\n\rsampling_rate\x18\x01 \x01(\x05:\x01\x30\x12\x1c\n\x10\x62\x61ndwidth_frames\x18\x02 \x01(\x02:\x02\x35\x30\x12\x1f\n\x14search_radius_frames\x18\x03 \x01(\x05:\x01\x31\x12J\n\x12solution_evaluator\x18\x04 \x01(\x0b\x32..mediapipe.FrameSelectionSolutionEvaluatorType\x12\x1c\n\x11max_output_frames\x18\x05 \x01(\x05:\x01\x30\"g\n\x15\x46rameSelectionOptions\x12\x35\n\tcriterion\x18\x01 \x03(\x0b\x32\".mediapipe.FrameSelectionCriterion\x12\x17\n\nchunk_size\x18\x02 \x01(\x05:\x03\x31\x30\x30')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'mediapipe.util.tracking.frame_selection_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_FRAMESELECTIONTIMESTAMP']._serialized_start=214
  _globals['_FRAMESELECTIONTIMESTAMP']._serialized_end=315
  _globals['_FRAMESELECTIONRESULT']._serialized_start=318
  _globals['_FRAMESELECTIONRESULT']._serialized_end=516
  _globals['_FRAMESELECTIONCRITERION']._serialized_start=519
  _globals['_FRAMESELECTIONCRITERION']._serialized_end=739
  _globals['_FRAMESELECTIONOPTIONS']._serialized_start=741
  _globals['_FRAMESELECTIONOPTIONS']._serialized_end=844
# @@protoc_insertion_point(module_scope)
