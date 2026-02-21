from vidtoolz.hookspecs import hookimpl
import argparse
from .ffmpegtools import scale_video


@hookimpl
def register_commands(subparser):
    scale_parser = subparser.add_parser("scale", description="Scale a video file")
    scale_parser.add_argument("input_file", help="Path to the input video file")
    scale_parser.add_argument("output_file", nargs="?", help="Path to the output video file (optional)")
    scale_parser.add_argument("width", type=int, help="Target width")
    scale_parser.add_argument("height", type=int, nargs="?", default=-2, help="Target height (default: -2 for auto)")
    scale_parser.set_defaults(func=scale_video_command)


def scale_video_command(args):
    try:
        code, log, output_path = scale_video(
            args.input_file,
            args.width,
            args.height,
            output_path=args.output_file
        )
        
        if code == 0:
            print(f"Video scaled and saved to {output_path}")
        else:
            print(f"Error scaling video. Return code: {code}")
            print("FFmpeg output:")
            print(log)
            
    except FileNotFoundError:
        print(f"Error: Input file {args.input_file} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")