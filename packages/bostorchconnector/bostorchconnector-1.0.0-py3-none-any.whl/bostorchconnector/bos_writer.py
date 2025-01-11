import io
from typing import Union

from _bos_client_imp import PutObjectStream


class BosWriter(io.BufferedIOBase):
    """A write-only, file like representation of a single object stored in bos."""

    def __init__(self, stream: PutObjectStream):
        self.stream = stream
        self._position = 0

    def __enter__(self):
        self._position = 0
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def write(
        self,
        # Ignoring the type for this as we don't currently support the Buffer protocol
        data: Union[bytes, memoryview],  # type: ignore
    ) -> int:
        """Write bytes to BOS Object specified by bucket and key

        Args:
            data (bytes | memoryview): bytes to write

        Returns:
            int: Number of bytes written

        Raises:
            BosException: An error occurred accessing BOS.
        """
        if isinstance(data, memoryview):
            data = data.tobytes()
        self.stream.write(data)
        self._position += len(data)
        return len(data)

    def close(self):
        """Close write-stream to BOS. Ensures all bytes are written successfully.

        Raises:
            BosException: An error occurred accessing BOS.
        """
        self.stream.close()

    def flush(self):
        """No-op"""
        pass

    def readable(self) -> bool:
        """
        Returns:
            bool: Return whether object was opened for reading.
        """
        return False

    def writable(self) -> bool:
        """
        Returns:
            bool: Return whether object was opened for writing.
        """
        return True

    def tell(self) -> int:
        """
        Returns:
              int: Current stream position.
        """
        return self._position
