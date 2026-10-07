import sys
from pathlib import Path
import cv2 as cv

from arquivos import convertCsvToDict
from modelos import COLOR
from modelos import ImagemAnotada, Deteccao

# region ########## Methods ######################
# ************************************************
def check_detections(img_data: ImagemAnotada, height: int, width: int):
    for data in img_data.detection_list:
        if not (0 <= data.x_min < data.x_max < width):
            print(f"Image Path: {img_data.img_path}")
            print(f"Original Height: {height} | Original Width: {width}")
            print(f"DETECTION FAILED --- WIDTH ERROR: class_id={data.class_id} "
                  f"x_min={data.x_min} x_max={data.x_max}")
            sys.exit(1)
        if not (0 <= data.y_min < data.y_max < height):
            print(f"Image Path: {img_data.img_path}")
            print(f"Original Height: {height} | Original Width: {width}")
            print(f"DETECTION FAILED --- HEIGHT ERROR: class_id={data.class_id} "
                  f"y_min={data.y_min} y_max={data.y_max}")
            sys.exit(1)


def resize_for_display(image, max_width=1280, max_height=720):
    height, width = image.shape[:2]

    if width <= max_width and height <= max_height:
        return image

    factor = min(max_width / width, max_height / height)
    new_width = int(width * factor)
    new_height = int(height * factor)

    return cv.resize(image, (new_width, new_height), interpolation=cv.INTER_AREA)


def draw_legend(image, image_name):
    cv.putText(image, image_name, (10, 25),
               cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv.LINE_AA)

    y = 55
    for class_id, color in COLOR.items():
        text = f"class {class_id}"
        cv.putText(image, text, (10, y),
                   cv.FONT_HERSHEY_SIMPLEX, 0.6, color, 2, cv.LINE_AA)
        y += 25


def main():
    root = Path(__file__).parent.parent
    csv_path = root / "dados" / "anotacoes.csv"
    results_folder = root / "resultados"
    results_folder.mkdir(exist_ok=True)

    images_dict = convertCsvToDict(str(csv_path))
    sorted_names = sorted(images_dict.keys())

    for name in sorted_names:
        annotated_image = images_dict[name]

        original = cv.imread(str(annotated_image.img_path))
        if original is None:
            print(f"ERROR: could not read image {annotated_image.img_path}")
            sys.exit(1)

        height, width = original.shape[:2]
        check_detections(annotated_image, height, width)

        annotated_copy = annotated_image.imageProcessing(original)

        print(f"Image: {name} | Boxes drawn: {len(annotated_image.detection_list)}")

        output_path = results_folder / name
        cv.imwrite(str(output_path), annotated_copy)

        display_copy = resize_for_display(annotated_copy.copy())
        draw_legend(display_copy, name)

        while True:
            cv.imshow("Annotation Viewer", display_copy)
            key = cv.waitKey(0) & 0xFF

            if key == ord(' '):
                break
            elif key == ord('q'):
                cv.destroyAllWindows()
                return

    cv.destroyAllWindows()
# endregion --------------------------------------------------

if __name__ == "__main__":
    main()
