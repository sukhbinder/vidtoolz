import os
import subprocess
import tempfile
from enum import Enum
from typing import List


# ---------------- ENUMS ----------------

class Position(Enum):
    TopLeft = 1
    TopCenter = 2
    TopRight = 3
    RightCenter = 4
    BottomRight = 5
    BottomCenter = 6
    BottomLeft = 7
    LeftCenter = 8
    Center = 9


# ---------------- CORE HELPERS ----------------

def run_command(command: str, timeout: int = 300):
    """Run a shell command and capture stdout/stderr."""
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            shell=True,
            text=True
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Process timed out"


def run_ffmpeg(cmd: str, timeout: int = 300):
    """Execute FFmpeg command."""
    command = f"ffmpeg {cmd}"
    code, out, err = run_command(command, timeout)
    log = f"{command}\n{out}\n{err}"
    return code, log


def run_ffprobe(cmd: str, timeout: int = 60):
    """Execute FFprobe command."""
    command = f"ffprobe {cmd}"
    code, out, err = run_command(command, timeout)
    log = f"{command}\n{out}\n{err}"
    return code, log


def run_ffplay(cmd: str, timeout: int = 60):
    """Execute FFplay command."""
    command = f"ffplay {cmd}"
    code, out, err = run_command(command, timeout)
    log = f"{command}\n{out}\n{err}"
    return code, log


def convert_to_seconds(time_value):
    """Convert seconds / MM:SS / HH:MM:SS → float seconds."""
    if isinstance(time_value, (int, float)):
        return float(time_value)

    parts = [float(p) for p in str(time_value).split(":")]

    if len(parts) == 3:
        h, m, s = parts
        return h * 3600 + m * 60 + s
    elif len(parts) == 2:
        m, s = parts
        return m * 60 + s

    return parts[0]


# ---------------- VIDEO OPERATIONS ----------------

def clip_video(video_path, start=None, end=None, duration=None,
               output_path=None, timeout=60):
    """Clip a video."""
    try:
        if output_path is None:
            base, ext = os.path.splitext(video_path)
            output_path = f"{base}_clip{ext}"

        cmd = ""

        if start is not None:
            cmd += f"-ss {convert_to_seconds(start)} "

        cmd += f"-i \"{video_path}\" "

        if end is None and duration is not None:
            end = convert_to_seconds(start or 0) + convert_to_seconds(duration)

        if end is not None:
            cmd += f"-to {convert_to_seconds(end)} "

        cmd += f"-y \"{output_path}\""

        code, log = run_ffmpeg(cmd, timeout)
        return code, log, output_path

    except Exception as e:
        return -1, str(e), ""


def scale_video(video_path, width, height=-2,
                output_path=None, timeout=120):
    """Scale a video."""
    try:
        if output_path is None:
            base, ext = os.path.splitext(video_path)
            output_path = f"{base}_scaled{ext}"

        cmd = (
            f"-i \"{video_path}\" "
            f"-vf scale={width}:{height} "
            f"-y \"{output_path}\""
        )

        code, log = run_ffmpeg(cmd, timeout)
        return code, log, output_path

    except Exception as e:
        return -1, str(e), ""


def overlay_video(background_video, overlay_video,
                  output_path=None,
                  position=Position.TopLeft,
                  dx=0, dy=0,
                  overlay_scale=None,
                  timeout=180):
    """Overlay one video onto another."""
    try:
        if output_path is None:
            base, ext = os.path.splitext(background_video)
            output_path = f"{base}_overlay{ext}"

        if position == Position.TopLeft:
            x, y = f"{dx}", f"{dy}"
        elif position == Position.TopCenter:
            x, y = f"(W-w)/2+{dx}", f"{dy}"
        elif position == Position.TopRight:
            x, y = f"(W-w)+{dx}", f"{dy}"
        elif position == Position.RightCenter:
            x, y = f"(W-w)+{dx}", f"(H-h)/2+{dy}"
        elif position == Position.BottomRight:
            x, y = f"(W-w)+{dx}", f"(H-h)+{dy}"
        elif position == Position.BottomCenter:
            x, y = f"(W-w)/2+{dx}", f"(H-h)+{dy}"
        elif position == Position.BottomLeft:
            x, y = f"{dx}", f"(H-h)+{dy}"
        elif position == Position.LeftCenter:
            x, y = f"{dx}", f"(H-h)/2+{dy}"
        else:
            x, y = f"(W-w)/2+{dx}", f"(H-h)/2+{dy}"

        filter_parts = []

        if overlay_scale:
            ow, oh = overlay_scale
            filter_parts.append(f"[1:v]scale={ow}:{oh}[ovr]")
            overlay_input = "[ovr]"
        else:
            overlay_input = "[1:v]"

        filter_parts.append(f"[0:v]{overlay_input}overlay={x}:{y}[vout]")
        filter_parts.append(f"[0:a][1:a]amix=inputs=2[aout]")

        filter_complex = ";".join(filter_parts)

        cmd = (
            f"-i \"{background_video}\" -i \"{overlay_video}\" "
            f"-filter_complex \"{filter_complex}\" "
            f"-map \"[vout]\" -map \"[aout]\" "
            f"-y \"{output_path}\""
        )

        code, log = run_ffmpeg(cmd, timeout)
        return code, log, output_path

    except Exception as e:
        return -1, str(e), ""


def concat_videos(input_files: List[str],
                  output_path=None,
                  fast=True,
                  timeout=120):
    """Concatenate videos."""
    try:
        if output_path is None:
            base, _ = os.path.splitext(input_files[0])
            output_path = f"{base}_merged.mp4"

        for file in input_files:
            if not os.path.exists(file):
                raise FileNotFoundError(f"{file} not found")

        if fast:
            with tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8") as f:
                for file in input_files:
                    f.write(f"file '{os.path.abspath(file)}'\n")
                list_path = f.name

            cmd = f"-f concat -safe 0 -i \"{list_path}\" -c copy -y \"{output_path}\""
            code, log = run_ffmpeg(cmd, timeout)

            os.remove(list_path)
            return code, log, output_path

        else:
            inputs = " ".join([f"-i \"{f}\"" for f in input_files])
            filter_str = f"concat=n={len(input_files)}:v=1:a=1[vout][aout]"

            cmd = (
                f"{inputs} "
                f"-filter_complex \"{filter_str}\" "
                f"-map \"[vout]\" -map \"[aout]\" "
                f"-y \"{output_path}\""
            )

            code, log = run_ffmpeg(cmd, timeout)
            return code, log, output_path

    except Exception as e:
        return -1, str(e), ""


# ---------------- INFO / PLAYBACK ----------------

def get_video_info(video_path):
    """Retrieve stream info via FFprobe."""
    cmd = f"-v error -show_streams -of json \"{video_path}\""
    return run_ffprobe(cmd)


def play_video(video_path, speed=1.0, loop=0):
    """Play video using FFplay."""
    speed = float(speed)
    loop = int(loop)

    cmd = f"-loop {loop} "

    if speed != 1:
        cmd += f"-vf setpts={1/speed}*PTS -af atempo={speed} "

    cmd += f"\"{video_path}\""

    return run_ffplay(cmd)

