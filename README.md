
[![PyPI](https://img.shields.io/pypi/v/vidtoolz.svg)](https://pypi.org/project/vidtoolz/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/vidtoolz?include_prereleases&label=changelog)](https://github.com/sukhbinder/vidtoolz/releases)
[![Tests](https://github.com/sukhbinder/vidtoolz/workflows/Test/badge.svg)](https://github.com/sukhbinder/vidtoolz/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/vidtoolz/blob/main/LICENSE)


# vidtoolz
Make vides using python. A plugin-based CLI toolset for editing, authering videos, built with python.

**Overview**
-----------

vidtoolz is a collection of command-line tools designed to make videos and edit videos easier. The project takes a plugin-based approach, allowing users to extend its functionality by creating custom plugins.

There are few plugins that i am activiley using. I will soon add all of them here.

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


