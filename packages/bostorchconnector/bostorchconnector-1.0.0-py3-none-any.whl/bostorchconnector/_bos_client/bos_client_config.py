from dataclasses import dataclass


@dataclass
class BosClientConfig:
    """A dataclass exposing configurable parameters for the Bos client.

    Args:
    part_size(int): Size (bytes) of file parts that will be uploaded/downloaded.
        Note: for saving checkpoints, the inner client will adjust the part size to meet the service limits.
        (max number of parts per upload is 10,000, minimum upload part size is 5 MiB).
        Part size must have values between 5MiB and 5GiB.
        8MiB by default (may change in future).
    """

    credentials_path: str = "~/.baidubce/credentials"
    log_level: int = 1
    log_path: str = "/tmp/bostorchconnector/sdk.log"
    part_size: int = 8 * 1024 * 1024
    prefect_limit_mb: int = 4 * 1024

