from vidtoolz.hookspecs import hookimpl
import argparse
from .ffmpegtools import concat_videos


@hookimpl
def register_commands(subparser):
    concat_parser = subparser.add_parser("ffconcat", description="Concatenate video files using FFmpeg")
    concat_parser.add_argument("input_files", nargs="+", help="Path to input video files")
    concat_parser.add_argument("-o", "--output", help="Path to the output video file (optional)")
    concat_parser.add_argument("-f", "--no-fast", action="store_false", dest="fast", 
                               help="Use slower but more compatible concatenation method")
    concat_parser.set_defaults(func=concat_video_command)


def concat_video_command(args):
    try:
        code, log, output_path = concat_videos(
            args.input_files,
            output_path=args.output,
            fast=args.fast
        )
        
        if code == 0:
            print(f"Videos FFmpeg concatenated and saved to {output_path}")
        else:
            print(f"Error FFmpeg concatenating videos. Return code: {code}")
            print("FFmpeg output:")
            print(log)
            
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")