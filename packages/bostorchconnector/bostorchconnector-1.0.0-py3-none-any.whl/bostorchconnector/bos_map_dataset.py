
from functools import partial
from typing import List, Any, Callable, Iterable, Union, Optional
import logging

import torch.utils.data
#from bostorchconnector.src.bostorchconnector._bos_bucket_key_data import BosBucketKeyData
from bostorchconnector._bos_bucket_key_data import BosBucketKeyData

from ._bos_client import BosClient, BosClientConfig
from . import BosReader

from ._bos_dataset_common import (
    get_objects_from_uris,
    get_objects_from_prefix,
    identity,
)

log = logging.getLogger(__name__)


class BosMapDataset(torch.utils.data.Dataset):
    """A Map-Style dataset created from Bos objects.

    To create an instance of BosMapDataset, you need to use
    `from_prefix` or `from_objects` methods.
    """

    def __init__(
        self,
        get_dataset_objects: Callable[[BosClient], Iterable[BosBucketKeyData]],
        endpoint: Optional[str] = None,
        transform: Callable[[BosReader], Any] = identity,
        bos_client_config: Optional[BosClientConfig] = None,
    ):
        self._get_dataset_objects = get_dataset_objects
        self._transform = transform
        self._endpoint = endpoint
        self._bos_client_config = bos_client_config
        self._client = None
        self._bucket_key_pairs: Optional[List[BosBucketKeyData]] = None

    @property
    def endpoint(self):
        return self._endpoint

    @property
    def _dataset_bucket_key_pairs(self) -> List[BosBucketKeyData]:
        if self._bucket_key_pairs is None:
            self._bucket_key_pairs = list(self._get_dataset_objects(self._get_client()))
        assert self._bucket_key_pairs is not None
        return self._bucket_key_pairs

    @classmethod
    def from_objects(
        cls,
        object_uris: Union[str, Iterable[str]],
        *,
        endpoint: Optional[str] = None,
        transform: Callable[[BosReader], Any] = identity,
        bos_client_config: Optional[BosClientConfig] = None,
    ):
        """Returns an instance of BosMapDataset using the Bos URI(s) provided.

        Args:
          object_uris(str | Iterable[str]): Bos URI of the object(s) desired.
          endpoint(str): Bos endpoint of the Bos bucket where the objects are stored.
          transform: Optional callable which is used to transform an BosReader into the desired type.
          bos_client_config: Optional BosClientConfig with parameters for Bos client.

        Returns:
            BosMapDataset: A Map-Style dataset created from Bos objects.

        Raises:
            BosException: An error occurred accessing Bos.
        """
        log.info(f"Building {cls.__name__} from_objects")
        return cls(
            partial(get_objects_from_uris, object_uris),
            endpoint,
            transform=transform,
            bos_client_config=bos_client_config,
        )

    @classmethod
    def from_prefix(
        cls,
        bos_uri: str,
        *,
        endpoint: Optional[str] = None,
        transform: Callable[[BosReader], Any] = identity,
        bos_client_config: Optional[BosClientConfig] = None,
    ):
        """Returns an instance of BosMapDataset using the Bos URI provided.

        Args:
          bos_uri(str): An Bos URI (prefix) of the object(s) desired. Objects matching the prefix will be included in the returned dataset.
          endpoint(str): Bos endpoint of the Bos bucket where the objects are stored.
          transform: Optional callable which is used to transform an BosReader into the desired type.
          bos_client_config: Optional BosClientConfig with parameters for Bos client.

        Returns:
            BosMapDataset: A Map-Style dataset created from Bos objects.

        Raises:
            BosException: An error occurred accessing Bos.
        """
        log.info(f"Building {cls.__name__} from_prefix {bos_uri=}")
        return cls(
            partial(get_objects_from_prefix, bos_uri),
            endpoint,
            transform=transform,
            bos_client_config=bos_client_config,
        )

    def _get_client(self):
        if self._client is None:
            self._client = BosClient(
                endpoint=self.endpoint,
                bos_client_config=self._bos_client_config,
                dataset_type=0,
            )
        return self._client

    def _get_object(self, i: int) -> BosReader:
        bucket_key = self._dataset_bucket_key_pairs[i]
        return self._get_client().get_object(
            bucket_key.bucket, bucket_key.key, object_info=bucket_key.object_info
        )

    def __getitem__(self, i: int) -> Any:
        return self._transform(self._get_object(i))

    def __len__(self):
        return len(self._dataset_bucket_key_pairs)
