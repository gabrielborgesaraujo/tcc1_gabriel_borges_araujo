import os
import json
import matplotlib.pyplot as plt
from PIL import Image
from PIL.ImageStat import Stat
from text_element import TextElement
from img import Image as ObjImage
import wcag_contrast_ratio as contrast
from niveis_wcag import NiveisWCAG as Niv
import time

def get_files_in_dir(dir_path, file_type):
  files = []
  for file in os.listdir(dir_path):
    if file.endswith(file_type):
      files.append(os.path.join(dir_path, file))
  return files

def get_colors_by_position(img, column_min, row_min, column_max, row_max):
    light_color = 0
    dark_color = 0
    image_pil = Image.open(img)
    elemento_recortado = image_pil.crop((column_min, row_min, column_max, row_max))
    stat = Stat(elemento_recortado)
    light_color = ((stat._getextrema()[0][0]), (stat._getextrema()[1][0]), (stat._getextrema()[2][0]))
    dark_color = ((stat._getextrema()[0][1]), (stat._getextrema()[1][1]), (stat._getextrema()[2][1]))

    return light_color, dark_color
    
   

def rgb_to_hex(r, g, b):
    if not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
        raise ValueError("Os valores RGB devem estar no intervalo de 0 a 255.")

    return "#{:02x}{:02x}{:02x}".format(r, g, b)

def main():
    img_dir = get_files_in_dir("data/input", ".jpg")
    json_dir = get_files_in_dir("data/ocr", ".json")
    total_text_elements = 0
    total_imagens_conformes = 0
    total_imagens_nao_conformes = 0
    total_text_elements_conformes = 0
    total_text_elements_nao_conformes = 0
    tempo_inicio = time.time()
    array_of_contrasts = []

    for img in img_dir:
        img_path = img
        imgObj = ObjImage(img_path, None, [], None, None, None)
        with open(json_dir[img_dir.index(img)], "r", encoding="utf8") as f:
            data = json.load(f)
        imgObj.shape = data["img_shape"]
        number_of_texts = data["texts"].__len__()
        number_of_valid_texts = 0
        isImageValid = True
        contraste_medio_por_imagem = 0.0
        for text in data["texts"]:
            colors=get_colors_by_position(img, text["column_min"], text["row_min"], text["column_max"], text["row_max"])
            cor_escura = rgb_to_hex(colors[0][0], colors[0][1], colors[0][2])
            cor_clara = rgb_to_hex(colors[1][0], colors[1][1], colors[1][2])
            colors=((colors[0][0]/255, colors[0][1]/255, colors[0][2]/255), (colors[1][0]/255, colors[1][1]/255, colors[1][2]/255))
            nivel_wcag = Niv(contrast.passes_AA(contrast.rgb(colors[0], colors[1])), contrast.passes_AAA(contrast.rgb(colors[0], colors[1])))
            isValid = contrast.passes_AA(contrast.rgb(colors[0], colors[1])) and contrast.passes_AAA(contrast.rgb(colors[0], colors[1]))
            contraste_medio_por_imagem += contrast.rgb(colors[0], colors[1])
            array_of_contrasts.append(contrast.rgb(colors[0], colors[1]))
            if isValid:
                total_text_elements_conformes += 1
                number_of_valid_texts += 1
            else:
                total_text_elements_nao_conformes += 1
                isImageValid = False
            text_element = TextElement(contrast.rgb(colors[0], colors[1]), cor_clara, cor_escura, nivel_wcag, isValid, (text["column_min"], text["row_min"], text["column_max"], text["row_max"]), text["content"])
            imgObj.text_elements.append(text_element)
            total_text_elements += 1
        imgObj.number_of_texts = number_of_texts
        imgObj.number_of_valid_texts = number_of_valid_texts
        if contraste_medio_por_imagem == 0:
            imgObj.contraste_medio_por_imagem = 0
        else:
            imgObj.contraste_medio_por_imagem = contraste_medio_por_imagem/number_of_texts
        if isImageValid:
            total_imagens_conformes += 1
        else:
            total_imagens_nao_conformes += 1
        with open("data/output/{}".format(img.replace("data/input\\", "").replace(".jpg", ".json")), "w", encoding="utf8") as f:
            json.dump(imgObj.to_dict(), f, indent=4)
    tempo_final = time.time()
    tempo_de_processamento = tempo_final - tempo_inicio
    resultados_totais = {
        "total_text_elements": total_text_elements,
        "total_images": img_dir.__len__(),
        "total_imagens_conformes": total_imagens_conformes,
        "total_imagens_nao_conformes": total_imagens_nao_conformes,
        "total_text_elements_conformes": total_text_elements_conformes,
        "total_text_elements_nao_conformes": total_text_elements_nao_conformes,
        "tempo_de_processamento": (f"A execução levou {tempo_de_processamento:.6f} segundos")
        }
    with open("data/resultados_totais.json", "w", encoding="utf8") as f:
        json.dump(resultados_totais, f, indent=4)
    plt.hist(array_of_contrasts, bins=20, edgecolor='black')
    plt.xlabel('Valores')
    plt.ylabel('Frequência')
    plt.title('Histograma dos Contrastes')
    

if __name__ == "__main__":
  main()
