"""Backward compatibility module for nakala_client.collection"""
import warnings
warnings.warn("nakala_client.collection is deprecated. Use o_nakala_core.collection instead.", DeprecationWarning, stacklevel=2)

from o_nakala_core.collection import *