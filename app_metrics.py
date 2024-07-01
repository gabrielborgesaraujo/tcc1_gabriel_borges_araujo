import numpy as np
import os
import json
import matplotlib.pyplot as plt
from PIL import Image
from PIL.ImageStat import Stat
from text_element import TextElement
from img import Image as ObjImage
import wcag_contrast_ratio as contrast
from niveis_wcag import NiveisWCAG as Niv
from main import get_files_in_dir
import pandas as pd


class AppMetrics:
    def __init__(self, total_elements, total_valid_elements, contrast_medio, app_aproved, app_name):
        self.total_elements = total_elements
        self.total_valid_elements = total_valid_elements
        self.contrast_medio = contrast_medio
        self.app_aproved = app_aproved
        self.app_name = app_name

    def to_dict(self):
        return {
            "total_elements": self.total_elements,
            "total_valid_elements": self.total_valid_elements,
            "contrast_medio": self.contrast_medio,
            "app_aproved": self.app_aproved,
            "app_name": self.app_name
        
        }

class CategoriaMetrics:
    def __init__(self, nome, qtd_apps_reprovados, total_apps_na_categoria):
        self.nome = nome
        self.qtd_apps_reprovados = qtd_apps_reprovados
        self.total_apps_na_categoria = total_apps_na_categoria

    def to_dict(self):
        return {
            "nome": self.nome,
            "qtd_apps_reprovados": self.qtd_apps_reprovados,
            "total_apps_na_categoria": self.total_apps_na_categoria
        }
    
class TotalMetrics:
    def __init__(self, total_apps, apps_validos, apps_invalidos, apps_with_100_percent, apps_with_75_percent, apps_with_50_percent, apps_with_more_25_percent, apps_with_less_25_percent, apps_sem_tela, telas_sem_texto, categorias):
        self.total_apps = total_apps
        self.apps_validos = apps_validos
        self.apps_invalidos = apps_invalidos
        self.apps_with_100_percent = apps_with_100_percent
        self.apps_with_75_percent = apps_with_75_percent
        self.apps_with_50_percent = apps_with_50_percent
        self.apps_with_more_25_percent = apps_with_more_25_percent
        self.apps_with_less_25_percent = apps_with_less_25_percent
        self.apps_sem_tela = apps_sem_tela
        self.telas_sem_texto = telas_sem_texto
        self.categorias = categorias

    def to_dict(self):
        return {
            "total_apps": self.total_apps,
            "apps_validos": self.apps_validos,
            "apps_invalidos": self.apps_invalidos,
            "apps_with_100_percent": self.apps_with_100_percent,
            "apps_with_75_percent": self.apps_with_75_percent,
            "apps_with_50_percent": self.apps_with_50_percent,
            "apps_with_more_25_percent": self.apps_with_more_25_percent,
            "apps_with_less_25_percent": self.apps_with_less_25_percent,
            "apps_sem_tela": self.apps_sem_tela,
            "telas_sem_texto": self.telas_sem_texto,
            "categorias": [categoria.to_dict() for categoria in self.categorias]
        }


def dict_to_json(dicionario):
    try:
        json_string = json.dumps(dicionario, indent=4, ensure_ascii=True, encoding="utf8")
        return json_string
    except (TypeError, ValueError) as e:
        return str(e)
    
def main():
    apps_dir = get_files_in_dir("data/group", ".json")
    df = pd.read_csv("data/app_details.csv")
    array_to_histogram = []
    apps_validos = 0
    apps_invalidos = 0
    total_apps = apps_dir.__len__()
    apps_with_100_percent = 0
    apps_with_75_percent = 0
    apps_with_50_percent = 0
    apps_with_more_25_percent = 0
    apps_with_less_25_percent = 0
    apps_sem_tela = 0
    telas_sem_texto = 0
    total_per_category = df['Category'].value_counts().to_dict()
    cetegorias = dict(zip(df['Category'].drop_duplicates().tolist(), [0]*df['Category'].nunique() ))
    categoriaMetricList = []
    for app in apps_dir:
        print("Processando app: {}".format(app))
        text_per_app = 0
        valid_text_per_app = 0
        is_app_aproved = True
        contrast_array = []
        percent = 0
        app_category = ""
        with open(app, "r", encoding="utf8") as f:
            data = json.load(f)
            app_category = data["categoria"]
            if data["telas"].__len__() == 0:
                apps_sem_tela += 1
                is_app_aproved = False
                continue
            for tela in data["telas"]:
                with open("data/output/{}.json".format(tela).replace("combined\\", ""), "r", encoding="utf8") as fp:
                    tela_info = json.load(fp)
                    if tela_info["text_elements"].__len__() != 0:
                        text_per_app += tela_info["number_of_texts"]
                        valid_text_per_app += tela_info["number_of_valid_texts"]
                        for text in tela_info["text_elements"]:
                            contrast_array.append(text["razao_contraste"])
                            array_to_histogram.append(text["razao_contraste"])
                    else:
                        telas_sem_texto += 1
                    
        contrast_medio = np.mean(contrast_array)
        if valid_text_per_app == text_per_app and text_per_app != 0: 
            apps_validos += 1
        else:
            apps_invalidos += 1
            is_app_aproved = False
            cetegorias[app_category] += 1
        if text_per_app == 0:
            percent = 0
        else:
            percent = valid_text_per_app / text_per_app
        if percent >= 0.0 and percent < 0.25:
            apps_with_less_25_percent += 1
        elif percent >= 0.25 and percent < 0.5:
            apps_with_more_25_percent += 1
        elif percent >= 0.5 and percent < 0.75:
            apps_with_50_percent += 1
        elif percent >= 0.75 and percent < 1.0:
            apps_with_75_percent += 1
        else:
            apps_with_100_percent += 1
        if contrast_medio is np.nan:
            contrast_medio = 0
        app_metrics = AppMetrics(text_per_app, valid_text_per_app, contrast_medio, is_app_aproved, app.replace("data/group\\", ""))
        with open("data/apps_info/{}".format(app).replace("group\\", "").replace("/data", "/"), "w", encoding="utf8") as f:
            json.dump(app_metrics.__dict__, f, indent=4)
        print("App processado com sucesso!\n")
    
    for key in cetegorias.keys():
        categoriaMetric = CategoriaMetrics(key, cetegorias.get(key), total_per_category.get(key))
        categoriaMetricList.append(categoriaMetric)
    
    print(sum(total_per_category.values()))
    result= TotalMetrics(total_apps, apps_validos, apps_invalidos, apps_with_100_percent, apps_with_75_percent, apps_with_50_percent, apps_with_more_25_percent, apps_with_less_25_percent, apps_sem_tela, telas_sem_texto, categoriaMetricList)
    with open("data/apps_metrics.json", "w", encoding="utf8") as f:
        json.dump(result.to_dict(), f, indent=4)
    plt.figure()
    #array_to_histogram = np.array(array_to_histogram)
    #print(np.histogram(array_to_histogram, bins=10)[0])
    #print(apps_sem_tela)
    plt.hist(array_to_histogram, bins=20, color="blue", edgecolor="black", rwidth=0.85, histtype="bar", align="mid")
    plt.title("Histograma de contraste")
    plt.xlabel("Contraste")
    plt.ylabel("Frequência")
    plt.savefig("data/histograms/histograma_total.png")

if __name__ == "__main__":
  main()