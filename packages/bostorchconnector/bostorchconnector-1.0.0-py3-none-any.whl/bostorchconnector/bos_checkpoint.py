from typing import Optional

from ._bos_dataset_common import parse_bos_uri
from ._bos_client import BosClient, BosClientConfig
from . import BosReader, BosWriter


class BosCheckpoint:
    """A checkpoint manager for Bos.

    To read a checkpoint from Bos, users need to create an BosReader
    by providing bos_uri of the checkpoint stored in Bos. Similarly, to save a
    checkpoint to Bos, users need to create an BosWriter by providing bos_uri.
    BosReader and BosWriter implements io.BufferedIOBase therefore, they can be passed to
    torch.load, and torch.save.
    """

    def __init__(
        self,
        endpoint: Optional[str] = None,
        bos_client_config: Optional[BosClientConfig] = None,
    ):
        self.endpoint = endpoint
        self._client = BosClient(
            endpoint=endpoint, bos_client_config=bos_client_config
        )

    def reader(self, bos_uri: str) -> BosReader:
        """Creates an BosReader from a given bos_uri.

        Args:
            bos_uri (str): A valid bos_uri. (i.e. bos://<BUCKET>/<KEY>)

        Returns:
            BosReader: a read-only binary stream of the Bos object's contents, specified by the bos_uri.

        Raises:
            BosException: An error occurred accessing Bos.
        """
        bucket, key = parse_bos_uri(bos_uri)
        return self._client.get_object(bucket, key)

    def writer(self, bos_uri: str) -> BosWriter:
        """Creates an BosWriter from a given bos_uri.

        Args:
            bos_uri (str): A valid bos_uri. (i.e. bos://<BUCKET>/<KEY>)

        Returns:
            BosWriter: a write-only binary stream. The content is saved to Bos using the specified bos_uri.

        Raises:
            BosException: An error occurred accessing Bos.
        """
        bucket, key = parse_bos_uri(bos_uri)
        return self._client.put_object(bucket, key)
