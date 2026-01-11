
[![PyPI](https://img.shields.io/pypi/v/vidtoolz.svg)](https://pypi.org/project/vidtoolz/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/vidtoolz?include_prereleases&label=changelog)](https://github.com/sukhbinder/vidtoolz/releases)
[![Tests](https://github.com/sukhbinder/vidtoolz/workflows/Test/badge.svg)](https://github.com/sukhbinder/vidtoolz/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/vidtoolz/blob/main/LICENSE)


# vidtoolz
Make videos using python. A plugin-based CLI toolset for editing, authering videos, built with python.

**Overview**
-----------

vidtoolz is a collection of command-line tools designed to make videos and edit videos easier. The project takes a plugin-based approach, allowing users to extend its functionality by creating custom plugins.

After installing ``vidtoolz``, install any of the [following plugins](https://pypi.org/search/?q=vidtoolz).



**VidToolz Plugins**

| Tool | Description | Category |
| --- | --- | --- |
| Reverse | Reverse a video file | Video Effects |
| Zoomtext | Zoom out the video and display text as caption | Video Effects |
| Mchap | Make chapters using a list of videos | Video Effects |
| Lightning | Add lightning effects on video | Video Effects |
| Flicker | Add flicker  effects on video | Video Effects |
| Slideshow | Create slideshow with images using ffmpeg | Video Effects |
| Split | Split a video into two | Video Effects |
| Normalize | Normalize audio of a video | Audio Enhancements |
| Shake | Shake a portion of a video | Special Effects |
| Flip | Flip a vedio vertically or horizontally | Special Effects |
| Denoise | Denoise audio in a video | Audio Enhancements |
| Enhance | Enhance audio of a video using ffmpeg | Audio Enhancements |
| Twitch | Add twitch effect to a video | Video Effects |
| H2R | Tools for hum hai rahi channel | Video Effects |
| Vintage | Create vintage effect on videos using ffmpeg | Video Effects |
| Jitter | Add jitter effect to a video using moviepy | Special Effects |
| Trim | Trim video using ffmpeg | Video Effects |
| Rotate | Rotates a video | Special Effects |
| Metadata | Add metadata to a video for better SEO | Metadata and SEO |
| Stitch | Stitch videos using music | Music Integration |
| Highlights | Make highlights from videos | Video Effects |
| Fade | Add fade in and out for a video using ffmpeg | Video Effects |
| Fadeinout | Apply fadein-fadeout effects on videos | Video Effects |
| Soundeffects | Add sound effects to videos | Audio Enhancements |
| Getframe | Get frame out of a video for thumbnail | Special Effects |
| Chapters | Write formated youtube chapters with text inputs | Video Effects |
| Hue | Add a hue to a video using ffmpeg | Video Effects |
| Echo | Apply noise reduction and echo effect | Audio Enhancements |
| Beats | Get beats from a mp3 song | Music Analysis |
| Greenscreen | Apply greenscreen video on top of a video | Special Effects |
| Shorts | Create shorts from long form videos | Video Effects |
| Freeze | Use moviepy to flash freeze a frame just like imovie | Special Effects |
| Intro | Create intro video from a series of videos | Video Effects |
| Repaudio | Replace audio for a video file | Audio Enhancements |
| Vignette | Apply Vignette on Video | Video Effects |
| Addtext | Add text to a video file | Text and Overlay |
| Volume | Increase decrease volume | Audio Control |
| Addsound | Add sound to a video | Audio Control |
| Loudness | Use EBU R128 Loudness Normalization with ffmpeg | Audio Enhancements |
| Overlay | Add overlay effect on video using ffmpeg | Text and Overlay |
| Textclip | Create a color clip with overlaid text | Text and Overlay |
| Compose | Compose Videos using the supplied compose_vid file | Video Composition |
| Concat | Concat videos using ffmpeg | Video Composition |

To get help, just type ``vidtoolz`` or its shortcut ``vid`` to access the cli.

```bash
vidtoolz --help 
```

or

```bash
vid --help
```
This will show all the plugins installed.

```bash
usage: vid [-h]
           {plugins,install,trim,addtext,chapters,beats,greenscreen,shorts,repaudio,addsound,concat}
           ...

Video Tools for editing videos using python

positional arguments:
 plugins              Get all listed plugins
 install              Install plugins in the same environemnt as vidtoolz
 trim                 Trim video using ffmpeg
 addtext              Add text to a video file
 chapters             Write formated youtube chapters with text inputs
 beats                Get beats from a mp3 song
 greenscreen          Apply greenscreen video on top of a video
 shorts               Create shorts from long form videos
 repaudio             Replace audio for a video file
 addsound             Add sound to a video
 concat               Concat videos using ffmpeg 

optional arguments:
  -h, --help            show this help message and exit

```


To install a plugin, just type 

```bash
vid install vidtoolz-trim
```

![vidtoolz-help](https://raw.githubusercontent.com/sukhbinder/vidtoolz/refs/heads/main/vidtoolz.gif)

**Features**
------------

*   A simple and intuitive CLI interface
*   Extensive plugin support for customizing and extending the toolset
*   Integration with popular Python libraries and frameworks
*   Support for multiple Python versions (>=3.9)

**Requirements**
----------------

*   Python 3.9 or later
*   The `pluggy` library for plugin management

**Installation**
----------------

```bash
pip install vidtoolz
```

## Developing your plugin
------------------------

You'll need to have [cookiecutter](https://cookiecutter.readthedocs.io/) installed.

```bash
pipx install cookiecutter
```

Regular `pip` will work OK too.

## Usage

Run `cookiecutter gh:sukhbinder/vidtoolz-plugin` and then answer the prompts. Here's an example run:

```bash
cookiecutter gh:sukhbinder/vidtoolz-plugin
```

This will show this. Fill this and the template is ready. Just add your code.

```
plugin_name []: vidtoolz plugin template demo
description []: Demonstrating https://github.com/sukhbinder/vidtoolz-plugin
hyphenated [vidtoolz-plugin-template-demo]:
underscored [vidtoolz_plugin_template_demo]:
github_username []: sukhbinder
author_name []: Sukhbinder Singh
```
