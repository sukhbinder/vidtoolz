from vidtoolz.hookspecs import hookimpl
import argparse
from .ffmpegtools import get_video_info


@hookimpl
def register_commands(subparser):
    info_parser = subparser.add_parser("info", description="Get video information")
    info_parser.add_argument("video_file", help="Path to the video file")
    info_parser.set_defaults(func=get_video_info_command)


def get_video_info_command(args):
    try:
        code, log = get_video_info(args.video_file)
        
        if code == 0:
            print("Video information:")
            print(log)
        else:
            print(f"Error getting video info. Return code: {code}")
            print("FFprobe output:")
            print(log)
            
    except FileNotFoundError:
        print(f"Error: Video file {args.video_file} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")