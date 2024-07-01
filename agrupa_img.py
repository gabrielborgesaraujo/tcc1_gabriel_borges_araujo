import json
import os
import pandas as pd
from multiprocessing import Pool

df = pd.read_csv("data/app_details.csv")



class App:
    def __init__(self, nome, categoria, telas):
        self.nome = nome
        self.categoria = categoria
        self.telas = telas
    def __str__(self):
        return f'App: {self.nome}, Categoria: {self.categoria}, Telas: {self.telas}'
    
    def to_dict(self):
        return {
            'nome': self.nome,
            'categoria': self.categoria,
            'telas': self.telas
        }
        
def get_files_in_dir(dir_path, file_type):
  files = []
  for file in os.listdir(dir_path):
    if file.endswith(file_type):
      files.append(os.path.join(dir_path, file))
  return files

def find_all_imgs_from_app(app_name):
  img_json_files = get_files_in_dir('combined', '.json')
  images = []
  imgs_alredy_added = get_files_in_dir('data/group', '.json')
  if f'{app_name}.json' in imgs_alredy_added:
     with open(f'data/group/{app_name}.json', 'r', encoding='utf8') as arquivo:
        print(f'{app_name} já processado!')
        images = json.load(arquivo)['telas']
  for img_json in img_json_files:
      with open(img_json, 'r', encoding="utf8") as arquivo:
          app = json.load(arquivo)
          nome_do_app = app['activity_name'].split('/')[0]
          if nome_do_app.lower() == app_name.lower():
              images.append(img_json.split('/')[0].replace('.json', ''))
  images = list(set(images))
  app_info = App(app_name, df.loc[df['App Package Name'] == app_name]['Category'].values[0], images)
  return app_info

def processa_array(apps):
   print("Processando array...")
   print("Tamanho do array: ", len(apps))
   for app in apps:
       print(f'Processando {app}...')
       app_info = find_all_imgs_from_app(app)
       with open(f'data/group/{app_info.nome}.json', 'w', encoding='utf8') as arquivo:
           json.dump(app_info.to_dict(), arquivo, ensure_ascii=False, indent=4)
           print(f'{app_info.nome} processado com sucesso!')
  
def main():
    #apps = []
    #json_dir = get_files_in_dir('combined', '.json')
    #for json_file in json_dir:
        #with open(json_file, 'r', encoding="utf8") as arquivo:
            #apps = json.load(arquivo)
            #nome_do_app = apps['activity_name'].split('/')[0]
            #print(nome_do_app)
    apps = df["App Package Name"].tolist()
    apps = apps[0:]
    partes_array = [apps[i : i + len(apps) // 8] for i in range(0, len(apps), len(apps) // 8)]
    print(apps.__len__()/8)
    with Pool(processes=8) as p:
        p.map(processa_array, partes_array)
    print('Processamento Concluído!')
       

            

if __name__ == "__main__":
  main()    