from vidtoolz.hookspecs import hookimpl
from moviepy import VideoFileClip, vfx, afx


@hookimpl
def register_commands(subparser):
    reverse_parser = subparser.add_parser("reverse", description="Reverse a video file")
    reverse_parser.add_argument("input_file", help="Path to the input video file")
    reverse_parser.add_argument("output_file", help="Path to the output video file")
    reverse_parser.set_defaults(func=reverse_video)


def reverse_video(args):
    try:
        clip = VideoFileClip(args.input_file)
        new_clip = clip.time_transform(
            lambda t: clip.duration - t, apply_to=["mask", "audio"], keep_duration=True
        )

        new_clip.write_videofile(
            args.output_file, codec="libx264", fps=clip.fps, audio_codec="aac"
        )
        print(f"Video reversed and saved to {args.output_file}")
    except FileNotFoundError:
        print(f"Error: Input file {args.input_file} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
