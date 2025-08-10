from .qsartoolbox import QSARToolbox

try:  # pragma: no cover
	from importlib.metadata import version as _version
	__version__ = _version("pyqsartoolbox")
except Exception:  # pragma: no cover
	__version__ = "0.0.0"

__all__ = ["QSARToolbox", "__version__"]