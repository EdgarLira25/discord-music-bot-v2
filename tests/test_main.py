from unittest.mock import MagicMock, patch
from application.listener import Listener
from main import main


def mock_run(token: str):
    assert token


@patch.dict("os.environ", {"TOKEN": "fake_token"})
@patch.object(Listener, "run")
def test_main_execution(mock_run_listener: MagicMock):
    mock_run_listener.side_effect = mock_run
    main()
    mock_run_listener.assert_called_once()
