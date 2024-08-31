from unittest.mock import patch, MagicMock
from applications.core.helpers import EventFileNameGenerator


class TestEventFileNameGenerator:
    @patch("applications.core.helpers.uuid.uuid4", return_value="2137")
    def test_generate_makes_new_filename_from_provided(self, _: MagicMock):
        result = EventFileNameGenerator.generate(None, "example.png")
        assert result == "media/events/2137.png"
