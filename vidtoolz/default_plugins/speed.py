from vidtoolz.hookspecs import hookimpl
import argparse
from .ffmpegtools import change_video_speed


@hookimpl
def register_commands(subparser):
    speed_parser = subparser.add_parser("speed", description="Change video playback speed")
    speed_parser.add_argument("input_file", help="Path to the input video file")
    speed_parser.add_argument(
        "output_file", nargs="?", help="Path to the output video file (optional)"
    )
    speed_parser.add_argument(
        "speed", type=float, help="Speed factor (e.g., 2.0 for 2x speed, 0.5 for half speed)"
    )
    speed_parser.add_argument(
        "-a",
        "--audio-mode",
        choices=["adjust", "mute", "keep"],
        default="adjust",
        help="Audio handling mode: adjust (default), mute, or keep",
    )
    speed_parser.set_defaults(func=speed_video_command)


def speed_video_command(args):
    try:
        code, log, output_path = change_video_speed(
            args.input_file,
            speed=args.speed,
            audio_mode=args.audio_mode,
            output_path=args.output_file,
        )

        if code == 0:
            print(f"Video speed changed and saved to {output_path}")
        else:
            print(f"Error changing video speed. Return code: {code}")
            print("FFmpeg output:")
            print(log)

    except FileNotFoundError:
        print(f"Error: Input file {args.input_file} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")