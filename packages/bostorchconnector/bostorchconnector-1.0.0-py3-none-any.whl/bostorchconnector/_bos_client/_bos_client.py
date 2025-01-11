import logging
import os
import threading
from functools import partial
from typing import Optional, Any

#from bostorchconnector.src.bostorchconnector import BosReader, BosWriter
#from bostorchconnector.src.bostorchconnector._user_agent import UserAgent
from bostorchconnector._user_agent import UserAgent
from bostorchconnector import BosReader, BosWriter
from .bos_client_config import BosClientConfig

from _bos_client_imp import (
    BosClientImp,
    ObjectInfo,
    ListObjectStream,
    GetObjectStream,
)



"""
_bos_client.py
    Internal client wrapper class on top of Bos client implementation 
    with multi-process support.
"""


log = logging.getLogger(__name__)


def _identity(obj: Any) -> Any:
    return obj


_client_lock = threading.Lock()


class BosClient:
    def __init__(
        self,
        *,
        endpoint: Optional[str] = None,
        user_agent: Optional[UserAgent] = None,
        bos_client_config: Optional[BosClientConfig] = None,
        dataset_type: Optional[int] = 0,
        world_size: Optional[int] = None,
        rank: Optional[int] = None, 
        num_workers: Optional[int] = None, 
        worker_id: Optional[int] = None,
    ):
        self._endpoint = endpoint
        self._real_client: Optional[BosClientImp] = None
        self._client_pid: Optional[int] = None
        user_agent = user_agent or UserAgent()
        self._user_agent_prefix = user_agent.prefix
        self._bos_client_config = bos_client_config or BosClientConfig()
        self._dataset_type = dataset_type
        self._world_size = world_size
        self._rank = rank
        self._num_workers = num_workers
        self._worker_id = worker_id

    @property
    def _client(self) -> BosClientImp:
        # This is a fast check to avoid acquiring the lock unnecessarily.
        if self._client_pid is None or self._client_pid != os.getpid():
            # Acquire the lock to ensure thread-safety when creating the client.
            with _client_lock:
                # This double-check ensures that the client is only created once.
                if self._client_pid is None or self._client_pid != os.getpid():
                    # `BosClientImp` does not survive forking, so re-create it if the PID has changed.
                    self._real_client = self._client_builder()
                    self._client_pid = os.getpid()
        assert self._real_client is not None
        return self._real_client

    @property
    def bos_client_config(self) -> BosClientConfig:
        return self._bos_client_config

    @property
    def user_agent_prefix(self) -> str:
        return self._user_agent_prefix

    def _client_builder(self) -> BosClientImp:
        self._bos_client_config.credentials_path = os.path.expanduser(self._bos_client_config.credentials_path)
        return BosClientImp(
            user_agent_prefix = self._user_agent_prefix,
            bos_client_config = self._bos_client_config,
            endpoint = self._endpoint,
            world_size = self._world_size,
            rank = self._rank, 
            num_workers = self._num_workers, 
            worker_id = self._worker_id,
        )

    def get_object(
        self, bucket: str, key: str, *, object_info: Optional[ObjectInfo] = None
    ) -> BosReader:
        log.debug(f"GetObject bos://{bucket}/{key}, {object_info is None=}")
        if object_info is None:
            get_object_info = partial(self.head_object, bucket, key)
        else:
            get_object_info = partial(_identity, object_info)

        return BosReader(
            bucket,
            key,
            get_object_info=get_object_info,
            get_stream=partial(self._get_object_stream, bucket, key),
        )

    def _get_object_stream(self, bucket: str, key: str, size: Optional[int] = -1) -> GetObjectStream:
        return self._client.get_object(bucket, key, size)

    def put_object(
        self, bucket: str, key: str
    ) -> BosWriter:
        log.debug(f"PutObject bos://{bucket}/{key}")
        return BosWriter(self._client.put_object(bucket, key))

    # TODO: Probably need a ListObjectResult on dataset side
    def list_objects(
        self, bucket: str, prefix: str = "", delimiter: str = "/", max_keys: int = 1000
    ) -> ListObjectStream:
        log.debug(f"ListObjects bos://{bucket}/{prefix}")
        return self._client.list_objects(bucket, prefix, delimiter, max_keys, self._dataset_type)

    # TODO: We need ObjectInfo on dataset side
    def head_object(self, bucket: str, key: str) -> ObjectInfo:
        log.debug(f"HeadObject bos://{bucket}/{key}")
        return self._client.head_object(bucket, key)

    def delete_object(self, bucket: str, key: str) -> None:
        log.debug(f"DeleteObject bos://{bucket}/{key}")
        self._client.delete_object(bucket, key)

    def copy_object(
        self, src_bucket: str, src_key: str, dst_bucket: str, dst_key: str
    ) -> None:
        log.debug(
            f"CopyObject bos://{src_bucket}/{src_key} to bos://{dst_bucket}/{dst_key}"
        )
        return self._client.copy_object(src_bucket, src_key, dst_bucket, dst_key)
