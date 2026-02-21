import os
import sys
import subprocess

# Ensure FFmpeg is available, either from system or via static-ffmpeg
def ensure_ffmpeg_available():
    """
    Ensure FFmpeg is available by checking if it's in the system path,
    and if not, use static-ffmpeg as a fallback.
    """
    try:
        # Check if ffmpeg is already available in the system
        subprocess.run(["ffmpeg", "-version"], 
                      stdout=subprocess.DEVNULL, 
                      stderr=subprocess.DEVNULL,
                      check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            # Try to use static-ffmpeg as fallback
            import static_ffmpeg
            static_ffmpeg.add_paths()
            
            # Verify it worked
            subprocess.run(["ffmpeg", "-version"], 
                          stdout=subprocess.DEVNULL, 
                          stderr=subprocess.DEVNULL,
                          check=True)
            return True
        except Exception as e:
            sys.exit(f"Error: FFmpeg is not available and static-ffmpeg fallback failed: {e}")


def determine_output_path(input_file, output_file, suffix):
    input_dir, input_filename = os.path.split(input_file)
    name, _ = os.path.splitext(input_filename)

    if output_file:
        output_dir, output_filename = os.path.split(output_file)
        if not output_dir:  # If no directory is specified, use input file's directory
            return os.path.join(input_dir, output_filename)
        return output_file
    else:
        return os.path.join(input_dir, f"{name}_{suffix}.mp4")


def write_clip(video_with_text, output_video_path, fps):
    try:
        # Write the result to a file
        video_with_text.write_videofile(
            output_video_path,
            codec="libx264",
            fps=fps,
            audio_codec="aac",
            temp_audiofile="temp_audio.m4a",
            remove_temp=True,
        )
    except Exception as e:
        sys.exit("Error writing video file: " + str(e))
    video_with_text.close()
