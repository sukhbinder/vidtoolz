import sys
from unittest import mock
import pytest
from vidtoolz.cli import main


def test_show_help(capsys):
    with mock.patch("sys.argv", ["vidtoolz"]):
        with mock.patch("vidtoolz.plugins.load_plugins", []):
            main()
            captured = capsys.readouterr()
            assert "usage: vidtoolz [-h]" in captured.out


def test_plugins(capsys):
    with mock.patch("sys.argv", ["vidtoolz", "plugins"]):
        main()
        captured = capsys.readouterr()
        assert "No external plugins in env." in captured.out


def test_invalid_command():
    with mock.patch("sys.argv", ["vidtoolz", "invalid_command"]):
        with pytest.raises(SystemExit) as e:
            main()
        assert str(e.value) == "2"  # SystemExit should be raised with code 2 (error)
