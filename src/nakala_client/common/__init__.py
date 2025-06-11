"""Backward compatibility module for nakala_client.common"""

import warnings

warnings.warn(
    "nakala_client.common is deprecated. Use o_nakala_core.common instead.",
    DeprecationWarning,
    stacklevel=2,
)

from o_nakala_core.common import *
