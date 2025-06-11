"""Backward compatibility module for nakala_client.curator"""
import warnings
warnings.warn("nakala_client.curator is deprecated. Use o_nakala_core.curator instead.", DeprecationWarning, stacklevel=2)

from o_nakala_core.curator import *