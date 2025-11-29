import os
from vidtoolz.hookspecs import hookimpl
from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx


def adjust_speed(args):
    """Adjusts the speed of a video file or a list of video files."""
    if not (0.1 <= args.speed <= 10.0):
        print("Error: Speed must be between 0.1 and 10.0.")
        return

    try:
        input_files = []
        if args.input_file.endswith(".txt"):
            with open(args.input_file, "r") as f:
                input_files = [line.strip() for line in f if line.strip()]
        else:
            input_files = [args.input_file]

        clips = []
        for file in input_files:
            try:
                clips.append(VideoFileClip(file))
            except FileNotFoundError:
                print(f"Error: Input file {file} not found.")
                return

        if not clips:
            print("Error: No valid video files found in the input.")
            return

        final_clip = concatenate_videoclips(clips) if len(clips) > 1 else clips[0]

        if args.keep_audio_intact:
            # Speed up video only and keep original audio
            new_clip = final_clip.fl_time(
                lambda t: args.speed * t, apply_to=["video"]
            ).set_duration(final_clip.duration / args.speed)
            new_clip = new_clip.set_audio(final_clip.audio)
        else:
            # Speed up both video and audio
            new_clip = final_clip.fx(vfx.speedx, args.speed)

        new_clip.write_videofile(
            args.output_file, codec="libx264", fps=final_clip.fps, audio_codec="aac"
        )
        print(f"Video speed adjusted and saved to {args.output_file}")

    except FileNotFoundError:
        print(f"Error: Input file {args.input_file} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


@hookimpl
def register_commands(subparser):
    """
    Registers the 'speed' command and its arguments.
    """
    speed_parser = subparser.add_parser(
        "speed", description="Adjust the speed of a video file."
    )
    speed_parser.add_argument(
        "input_file",
        help="Path to the input video file or a text file containing a list of video files.",
    )
    speed_parser.add_argument("output_file", help="Path to the output video file.")
    speed_parser.add_argument(
        "--speed",
        type=float,
        default=0.5,
        help="Speed factor (e.g., 0.5 for half speed, 2.0 for double speed). Range: 0.1 to 10.0.",
    )
    speed_parser.add_argument(
        "--keep-audio-intact",
        action="store_true",
        help="Keep the audio track at the original speed, padding with silence if necessary.",
    )
    speed_parser.set_defaults(func=adjust_speed)
