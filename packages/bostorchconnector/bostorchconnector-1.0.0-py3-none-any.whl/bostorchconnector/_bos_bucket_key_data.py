
from typing import NamedTuple, Optional

from _bos_client_imp import ObjectInfo


class BosBucketKeyData(NamedTuple):
    """Read-only information about object stored in Bos."""

    bucket: str
    key: str
    object_info: Optional[ObjectInfo] = None
