import csv
import sys
from modelos import ImagemAnotada, Deteccao
from pathlib import Path

# region ########## Methods ######################
# ************************************************
def convertCsvToDict(path, debug_dict = False):
    result_debug_dict = {}
    result_dict = {}

    try:
        file = open(path, mode='r', encoding='utf-8')
    except OSError as error:
        print(f"ERROR: could not read the CSV file at '{path}': {error}")
        sys.exit(1)

    with file:
        reader = csv.DictReader(file)
        for row_number, line in enumerate(reader, start=2): 
            try:
                key = line.pop('imagem')
                class_id = int(line['classe_id'])
                x_min = int(line['x_min'])
                y_min = int(line['y_min'])
                x_max = int(line['x_max'])
                y_max = int(line['y_max'])
            except (KeyError, ValueError, TypeError) as error:
                print(f"ERROR: invalid field on CSV line {row_number}: {line}")
                print(f"Details: {error}")
                sys.exit(1)

            class_number = 'class_1' if class_id == 1 else 'class_0'
            if(key not in result_debug_dict.keys()):
                img_path = Path(__file__).parent.parent / "imagens" / key
                result_debug_dict[key] = {'ImagemAnotada': ImagemAnotada(img_path), 'total_boxes': 0, 'boxes': [], 'class_0': 0, 'class_1': 0}
                result_dict[key] = ImagemAnotada(img_path)

            new_detection = Deteccao(class_id, x_min, y_min, x_max, y_max)
            if not debug_dict:
                result_dict[key].addDetection(new_detection)
            else:
                result_debug_dict[key]['ImagemAnotada'].addDetection(new_detection)
                result_debug_dict[key]['total_boxes'] += 1
                result_debug_dict[key]['boxes'].append(line)
                result_debug_dict[key][class_number] += 1

    if debug_dict:
        return result_debug_dict
    return result_dict


if __name__ == "__main__":
    result_debug_dict = convertCsvToDict("../dados/anotacoes.csv", True)
    for key in result_debug_dict.keys():
        print(f"Image: {key}: Boxes: {result_debug_dict[key]['total_boxes']} | class_0: {result_debug_dict[key]['class_0']} | class_1: {result_debug_dict[key]['class_1']}")
    print(f"Images found: {len(result_debug_dict)}")
    print("*"*53)
    result_dict = convertCsvToDict("../dados/anotacoes.csv")
    print(len(result_dict['cena_01_parque.jpg'].detection_list))
    print(result_dict['cena_01_parque.jpg'].toString())

# endregion
