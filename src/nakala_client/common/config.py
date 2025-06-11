"""Backward compatibility module for nakala_client.common.config"""

import warnings

warnings.warn(
    "nakala_client.common.config is deprecated. Use o_nakala_core.common.config instead.",
    DeprecationWarning,
    stacklevel=2,
)

from o_nakala_core.common.config import *
