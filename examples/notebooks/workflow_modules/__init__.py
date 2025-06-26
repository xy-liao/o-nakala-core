"""
O-Nakala Core Workflow Modules

Modular Python components for the NAKALA ultimate workflow, designed for
interactive Jupyter notebook execution and workshop demonstrations.

Compatible with o-nakala-core v2.4.1 from PyPI.
"""

from o_nakala_core.common.config import NakalaConfig
from o_nakala_core.upload import NakalaUploadClient
from o_nakala_core.collection import NakalaCollectionClient
from o_nakala_core.curator import NakalaCuratorClient, BatchModificationResult, CuratorConfig
from o_nakala_core.ml_engine import MLPatternLearner
from o_nakala_core.user_info import NakalaUserInfoClient

__version__ = "1.0.0"
__author__ = "O-Nakala Core Workshop"

__all__ = [
    "NakalaConfig",
    "NakalaUploadClient",
    "NakalaCollectionClient",
    "NakalaCuratorClient",
    "BatchModificationResult",
    "CuratorConfig",
    "MLPatternLearner",
    "NakalaUserInfoClient"
]