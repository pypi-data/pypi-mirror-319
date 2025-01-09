import pytest

from hdr_sdk.client import HDR
from hdr_sdk.models.config import HDRConfig


@pytest.fixture
def config() -> HDRConfig:
    return HDRConfig()


@pytest.fixture
def hdr(config: HDRConfig) -> HDR:
    return HDR(config)


class TestHDR:
    def test_computer(self, hdr: HDR):
        computer = hdr.computer()
        assert computer is not None
        assert computer._ws is not None
