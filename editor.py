import cv2
from pytesseract import pytesseract

cap = cv2.VideoCapture('input.mov')

fps = cap.get(cv2.CAP_PROP_FPS)
frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, frame_size)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    data = pytesseract.image_to_data(frame, output_type=pytesseract.Output.DICT)

    for i in range(len(data['text'])):
        if 'Project description' in data['text'][i]:
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    out.write(frame)

cap.release()
out.release()
