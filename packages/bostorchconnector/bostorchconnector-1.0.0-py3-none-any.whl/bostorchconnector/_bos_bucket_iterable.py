

from functools import partial
from itertools import chain
from typing import Iterator, List

from _bos_client_imp import (
    ObjectInfo,
    ListObjectResult,
    ListObjectStream,
)

from ._bos_bucket_key_data import BosBucketKeyData
from ._bos_client import BosClient


class BosBucketIterable:
    def __init__(self, client: BosClient, bucket: str, prefix: str):
        self._client = client
        self._bucket = bucket
        self._prefix = prefix

    def __iter__(self) -> Iterator[BosBucketKeyData]:
        # This allows us to iterate multiple times by re-creating the `_list_stream`
        return iter(BosBucketIterator(self._client, self._bucket, self._prefix))


class BosBucketIterator:
    def __init__(self, client: BosClient, bucket: str, prefix: str):
        self._client = client
        self._bucket = bucket
        self._list_stream = _PickleableListObjectStream(client, bucket, prefix)

    def __iter__(self) -> Iterator[BosBucketKeyData]:
        return chain.from_iterable(
            map(partial(_extract_list_results, self._bucket), self._list_stream)
        )


class _PickleableListObjectStream:
    def __init__(self, client: BosClient, bucket: str, prefix: str):
        self._client = client
        self._list_stream = iter(client.list_objects(bucket, prefix))

    def __iter__(self):
        return self

    def __next__(self) -> ListObjectResult:
        return next(self._list_stream)

    def __getstate__(self):
        return {
            "client": self._client,
            "bucket": self._list_stream.bucket,
            "prefix": self._list_stream.prefix,
            "delimiter": self._list_stream.delimiter,
            "max_keys": self._list_stream.max_keys,
            "continuation_token": self._list_stream.continuation_token,
            "complete": self._list_stream.complete,
        }

    def __setstate__(self, state):
        self._client = state["client"]
        self._list_stream = ListObjectStream._from_state(**state)


def _extract_list_results(
    bucket: str, list_result: ListObjectResult
) -> Iterator[BosBucketKeyData]:
    return map(partial(_extract_object_info, bucket), list_result.object_info)


def _extract_object_info(bucket: str, object_info: ObjectInfo) -> BosBucketKeyData:
    return BosBucketKeyData(bucket=bucket, key=object_info.key, object_info=object_info)
