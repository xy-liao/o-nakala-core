"""
Backward compatibility package for nakala_client.

This package provides compatibility for existing imports while transitioning
to the new o_nakala_core module structure.

DEPRECATED: Use 'import o_nakala_core' instead.
This compatibility layer will be removed in a future version.
"""

import warnings

# Issue deprecation warning
warnings.warn(
    "The 'nakala_client' package is deprecated. "
    "Please use 'o_nakala_core' instead. "
    "This compatibility layer will be removed in v3.0.0.",
    DeprecationWarning,
    stacklevel=2
)

# Import and re-export everything from o_nakala_core
try:
    from o_nakala_core import *
    from o_nakala_core import __version__, __author__
    
    # Re-export main classes for backward compatibility
    from o_nakala_core.upload import NakalaUploadClient
    from o_nakala_core.collection import NakalaCollectionClient
    from o_nakala_core.curator import NakalaCuratorClient, CuratorConfig, BatchModificationResult
    from o_nakala_core.common.config import NakalaConfig
    from o_nakala_core.common.utils import NakalaCommonUtils, NakalaPathResolver
    from o_nakala_core.common.exceptions import NakalaError, NakalaValidationError, NakalaAPIError
    
except ImportError as e:
    raise ImportError(
        f"Failed to import o_nakala_core: {e}. "
        "Please ensure o_nakala_core is properly installed."
    ) from e