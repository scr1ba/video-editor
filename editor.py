import cv2
from pytesseract import pytesseract
from concurrent.futures import ThreadPoolExecutor

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    return thresh1

def process_frame(frame, frame_number):
    preprocessed = preprocess_image(frame)

    data = pytesseract.image_to_data(preprocessed, output_type=pytesseract.Output.DICT)

    # Draw a rectangle around recognized text
    for i in range(len(data['text'])):
        if 'Project' in data['text'][i]:
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imwrite(f'debug/frame_{frame_number}.png', frame)

    return frame

cap = cv2.VideoCapture('input.mov')

fps = cap.get(cv2.CAP_PROP_FPS)
frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, frame_size)

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
    processed_frames = list(executor.map(process_frame, frames, range(len(frames))))

    print('Writing frames to output video...')
    for frame in processed_frames:
        out.write(frame)

print('Video processing completed.')

cap.release()
out.release()
