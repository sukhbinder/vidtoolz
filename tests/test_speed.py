import sys
from argparse import Namespace
from unittest import mock
import pytest
from vidtoolz.default_plugins.speed import adjust_speed, register_commands


@pytest.fixture
def mock_video_file_clip():
    with mock.patch("vidtoolz.default_plugins.speed.VideoFileClip") as mock_clip:
        instance = mock_clip.return_value
        instance.duration = 10
        instance.fps = 30
        instance.audio = mock.MagicMock()
        instance.fl_time.return_value = instance
        instance.set_duration.return_value = instance
        instance.set_audio.return_value = instance
        instance.fx.return_value = instance
        yield mock_clip


def test_adjust_speed_half_speed(mock_video_file_clip, capsys):
    args = Namespace(
        input_file="test.mp4",
        output_file="output.mp4",
        speed=0.5,
        keep_audio_intact=False,
    )
    adjust_speed(args)
    captured = capsys.readouterr()
    assert "Video speed adjusted and saved to output.mp4" in captured.out


def test_adjust_speed_double_speed_keep_audio(mock_video_file_clip, capsys):
    args = Namespace(
        input_file="test.mp4",
        output_file="output.mp4",
        speed=2.0,
        keep_audio_intact=True,
    )
    adjust_speed(args)
    captured = capsys.readouterr()
    assert "Video speed adjusted and saved to output.mp4" in captured.out


def test_adjust_speed_invalid_speed(capsys):
    args = Namespace(
        input_file="test.mp4",
        output_file="output.mp4",
        speed=11.0,
        keep_audio_intact=False,
    )
    adjust_speed(args)
    captured = capsys.readouterr()
    assert "Error: Speed must be between 0.1 and 10.0." in captured.out


def test_adjust_speed_file_not_found(mock_video_file_clip, capsys):
    mock_video_file_clip.side_effect = FileNotFoundError
    args = Namespace(
        input_file="nonexistent.mp4",
        output_file="output.mp4",
        speed=0.5,
        keep_audio_intact=False,
    )
    adjust_speed(args)
    captured = capsys.readouterr()
    assert "Error: Input file nonexistent.mp4 not found." in captured.out


def test_adjust_speed_file_in_list_not_found(mock_video_file_clip, capsys):
    with mock.patch("builtins.open", mock.mock_open(read_data="test1.mp4\nnonexistent.mp4")):
        mock_video_file_clip.side_effect = [mock.MagicMock(), FileNotFoundError]
        args = Namespace(
            input_file="list.txt",
            output_file="output.mp4",
            speed=0.5,
            keep_audio_intact=False,
        )
        adjust_speed(args)
        captured = capsys.readouterr()
        assert "Error: Input file nonexistent.mp4 not found." in captured.out


def test_register_commands():
    subparser = mock.MagicMock()
    subparser.add_parser.return_value = mock.MagicMock()
    register_commands(subparser)
    subparser.add_parser.assert_called_once_with(
        "speed", description="Adjust the speed of a video file."
    )
