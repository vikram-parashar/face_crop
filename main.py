import cv2
import shutil
from datetime import datetime
import os
import dlib
import argparse

detector = dlib.get_frontal_face_detector()

logfile = open("log.txt", "a")


def biggest_face(faces):
    biggest_at = -1
    mx = 0
    for id, face in enumerate(faces):
        x1, y1 = face.left(), face.top()
        x2, y2 = face.right(), face.bottom()
        h, w = y2 - y1, x2 - x1

        if h * w > mx:
            mx = h * w
            biggest_at = id
    return faces[biggest_at]


def detect_and_crop(args, input_img, out_dir):
    frame = cv2.imread(input_img)
    if frame is None:
        # copy failed image to failed folder
        shutil.copy(input_img, out_dir + "/failed/")

        # log to console and log file
        print(f"Failed to load image: {input_img}")
        logfile.write(f"Failed to load image: {input_img}\n")

        return

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    if len(faces) == 0:
        # copy failed image to failed folder
        shutil.copy(input_img, out_dir + "/failed/")

        # log to console and log file
        print(f"No faces found in {input_img}")
        logfile.write(f"No faces found in {input_img}\n")

        return
    # print(f"{len(faces)} face(s) in {input_img}")

    face = biggest_face(faces)

    x1, y1 = face.left(), face.top()
    x2, y2 = face.right(), face.bottom()
    h = y2 - y1
    y1_ = max(0, int(y1 - h * args.up)) if args.up else y1
    y2_ = min(frame.shape[0], int(y2 + h * args.down)) if args.down else y2
    new_h = y2_ - y1_
    new_w = int(new_h * args.ratio)
    x1_ = max(0, int((x1 + x2) / 2 - new_w / 2))
    x2_ = min(frame.shape[1], x1_ + new_w)
    if args.action == "draw":
        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (220, 55, 20),
            1,
        )
        cv2.rectangle(
            frame,
            (x1_, y1_),
            (x2_, y2_),
            (20, 255, 20),
            1,
        )
        cv2.imshow("img", frame)
        cv2.waitKey(0)
    elif args.action == "crop":
        imgCrop = frame[y1_:y2_, x1_:x2_]
        file_name = input_img.split("/")[-1]
        cv2.imwrite(f"{out_dir}/{file_name}", imgCrop)
    else:
        print("wrong argument to action use draw or crop")


def main():
    parser = argparse.ArgumentParser(
        description="Detect and crop faces from all images in a folder."
    )
    parser.add_argument(
        "--input",
        help="Path to the input directory containing images.",
    )
    parser.add_argument(
        "--up",
        type=float,
        help="move bounding box up (in fraction of box height)",
    )
    parser.add_argument(
        "--down",
        type=float,
        help="move bounding box down (in fraction of box height)",
    )
    parser.add_argument(
        "--ratio",
        type=float,
        default=1,
        help="Adjust the crop height by this ratio (default: 1)",
    )
    parser.add_argument(
        "--out", type=str, help="Output folder, default is same as input one"
    )
    parser.add_argument(
        "--action",
        default="draw",
        type=str,
        help="crop or draw",
    )
    args = parser.parse_args()
    if not args.input:
        print(" ****Please provide an input image or directory using --input ****\n")
        print(parser.print_help())
        return

    if os.path.isdir(args.input):
        out_dir = (
            args.out
            if args.out is not None
            else "/".join(args.input.split("/")[:-1]) + "/out"
        )
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        failed_dir = out_dir + "/failed"
        if not os.path.exists(failed_dir):
            os.makedirs(failed_dir)

        total_img = len(os.listdir(args.input))
        for id, img in enumerate(os.listdir(args.input)):
            print(f"@[{id+1}/{total_img}]")
            input_img = os.path.join(args.input, img)
            detect_and_crop(args, input_img, out_dir)

        print("Done")
        print(f"Output images are saved in {out_dir}")
        print(f"Failed images are saved in {failed_dir}")
        print("Log file is saved in log.txt")

    else:
        print("input not a directory")


if __name__ == "__main__":
    with open("log.txt", "w") as lf:
        lf.write(f"-----ran @ {datetime.now()}-----\n")
    main()
    logfile.close()
