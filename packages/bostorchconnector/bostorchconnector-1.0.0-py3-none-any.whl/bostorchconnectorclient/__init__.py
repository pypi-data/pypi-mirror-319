

import copyreg

from ._logger_patch import TRACE as LOG_TRACE
from ._logger_patch import _install_trace_logging
from ._bos_client_imp import BosException, __version__

_install_trace_logging()


def _bos_exception_reduce(exc: BosException):
    return S3Exception, exc.args


copyreg.pickle(BosException, _bos_exception_reduce)

__all__ = ["LOG_TRACE", "BosException", "__version__"]
