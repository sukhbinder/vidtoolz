from vidtoolz.hookspecs import hookimpl
import argparse
from .ffmpegtools import play_video


@hookimpl
def register_commands(subparser):
    play_parser = subparser.add_parser("play", description="Play a video file")
    play_parser.add_argument("video_file", help="Path to the video file")
    play_parser.add_argument(
        "-s", "--speed", type=float, default=1.0, help="Playback speed"
    )
    play_parser.add_argument(
        "-l", "--loop", type=int, default=0, help="Number of times to loop (0=infinite)"
    )
    play_parser.set_defaults(func=play_video_command)


def play_video_command(args):
    try:
        code, log = play_video(args.video_file, speed=args.speed, loop=args.loop)

        if code != 0:
            print(f"Error playing video. Return code: {code}")
            print("FFplay output:")
            print(log)

    except FileNotFoundError:
        print(f"Error: Video file {args.video_file} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
