
from functools import partial
from typing import Iterator, Any, Union, Iterable, Callable, Optional
import logging

import torch.utils.data
import torch

from . import BosReader
from ._bos_bucket_key_data import BosBucketKeyData
from ._bos_client import BosClient, BosClientConfig
from ._bos_dataset_common import (
    identity,
    get_objects_from_uris,
    get_objects_from_prefix,
)

log = logging.getLogger(__name__)


class BosIterableDataset(torch.utils.data.IterableDataset):
    """An IterableStyle dataset created from Bos objects.

    To create an instance of BosIterableDataset, you need to use
    `from_prefix` or `from_objects` methods.
    """

    def __init__(
        self,
        get_dataset_objects: Callable[[BosClient], Iterable[BosBucketKeyData]],
        endpoint: Optional[str] = None,
        transform: Callable[[BosReader], Any] = identity,
        bos_client_config: Optional[BosClientConfig] = None,
        enable_sharding: bool = True,
    ):
        self._get_dataset_objects = get_dataset_objects
        self._transform = transform
        self._endpoint = endpoint
        self._bos_client_config = bos_client_config
        self._client = None
        self._enable_sharding = enable_sharding

        self._rank = 0
        self._world_size = 1
        if torch.distributed.is_initialized():
            self._rank = torch.distributed.get_rank()
            self._world_size = torch.distributed.get_world_size()

    @property
    def endpoint(self):
        return self._endpoint

    @classmethod
    def from_objects(
        cls,
        object_uris: Union[str, Iterable[str]],
        *,
        endpoint: Optional[str] = None,
        transform: Callable[[BosReader], Any] = identity,
        bos_client_config: Optional[BosClientConfig] = None,
        enable_sharding: bool = True,
    ):
        """Returns an instance of BosIterableDataset using the Bos URI(s) provided.

        Args:
          object_uris(str | Iterable[str]): Bos URI of the object(s) desired.
          endpoint(str): Bos endpoint of the Bos bucket where the objects are stored.
          transform: Optional callable which is used to transform an BosReader into the desired type.
          bos_client_config: Optional BosClientConfig with parameters for Bos client.
          enable_sharding: If True (default), shard the dataset across multiple workers for parallel data loading. If False, each worker loads the entire dataset independently.

        Returns:
            BosIterableDataset: An IterableStyle dataset created from Bos objects.

        Raises:
            BosException: An error occurred accessing Bos.
        """
        log.info(f"Building {cls.__name__} from_objects")
        return cls(
            partial(get_objects_from_uris, object_uris),
            endpoint,
            transform=transform,
            bos_client_config=bos_client_config,
            enable_sharding=enable_sharding,
        )

    @classmethod
    def from_prefix(
        cls,
        bos_uri: str,
        *,
        endpoint: Optional[str] = None,
        transform: Callable[[BosReader], Any] = identity,
        bos_client_config: Optional[BosClientConfig] = None,
        enable_sharding: bool = True,
    ):
        """Returns an instance of BosIterableDataset using the Bos URI provided.

        Args:
          bos_uri(str): An Bos URI (prefix) of the object(s) desired. Objects matching the prefix will be included in the returned dataset.
          endpoint(str): Bos endpoint of the Bos bucket where the objects are stored.
          transform: Optional callable which is used to transform an BosReader into the desired type.
          bos_client_config: Optional BosClientConfig with parameters for Bos client.
          enable_sharding: If True (default), shard the dataset across multiple workers for parallel data loading. If False, each worker loads the entire dataset independently.

        Returns:
            BosIterableDataset: An IterableStyle dataset created from Bos objects.

        Raises:
            BosException: An error occurred accessing Bos.
        """
        log.info(f"Building {cls.__name__} from_prefix {bos_uri=}")
        return cls(
            partial(get_objects_from_prefix, bos_uri),
            endpoint,
            transform=transform,
            bos_client_config=bos_client_config,
            enable_sharding=enable_sharding,
        )

    def _get_client(self,
                    world_size: Optional[int] = None, 
                    rank: Optional[int] = None, 
                    num_workers: Optional[int] = None, 
                    worker_id: Optional[int] = None):
        if self._client is None:
            self._client = BosClient(
                endpoint=self.endpoint,
                bos_client_config=self._bos_client_config,
                dataset_type=1,
                world_size=world_size, 
                rank=rank, 
                num_workers=num_workers, 
                worker_id=worker_id,
            )
        return self._client

    def _get_transformed_object(self, bucket_key: BosBucketKeyData) -> Any:
        return self._transform(
            self._get_client().get_object(
                bucket_key.bucket, bucket_key.key, object_info=bucket_key.object_info
            )
        )

    def __iter__(self) -> Iterator[Any]:
        worker_id = 0
        num_workers = 1
        if self._enable_sharding:
            worker_info = torch.utils.data.get_worker_info()
            if worker_info is not None:
                worker_id = worker_info.id
                num_workers = worker_info.num_workers

        if not self._enable_sharding or (self._world_size == 1 and num_workers == 1):
            # sharding disabled or only one shard is available, so return the entire dataset
            return map(
                self._get_transformed_object,
                self._get_dataset_objects(self._get_client()),
            )

        """In a multi-process setting (e.g., distributed training), the dataset needs to be
        sharded across multiple processes. The following variables control this sharding:

        _rank: The rank (index) of the current process within the world (group of processes).
        _world_size: The total number of processes in the world (group).

        In addition, within each process, the dataset may be further sharded across multiple
        worker threads or processes (e.g., for data loading). The following variables control
        this intra-process sharding:

        worker_id: The ID of the current worker thread/process within the process.
        num_workers: The total number of worker threads/processes within the process.
        """

        return map(
            self._get_transformed_object,
            self._get_dataset_objects(self._get_client(self._world_size, self._rank, num_workers, worker_id)),
        )
