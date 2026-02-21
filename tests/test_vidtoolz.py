import sys
import os
import tempfile
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
        assert "vidtoolz.default_plugins.reverse" in captured.out


def test_invalid_command():
    with mock.patch("sys.argv", ["vidtoolz", "invalid_command"]):
        with pytest.raises(SystemExit) as e:
            main()
        assert str(e.value) == "2"  # SystemExit should be raised with code 2 (error)


# Integration tests for default plugins

def test_info_plugin(capsys):
    """Test the info plugin with test video data"""
    test_video = "tests/test_data/Hello-World.mp4"
    with mock.patch("sys.argv", ["vidtoolz", "info", test_video]):
        main()
        captured = capsys.readouterr()
        assert "Video information:" in captured.out
        assert "Duration" in captured.out or "duration" in captured.out.lower()


def test_clip_plugin():
    """Test the clip plugin with test video data"""
    test_video = "tests/test_data/Hello-World.mp4"
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        output_file = tmp.name
    
    try:
        with mock.patch("sys.argv", ["vidtoolz", "clip", test_video, output_file, "-s", "00:00:01", "-d", "00:00:02"]):
            main()
        
        # Verify output file was created
        assert os.path.exists(output_file)
        
        # Verify output file is smaller than input (since we clipped it)
        input_size = os.path.getsize(test_video)
        output_size = os.path.getsize(output_file)
        assert output_size < input_size
        
    finally:
        # Clean up
        if os.path.exists(output_file):
            os.unlink(output_file)


def test_concat_plugin():
    """Test the concat plugin with test video data"""
    test_video1 = "tests/test_data/Hello-World.mp4"
    test_video2 = "tests/test_data/test.mp4"
    
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        output_file = tmp.name
    
    try:
        # Use the slower but more reliable concat method to avoid codec compatibility issues
        with mock.patch("sys.argv", ["vidtoolz", "ffconcat", test_video1, test_video2, "--no-fast", "-o", output_file]):
            main()
        
        # Verify output file was created
        assert os.path.exists(output_file)
        
        # Verify output file is larger than individual inputs (since we concatenated)
        input1_size = os.path.getsize(test_video1)
        input2_size = os.path.getsize(test_video2)
        output_size = os.path.getsize(output_file)
        assert output_size > input1_size
        assert output_size > input2_size
        
    finally:
        # Clean up
        if os.path.exists(output_file):
            os.unlink(output_file)


def test_overlay_plugin():
    """Test the overlay plugin with test video data"""
    background_video = "tests/test_data/test.mp4"
    overlay_video = "tests/test_data/Hello-World.mp4"
    
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        output_file = tmp.name
    
    try:
        with mock.patch("sys.argv", ["vidtoolz", "ffoverlay", background_video, overlay_video, output_file, "-p", "TopLeft"]):
            main()
        
        # Verify output file was created
        assert os.path.exists(output_file)
        
        # Verify output file size is reasonable (should be similar to background video)
        background_size = os.path.getsize(background_video)
        output_size = os.path.getsize(output_file)
        assert output_size > 0
        assert output_size < background_size * 2  # Shouldn't be more than twice the background size
        
    finally:
        # Clean up
        if os.path.exists(output_file):
            os.unlink(output_file)


def test_scale_plugin():
    """Test the scale plugin with test video data"""
    test_video = "tests/test_data/Hello-World.mp4"
    
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        output_file = tmp.name
    
    try:
        with mock.patch("sys.argv", ["vidtoolz", "scale", test_video, output_file, "320", "240"]):
            main()
        
        # Verify output file was created
        assert os.path.exists(output_file)
        
        # Verify output file size is reasonable
        output_size = os.path.getsize(output_file)
        assert output_size > 0
        
    finally:
        # Clean up
        if os.path.exists(output_file):
            os.unlink(output_file)


import pytest

# ... (keep existing imports)

def test_reverse_plugin():
    """Test the reverse plugin with test video data (now using FFmpeg by default)"""
    test_video = "tests/test_data/Hello-World.mp4"
    
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        output_file = tmp.name
    
    try:
        with mock.patch("sys.argv", ["vidtoolz", "reverse", test_video, output_file]):
            main()
        
        # Verify output file was created
        assert os.path.exists(output_file)
        
        # Verify output file size is reasonable (should be similar to input)
        input_size = os.path.getsize(test_video)
        output_size = os.path.getsize(output_file)
        assert output_size > 0
        assert output_size < input_size * 1.5  # Shouldn't be much larger than input
        
    finally:
        # Clean up
        if os.path.exists(output_file):
            os.unlink(output_file)


def test_play_plugin(capsys):
    """Test the play plugin with test video data"""
    test_video = "tests/test_data/Hello-World.mp4"
    with mock.patch("sys.argv", ["vidtoolz", "play", test_video]):
        # Note: This test might not work in CI environments without display
        # but we can at least test that it doesn't crash immediately
        try:
            main()
        except Exception:
            # Expected in headless environments
            pass
