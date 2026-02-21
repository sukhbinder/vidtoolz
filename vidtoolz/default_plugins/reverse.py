from vidtoolz.hookspecs import hookimpl
import argparse
from .ffmpegtools import reverse_video as ffmpeg_reverse_video
from moviepy import VideoFileClip, vfx, afx


@hookimpl
def register_commands(subparser):
    reverse_parser = subparser.add_parser("reverse", description="Reverse a video file")
    reverse_parser.add_argument("input_file", help="Path to the input video file")
    reverse_parser.add_argument("output_file", nargs="?", help="Path to the output video file (optional)")
    reverse_parser.add_argument("--use-moviepy", action="store_true", 
                               help="Use MoviePy instead of FFmpeg (slower but may work better for some files)")
    reverse_parser.set_defaults(func=reverse_video_command)


def reverse_video_command(args):
    try:
        if args.use_moviepy:
            # Use the original MoviePy implementation
            clip = VideoFileClip(args.input_file)
            new_clip = clip.time_transform(
                lambda t: clip.duration - t, apply_to=["mask", "audio"], keep_duration=True
            )

            output_path = args.output_file
            if output_path is None:
                base, ext = os.path.splitext(args.input_file)
                output_path = f"{base}_reversed{ext}"

            new_clip.write_videofile(
                output_path, codec="libx264", fps=clip.fps, audio_codec="aac"
            )
            print(f"Video reversed and saved to {output_path}")
        else:
            # Use the new FFmpeg implementation (default)
            code, log, output_path = ffmpeg_reverse_video(
                args.input_file,
                output_path=args.output_file
            )
            
            if code == 0:
                print(f"Video reversed and saved to {output_path}")
            else:
                print(f"Error reversing video. Return code: {code}")
                print("FFmpeg output:")
                print(log)
                
    except FileNotFoundError:
        print(f"Error: Input file {args.input_file} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
