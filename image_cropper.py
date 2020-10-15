import cv2
from absl import logging
from absl import flags
from absl import app

FLAGS = flags.FLAGS
flags.DEFINE_string("input",r"D:\youtube\youtube video resources\12_deepfake_music2\deepfake\intro_female2_singpart.mov", "input image")
flags.DEFINE_string("output",r"E:\Google Drive\first-order-motion-model\cropped_intro_female2_singpart.avi", "output image")
flags.DEFINE_string("command", "findroi", "findroi or produce image")
flags.DEFINE_integer("width", 300, "default size")
# Preparing Track Bars
# Defining empty function

def outputvideo(x,y, width):
    logging.info(f"writing video file{FLAGS.output} with ({x},{y},{width})")
    out = cv2.VideoWriter(
        FLAGS.output, cv2.VideoWriter_fourcc(*"MJPG"), 30.0,
        (width, width))

    cap = cv2.VideoCapture(FLAGS.input)

    while True:
        ret, frame_read = cap.read()
        if not ret:
            break

        frame_cropped = frame_read[y:y+width,x:x+width]
        frame_resized = cv2.resize(frame_cropped,
                   (width,width), interpolation=cv2.INTER_LINEAR)
        out.write(frame_cropped)

    cap.release()
    out.release()
def do_nothing(x):
    pass

def findroi():
    write_video = False

    # Giving name to the window with Track Bars
    # And specifying that window is resizable
    cv2.namedWindow('Track Bars', cv2.WINDOW_NORMAL)

    cv2.createTrackbar('x', 'Track Bars', 0, 255, do_nothing)
    cv2.createTrackbar('y', 'Track Bars', 0, 255, do_nothing)
    cv2.createTrackbar('width', 'Track Bars', 0, 720, do_nothing)

    #read the first image
    cap = cv2.VideoCapture(FLAGS.input)
    ret, frame_orig = cap.read()

    cv2.setTrackbarMax('x', 'Track Bars', frame_orig.shape[0])
    cv2.setTrackbarMax('y', 'Track Bars', frame_orig.shape[1])
    cv2.setTrackbarPos('width', 'Track Bars', FLAGS.width)

    while True:
        x = cv2.getTrackbarPos('x', 'Track Bars')
        y = cv2.getTrackbarPos('y', 'Track Bars')
        width =cv2.getTrackbarPos('width', 'Track Bars')
        frame_new = frame_orig.copy()

        pt1 = (x, y)
        pt2 = (x + width, y + width)
        cv2.rectangle(frame_new, pt1, pt2, (0, 255, 0), 1)

        cv2.imshow("Output", frame_new)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('w'):
            write_video = True
            break
        elif key == ord('q'):
            write_video = False
            break

    logging.info(f"x: {x}")
    logging.info(f"y: {y}")
    logging.info(f"width: {width}")
    cap.release()

    if write_video:
        outputvideo(int(x),int(y), int(width))

def main(argv):
    findroi()

if __name__ == "__main__":
    app.run(main)
