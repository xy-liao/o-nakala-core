"""Backward compatibility module for nakala_client.upload"""

import warnings

warnings.warn(
    "nakala_client.upload is deprecated. Use o_nakala_core.upload instead.",
    DeprecationWarning,
    stacklevel=2,
)

from o_nakala_core.upload import *
