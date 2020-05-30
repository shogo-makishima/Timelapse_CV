from cv2 import VideoWriter_fourcc, CAP_PROP_FPS, VideoCapture, cvtColor, COLOR_BGR2GRAY, imwrite, VideoWriter, imread
import threading, time, os, argparse


parser = argparse.ArgumentParser(description="Timelapse video. Example: python3 main.py <capture_index> <x> <y> <count> <pause>")
parser.add_argument("--capture_index", "-ci", default=0, type=int, help="Capture index for get image from WebCam.")
parser.add_argument("--x_size", "-x", default=640, type=int, help="Resolution video: X.")
parser.add_argument("--y_size", "-y", default=320, type=int, help="Resolution video: Y.")
parser.add_argument("--count", "-c", default=10, type=int, help="Count of images.")
parser.add_argument("--pause", "-p", default=1, type=int, help="Pause between frames in seconds")

args = parser.parse_args()

CAPTURE_INDEX, RESOLUTION, COUNT, PAUSE = args.capture_index, (args.x_size, args.y_size), args.count, args.pause

"""
RESOLUTION: tuple = (640, 480)
PAUSE: int = 2  # seconds
COUNT: int = 2
CAPTURE_INDEX: int = 0
"""

class Main:
    def __init__(self):
        print("INITIALIZATION")
        self.capture: VideoCapture = VideoCapture(CAPTURE_INDEX)
        self.capture.set(3, RESOLUTION[0])
        self.capture.set(4, RESOLUTION[1])

        self.writer: VideoWriter = VideoWriter(f"Video\\{self.GetNextNameOfVideo()}.avi", VideoWriter_fourcc("M", "J", "P", "G"), 10, RESOLUTION)
        print("START")

    def GetNextNameOfVideo(self):
        video = list(filter(lambda x: x.endswith("avi") and x[:len(x)- 4].isdigit(), os.listdir(f"{os.curdir}\\Video\\")))
        if (len(video) != 0): next_name = max(list(map(int, [x[:len(x)- 4] for x in video]))) + 1
        else: next_name = 0
        return next_name

    def SaveImage(self, index: int):
        _, image = self.capture.read()
        print(f"IMAGE -> 'Images\\{index}.png'")
        imwrite(f"Images\\{index}.png", image)

    def WriteImagesToVideo(self, index: int):
        print(f"WRITER <- 'Images\\{index}.png'")
        image = imread(f"Images\\{index}.png")
        self.writer.write(image)

    def Close(self):
        self.capture.release()
        self.writer.release()


main = Main()

for i in range(COUNT):
    main.SaveImage(i)
    if (i < COUNT - 1):
        print(f"PAUSE -> {PAUSE} sec")
        time.sleep(PAUSE)

for i in range(COUNT):
    main.WriteImagesToVideo(i)

main.Close()
