from vidtoolz.hookspecs import hookimpl
import argparse
import os
from .ffmpegtools import clip_video, convert_to_seconds


@hookimpl
def register_commands(subparser):
    clip_parser = subparser.add_parser("clip", description="Clip a video file")
    clip_parser.add_argument("input_file", help="Path to the input video file")
    clip_parser.add_argument(
        "output_file", nargs="?", help="Path to the output video file (optional)"
    )

    # Time arguments
    clip_parser.add_argument(
        "-s", "--start", help="Start time (seconds or MM:SS or HH:MM:SS)"
    )
    clip_parser.add_argument(
        "-e", "--end", help="End time (seconds or MM:SS or HH:MM:SS)"
    )
    clip_parser.add_argument(
        "-d", "--duration", help="Duration to clip (seconds or MM:SS or HH:MM:SS)"
    )

    clip_parser.set_defaults(func=clip_video_command)


def clip_video_command(args):
    try:
        start = convert_to_seconds(args.start) if args.start else None
        end = convert_to_seconds(args.end) if args.end else None
        duration = convert_to_seconds(args.duration) if args.duration else None

        code, log, output_path = clip_video(
            args.input_file,
            start=start,
            end=end,
            duration=duration,
            output_path=args.output_file,
        )

        if code == 0:
            print(f"Video clipped and saved to {output_path}")
        else:
            print(f"Error clipping video. Return code: {code}")
            print("FFmpeg output:")
            print(log)

    except FileNotFoundError:
        print(f"Error: Input file {args.input_file} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
