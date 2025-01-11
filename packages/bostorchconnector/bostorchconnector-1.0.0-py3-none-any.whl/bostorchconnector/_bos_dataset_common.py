

from typing import Iterable, Union, Tuple

from ._bos_bucket_iterable import BosBucketIterable
from ._bos_client import BosClient
from . import BosReader
from ._bos_bucket_key_data import BosBucketKeyData

"""
_bos_dataset_common.py
    Collection of common methods for Bos datasets, containing logic for URIs parsing and objects listing. 
"""


def identity(obj: BosReader) -> BosReader:
    return obj


def parse_bos_uri(uri: str) -> Tuple[str, str]:
    if not uri or not uri.startswith("bos://"):
        raise ValueError("Only bos:// URIs are supported")
    uri = uri[len("bos://") :]
    if not uri:
        raise ValueError("Bucket name must be non-empty")
    split = uri.split("/", maxsplit=1)
    if len(split) == 1:
        bucket = split[0]
        prefix = ""
    else:
        bucket, prefix = split
    if not bucket:
        raise ValueError("Bucket name must be non-empty")
    return bucket, prefix


def get_objects_from_uris(
    object_uris: Union[str, Iterable[str]], client: BosClient
) -> Iterable[BosBucketKeyData]:
    if isinstance(object_uris, str):
        object_uris = [object_uris]
    # TODO: We should be consistent with URIs parsing. Revise if we want to do this upfront or lazily.
    bucket_key_pairs = [parse_bos_uri(uri) for uri in object_uris]

    return (BosBucketKeyData(bucket, key) for bucket, key in bucket_key_pairs)


def get_objects_from_prefix(bos_uri: str, client: BosClient) -> Iterable[BosBucketKeyData]:
    bucket, prefix = parse_bos_uri(bos_uri)
    return iter(BosBucketIterable(client, bucket, prefix))
