"""
O-Nakala Core Workflow Modules

Modular Python components for the NAKALA ultimate workflow, designed for
interactive Jupyter notebook execution and workshop demonstrations.

Compatible with o-nakala-core v2.3.0 from PyPI.
"""

__version__ = "1.0.0"
__author__ = "O-Nakala Core Workshop"

# Import main workflow components
from .workflow_config import WorkflowConfig
from .data_uploader import DataUploader
from .collection_manager import CollectionManager
from .metadata_enhancer import MetadataEnhancer
from .curator_operations import CuratorOperations
from .quality_analyzer import QualityAnalyzer
from .workflow_summary import WorkflowSummary

__all__ = [
    "WorkflowConfig",
    "DataUploader", 
    "CollectionManager",
    "MetadataEnhancer",
    "CuratorOperations",
    "QualityAnalyzer",
    "WorkflowSummary"
]