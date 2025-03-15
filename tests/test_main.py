from unittest.mock import MagicMock, patch
from application.listener import Listener
from database.connector import Database
from main import main


def mock_run(token: str, **_):
    assert token


def mock_migrate():
    pass


@patch("main.create_monitor_daemon", MagicMock())
@patch.dict("os.environ", {"TOKEN": "fake_token"})
@patch.object(Database, "migrate_all")
@patch.object(Listener, "run")
def test_main_execution(mock_run_listener: MagicMock, mock_db: MagicMock):
    mock_db.side_effect = mock_migrate
    mock_run_listener.side_effect = mock_run
    main()
    mock_run_listener.assert_called_once()
    mock_db.assert_called_once()
