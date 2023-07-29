# Video Text Highlighter with Fade Transitions

This command-line utility reads a video file, uses OCR (Optical Character Recognition) to recognize specified text, and highlights the recognized text with a colored box. It also applies fade-in and fade-out transitions at the start and end of the video, respectively.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for fiddling purposes.

## Prerequisites
- Python 3.6 or later
- Tesseract (pytesseract)
- OpenCV (opencv-python)

## Installing

These instructions would clone the repository to your local machine, set up a virtual space for python dependencies and install the required ones specified in requirements.tx

````
git clone https://github.com/yourusername/videotexthighlighter.git
cd videotexthighlighter
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
````

## Usage

Run the script with the desired parameters:

````
python script.py --input input.mov --output output.mp4 --text hello --margin 10 --color 0 255 0 --fade_duration 2.0
````

### Parameters
````
--input: Path to the input video file (required)
--output: Path to the output video file (required)
--text: Text to recognize (required)
--margin: Margin around the text (default: 10)
--color: Box color in BGR format (default: [0, 0, 255])
--fade_duration: Fade duration in seconds (default: 2.0)
````