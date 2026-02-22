from vidtoolz.hookspecs import hookimpl
import argparse
from .ffmpegtools import overlay_video, Position


@hookimpl
def register_commands(subparser):
    overlay_parser = subparser.add_parser(
        "ffoverlay", description="Overlay one video onto another using FFmpeg"
    )
    overlay_parser.add_argument(
        "background_file", help="Path to the background video file"
    )
    overlay_parser.add_argument("overlay_file", help="Path to the overlay video file")
    overlay_parser.add_argument(
        "output_file", nargs="?", help="Path to the output video file (optional)"
    )

    overlay_parser.add_argument(
        "-p",
        "--position",
        choices=[p.name for p in Position],
        default="TopLeft",
        help="Position of overlay",
    )
    overlay_parser.add_argument(
        "-x", "--dx", type=int, default=0, help="Horizontal offset"
    )
    overlay_parser.add_argument(
        "-y", "--dy", type=int, default=0, help="Vertical offset"
    )
    overlay_parser.add_argument(
        "-s",
        "--overlay-scale",
        nargs=2,
        type=int,
        metavar=("WIDTH", "HEIGHT"),
        help="Scale overlay to specific dimensions (absolute pixels)",
    )
    overlay_parser.add_argument(
        "-n",
        "--normalized-scale",
        nargs=2,
        type=float,
        metavar=("WIDTH_RATIO", "HEIGHT_RATIO"),
        help="Scale overlay as normalized ratio (0-1) of background video dimensions",
    )
    overlay_parser.add_argument(
        "-d",
        "--duration",
        type=float,
        help="Duration in seconds to overlay the video (overlay will be trimmed to this duration)",
    )
    overlay_parser.add_argument(
        "-f",
        "--fade-duration",
        type=float,
        default=0.5,
        help="Fade-out duration in seconds at the end of overlay (default: 0.5)",
    )

    overlay_parser.set_defaults(func=overlay_video_command)


def overlay_video_command(args):
    try:
        position = Position[args.position]
        overlay_scale = tuple(args.overlay_scale) if args.overlay_scale else None
        normalized_scale = (
            tuple(args.normalized_scale) if args.normalized_scale else None
        )

        code, log, output_path = overlay_video(
            args.background_file,
            args.overlay_file,
            output_path=args.output_file,
            position=position,
            dx=args.dx,
            dy=args.dy,
            overlay_scale=overlay_scale,
            normalized_scale=normalized_scale,
            duration=args.duration,
            fade_duration=args.fade_duration,
        )

        if code == 0:
            print(f"Video FFmpeg overlay created and saved to {output_path}")
        else:
            print(f"Error creating FFmpeg overlay. Return code: {code}")
            print("FFmpeg output:")
            print(log)

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
