from dotenv import load_dotenv

from hdr_sdk.models.config import HDRConfig

load_dotenv()


class TestHDRConfig:
    def test_init(self):
        config = HDRConfig()
        assert config.base_url is not None
        assert config.api_key is not None
