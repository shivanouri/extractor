import cv2

from extractor import Location
from extractor.exceptions import InvalidCropSizeException


def remove_close_lines(lines, thresh=30):
    lines.sort(key=lambda x: x[0])
    return [lines[i] for i in range(len(lines)) if abs(lines[i][0] - lines[i-1][0]) > thresh]


def separate_by_histogram(image, dimension, thresh=30, margin=0):
    hist = cv2.reduce(src=image, dim=dimension, rtype=cv2.REDUCE_AVG)\
        .reshape(-1)

    lines, start = list(), None
    if hist[0] > thresh:
        start = 0
    for idx in range(len(hist)-1):
        if hist[idx] <= thresh < hist[idx+1]:
            start = idx

        elif hist[idx] >= thresh > hist[idx+1] and start is not None:
            lines.append([max(0, start-margin), min(idx+margin, len(hist))])

    if start is not None and hist[-1] > thresh:
        lines.append([max(0, start - margin), len(hist)])
    return lines


def detect_lines(image, dimension, ratio=0.3):
    h, w = image.shape[:2]
    grayed_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    grayed_image = cv2.bitwise_not(grayed_image)
    threshed_image = cv2.adaptiveThreshold(
        grayed_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY, 15, -2
    )

    kernel = (round(ratio * w), 1) if dimension else (1, round(ratio * h))
    opening = cv2.morphologyEx(
        threshed_image, cv2.MORPH_OPEN,
        cv2.getStructuringElement(cv2.MORPH_RECT, kernel)
    )
    lines = separate_by_histogram(opening, dimension=dimension, thresh=40)
    midpoints = [[(line[0] + line[1])//2, line[1] - line[0]] for line in lines]

    return midpoints


def detect_horizontal_lines(image, ratio: float):
    return detect_lines(image, dimension=1, ratio=ratio)


def detect_vertical_lines(image, ratio: float):
    return detect_lines(image, dimension=0, ratio=ratio)


def segment_by_horizontal_lines(
        image,
        lines,
        margin=10,
        x_offset=0,
        y_offset=0,
        first=False,
        last=False
):

    h, w = image.shape[:2]
    segments = list()
    if len(lines) == 0:
        segments.append((x_offset, y_offset, w, h + margin))
        return segments

    if first:
        segments.append(
            (x_offset, y_offset, w, lines[0][0] + margin)
        )
    for i in range(len(lines) - 1):
        segments.append(
            (
                x_offset,
                lines[i][0] - margin + y_offset,
                w,
                (lines[i + 1][0] - lines[i][0]) + 2 * margin
            )
        )
    if last:
        segments.append(
            Location(
                x_offset,
                lines[-1][0] - margin + y_offset,
                w,
                (h - lines[-1][0]) + margin
            )
        )
    return segments


def segment_by_vertical_lines(
        image,
        lines,
        margin=10,
        x_offset=0,
        y_offset=0,
        first=False,
        last=False
):
    h, w = image.shape[:2]
    segments = list()
    if first:
        segments.append(
            (x_offset, y_offset, lines[0][0] + margin, h)
        )
    for i in range(len(lines) - 1):
        segments.append(
            (
                lines[i][0] - margin + x_offset, y_offset,
                (lines[i + 1][0] - lines[i][0]) + 2 * margin, h
            )
        )
    if last:
        segments.append(
            Location(
                lines[-1][0] - margin + x_offset, y_offset,
                (w - lines[-1][0]) + margin, h
            )
        )
    return segments


def line_array_detection(
        image, direction, threshold=50, margin=10, kernel_matrix=(30, 10)
):
    gray_image = image if len(image.shape) < 3 else cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    __, threshed_image = cv2.threshold(
        gray_image, 127, 255, cv2.THRESH_BINARY_INV
    )
    morphology_image = cv2.morphologyEx(
        threshed_image, cv2.MORPH_CLOSE,
        cv2.getStructuringElement(
            cv2.MORPH_RECT, kernel_matrix
        )
    )

    return separate_by_histogram(
        morphology_image, direction, threshold, margin
    )


def row_detection(image, threshold=50, margin=10, kernel_matrix=(30, 10)):
    return line_array_detection(
        image,
        direction=1,
        threshold=threshold,
        margin=margin,
        kernel_matrix=kernel_matrix
    )


def column_detection(image, threshold=70, margin=50, kernel_matrix=(30, 10)):
    return line_array_detection(
        image,
        direction=0,
        threshold=threshold,
        margin=margin,
        kernel_matrix=kernel_matrix
    )


def crop(image, location: Location=None):
    if location:
        h, w = image.shape[:2]
        if location.x > w or location.y > h:
            raise InvalidCropSizeException
        return image[
               location.y:location.y+location.h,
               location.x:location.x+location.w
               ]
