import cv2
import os
import dlib
import argparse

detector = dlib.get_frontal_face_detector()


def save(img, name, bbox, width=180, height=227):
    x, y, w, h = bbox
    imgCrop = img[y:h, x:w]
    imgCrop = cv2.resize(
        imgCrop, (width, height)
    )  # we need this line to reshape the images
    cv2.imwrite(name + ".jpg", imgCrop)


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


def preview_single(args):
    frame = cv2.imread(args.input)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if frame is None:
        print(f"Failed to load image: {image_path}")
        return

    faces = detector(gray)
    if len(faces) == 0:
        print(f"No faces found in {image_path}")
        return
    print(f"Number of faces detected: {len(faces)}")

    face = biggest_face(faces)
    print(face)

    x1, y1 = face.left(), face.top()
    x2, y2 = face.right(), face.bottom()
    h = y2 - y1
    y1_ = max(0, int(y1 - h * args.up)) if args.up else y1
    y2_ = min(frame.shape[0], int(y2 + h * args.down)) if args.down else y2
    new_h = y2_ - y1_
    new_w = int(new_h * args.ratio)
    x1_ = max(0, int((x1 + x2) / 2 - new_w / 2))
    x2_ = min(frame.shape[1], x1_ + new_w)
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
    frame = cv2.resize(frame, (800, 800))
    cv2.imshow("img", frame)
    cv2.waitKey(0)
    print("done saving")


def main():
    parser = argparse.ArgumentParser(
        description="Detect and crop faces from all images in a folder."
    )
    parser.add_argument(
        "--input",
        help="Path to the input image or directory containing images.",
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
    # parser.add_argument(
    #     "raw_images_dir", help="Path to the directory containing input images."
    # )
    args = parser.parse_args()
    if not args.input:
        print(" ****Please provide an input image or directory using --input ****\n")
        print(parser.print_help())
        return

    if os.path.isdir(args.input):
        print(f"Processing all images in directory: {args.input}")
        # Add code to process all images in the directory
    else:
        preview_single(args)


if __name__ == "__main__":
    main()
