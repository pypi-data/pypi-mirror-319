# Common Image Tools

![Latest Stable Version](https://badgen.net/github/release/lanzani/common-image-tools/stable?dummy=8484744)
![PyPI - Downloads](https://badgen.net/pypi/dm/common-image-tools)

[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Coverage Status](/reports/coverage/coverage-badge.svg?dummy=8484744)](./reports/coverage/index.html)
![example workflow](https://github.com/lanzani/common-image-tools/actions/workflows/release.yml/badge.svg)



## Description

common_image_tools is a repository containing a curated collection of commonly used image manipulation functions for
computer vision projects. These tools provide a set of handy functions for performing various image processing tasks,
such as resizing, cropping, filtering, and more.

## Features

- **Resizing**: Easily resize images to desired dimensions.
- **Cropping**: Crop images to focus on specific regions.
- **Filtering**: Apply various filters to enhance or modify images.
- **Conversion**: Convert images between different formats.
- **Visualization**: Tools for visualizing image data.
- **Video Source**: Flexible interface for handling different types of video inputs.

## Installation

To install common_image_tools, run the following command:

```bash
pip install common-image-tools
```

or using poetry:

```bash
poetry add common-image-tools
```

## Usage

### Video Source

The `VideoSource` class provides a flexible interface for handling different types of video inputs with support for various OpenCV backends and hardware acceleration on Jetson devices.

#### Features
- Support for multiple video source types:
  - RTSP streams
  - Video files (MP4)
  - Webcam devices
- Configurable frame dimensions and FPS
- Multiple backend options:
  - OpenCV default
  - GStreamer
  - GStreamer with Jetson hardware acceleration
- Automatic backend selection based on system capabilities

#### Basic Usage

```python
from common_image_tools import VideoSource
import cv2

# Create a video source
source = VideoSource(
    "video.mp4",
    target_frame_height=720,
    target_frame_width=1280,
    target_fps=30
)

# Use with OpenCV
cap = cv2.VideoCapture(source.parsed_source)
```

#### Different Source Types

```python
# RTSP Stream
rtsp_source = VideoSource("rtsp://example.com/stream")

# Video File
file_source = VideoSource("path/to/video.mp4")

# Webcam
webcam_source = VideoSource("/dev/video0")

# Webcam
webcam_source = VideoSource(0)
```

#### Backend Selection

```python
from common_image_tools import VideoSource, OpencvBackendMode

# Auto backend selection (default)
source = VideoSource("video.mp4")

# Force OpenCV default backend
source = VideoSource(
    "video.mp4",
    opencv_backend=OpencvBackendMode.OPENCV_DEFAULT
)

# Force GStreamer backend
source = VideoSource(
    "video.mp4",
    opencv_backend=OpencvBackendMode.OPENCV_GSTREAMER
)

# Use Jetson-optimized GStreamer backend
source = VideoSource(
    "video.mp4",
    opencv_backend=OpencvBackendMode.OPENCV_GSTREAMER_JETSON
)
```

#### API Reference

##### VideoSource

```python
VideoSource(
    source,
    target_frame_height: int = None,
    target_frame_width: int = None,
    target_fps: int = None,
    opencv_backend: OpencvBackendMode = OpencvBackendMode.AUTO
)
```

### Conversion

### Operation

### Tool

### Verification

### Visualization

## Contributing

Contributions are welcome! If you have any suggestions, improvements, or new features to add, please open an issue or
submit a pull request. Make sure to follow the existing coding style and include appropriate tests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
