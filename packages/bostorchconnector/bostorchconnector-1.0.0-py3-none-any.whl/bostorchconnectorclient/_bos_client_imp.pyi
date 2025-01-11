

from typing import List, Optional

# This interface is unstable!
class BosClientImp:
    user_agent_prefix: str
    bos_client_config: Optional[object]
    profile: Optional[str]
    dataset_type: Optional[int]
    endpoint: Optional[str]
    world_size: Optional[int]
    rank: Optional[int]
    num_workers: Optional[int]
    worker_id: Optional[int]

    def __init__(
        self,
        user_agent_prefix: str = "",
        bos_client_config: Optional[object] = None,
        profile: Optional[str] = None,
        dataset_type: Optional[int] = 0,
        endpoint: Optional[str] = None,
        world_size: Optional[int] = 1,
        rank: Optional[int] = 0,
        num_workers: Optional[int] = 1,
        worker_id: Optional[int] = 0,
    ): ...
    def get_object(self, bucket: str, key: str) -> GetObjectStream: ...
    def put_object(
        self, bucket: str, key: str
    ) -> PutObjectStream: ...
    def list_objects(
        self, bucket: str, prefix: str = "", delimiter: str = "", max_keys: int = 1000
    ) -> ListObjectStream: ...
    def head_object(self, bucket: str, key: str) -> ObjectInfo: ...
    def delete_object(self, bucket: str, key: str) -> None: ...
    def copy_object(
        self, src_bucket: str, src_key: str, dst_bucket: str, dst_key: str
    ) -> None: ...

class GetObjectStream:
    bucket: str
    key: str

    def __iter__(self) -> GetObjectStream: ...
    def __next__(self) -> bytes: ...
    def tell(self) -> int: ...

class PutObjectStream:
    bucket: str
    key: str
    def write(self, data: bytes) -> None: ...
    def close(self) -> None: ...

class ObjectInfo:
    key: str
    etag: str
    size: int
    last_modified: int

    def __init__(
        self,
        key: str,
        etag: str,
        size: int,
        last_modified: int,
    ): ...

class ListObjectResult:
    object_info: List[ObjectInfo]
    common_prefixes: List[str]

class ListObjectStream:
    bucket: str
    continuation_token: Optional[str]
    complete: bool
    prefix: str
    delimiter: str
    max_keys: int

    def __iter__(self) -> ListObjectStream: ...
    def __next__(self) -> ListObjectResult: ...
    @staticmethod
    def _from_state(
        client: BosClientImp,
        bucket: str,
        prefix: str,
        delimiter: str,
        max_keys: int,
        continuation_token: Optional[str],
        complete: bool,
    ) -> ListObjectStream: ...

class BosException(Exception):
    pass

__version__: str
