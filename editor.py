import cv2
from pytesseract import pytesseract
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import argparse

def preprocess_image(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    return thresh1

def process_frame(args, frame, frame_number):
    preprocessed = preprocess_image(frame)

    # Use OCR to recognize text in the frame
    data = pytesseract.image_to_data(preprocessed, output_type=pytesseract.Output.DICT)

    # Draw a rectangle around recognized text
    for i in range(len(data['text'])):
        if args.text in data['text'][i]:
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            # Add a margin to the rectangle
            cv2.rectangle(frame, (x - args.margin, y - args.margin), (x + w + args.margin, y + h + args.margin), args.color, 2)
            # Save the frame as an image file for debugging
            cv2.imwrite(f'debug/frame_{frame_number}.png', frame)

    return frame

def process_video(args):
    cap = cv2.VideoCapture(args.input)

    # Get the frames per second (fps) and frame size of the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    # Calculate the number of frames to fade in and out
    fade_frames = int(fps * args.fade_duration)

    # Initialize a VideoWriter object to save the output video
    out = cv2.VideoWriter(args.output, cv2.VideoWriter_fourcc(*'mp4v'), fps, frame_size)

    print('Starting video processing...')

    # Process each frame
    with ThreadPoolExecutor() as executor:
        frames = []
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)

        print('Frames captured, starting OCR and draw operations...')
        processed_frames = list(executor.map(process_frame, [args]*len(frames), frames, range(len(frames))))

        print('Applying fade in and fade out transitions...')
        for i, frame in enumerate(processed_frames):
            # Apply fade-in at the start of the video
            if i < fade_frames:
                alpha = i / fade_frames
                frame = cv2.convertScaleAbs(frame, alpha=alpha)
            # Apply fade-out at the end of the video
            elif i > len(frames) - fade_frames:
                alpha = (len(frames) - i) / fade_frames
                frame = cv2.convertScaleAbs(frame, alpha=alpha)

            out.write(frame)

    print('Video processing completed.')

    cap.release()
    out.release()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Edit a video by recognizing a given text and applying a box and fade transitions.')
    parser.add_argument('--input', type=str, required=True, help='Input video file')
    parser.add_argument('--output', type=str, required=True, help='Output video file')
    parser.add_argument('--text', type=str, required=True, help='Text to recognize')
    parser.add_argument('--margin', type=int, default=10, help='Margin around the text (default: 10)')
    parser.add_argument('--color', type=int, nargs=3, default=[0, 0, 255], help='Box color in BGR format (default: [0, 0, 255])')
    parser.add_argument('--fade_duration', type=float, default=2.0, help='Fade duration in seconds (default: 2.0)')

    args = parser.parse_args()

    process_video(args)
