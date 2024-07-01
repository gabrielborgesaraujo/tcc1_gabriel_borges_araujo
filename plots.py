import json
import matplotlib.pyplot as plt
import numpy as np

def criar_grafico_barras():
    # Dados
    categorias = ['Total de Apps', 'Apps Validos', 'Apps Sem Telas']
    valores = [9384, 583, 131]
    cores = ['red', 'blue', 'green']

    porcentagens = [(9384/9384*100), (583/9384*100), (131/9384*100)]
    
    # Criar gráfico
    plt.figure(figsize=(8, 6))
    plt.bar(categorias, valores, color=cores)
    # Adicionar títulos e rótulos
    plt.title('Total de Apps x Apps Válidos x Apps Sem Telas')
    plt.ylabel('Valores')
    barras = plt.bar(categorias, valores, color=cores)
    
    for barra, texto in zip(barras, porcentagens):
        altura = barra.get_height()
        texto_formatado = f'{texto:.1f}%'
        plt.text(barra.get_x() + barra.get_width() / 2, altura+120, texto_formatado,
                 ha='center', va='center', color='black', fontsize=10, fontweight='bold')
            
    
    # Exibir gráfico
    plt.savefig('data/imgs/total_apps_x_apps_validos_x_apps_sem_telas.png')
    plt.show()
# Chamar a função para criar e mostrar o gráfico

def resultados_totais():
    categorias = ['Total de Textos', "Textos Conformes", 'Total de Telas', 'Telas Conformes']
    valores = [1230033, 851205, 66261, 11400 ]
    cores = plt.cm.tab20c(np.linspace(0, 1, len(categorias)))

    porcentagens = [(1230033/1230033*100), (851205/1230033*100), (66261/66261*100), (11400/66261*100)]
    
    # Criar gráfico
    plt.figure(figsize=(8, 6))
    plt.bar(categorias, valores, color=cores)
    # Adicionar títulos e rótulos
    plt.title('Resultado Total de Elementos')
    plt.ylabel('Valores')
    barras = plt.bar(categorias, valores, color=cores)
    
    for barra, texto in zip(barras, porcentagens):
        altura = barra.get_height()
        texto_formatado = f'{texto:.1f}%'
        plt.text(barra.get_x() + barra.get_width() / 2, altura+20000, texto_formatado,
                 ha='center', va='center', color='black', fontsize=10, fontweight='bold')
            
    
    # Exibir gráfico
    plt.savefig('data/imgs/resultados_totais.png')
    plt.show()


def resultados_totais_pizza():
    categorias = ['Textos Desconformes', "Textos Conformes"]
    valores = [1230033-851205, 851205]
    explode = (0.1, 0)
    cores = ["orange", "lightblue"]
    
    # Criar gráfico
    plt.figure(figsize=(8, 6))
    # Criação do gráfico de pizza
    plt.pie(valores, explode=explode, labels=categorias, colors=cores,
        autopct='%1.1f%%', shadow=True, startangle=140)

    # Adiciona a legenda
    plt.legend(categorias, loc="best")

    # Assegura que o gráfico de pizza é desenhado como um círculo
    plt.axis('equal')
    plt.title('Resultado Total de Elementos Textuais')
    # Exibir gráfico
    plt.savefig('data/imgs/resultados_totais_textuais_pizza.png')
    plt.show()


def resultados_totais_pizza_telas():
    categorias = ['Telas Desconformes', "Telas Conformes"]
    valores = [54861, 11400]
    explode = (0.1, 0)
    cores = ["lightcoral", "lightgreen"]
    # Criar gráfico
    plt.figure(figsize=(8, 6))
    # Criação do gráfico de pizza
    plt.pie(valores, explode=explode, labels=categorias, colors=cores,
        autopct='%1.1f%%', shadow=True, startangle=140)

    # Adiciona a legenda
    plt.legend(categorias, loc="best")

    # Assegura que o gráfico de pizza é desenhado como um círculo
    plt.axis('equal')
    plt.title('Resultado Total de Telas')
    # Exibir gráfico
    plt.savefig('data/imgs/resultados_totais_telas_pizza.png')
    plt.show()


def aplicativos_por_categoria():
    with open('data/apps_metrics.json', 'r') as arquivo:
        dados = json.load(arquivo)
        categorias = list([categoria["nome"] for categoria in dados["categorias"]])[:-1]
        valores = list([categoria["total_apps_na_categoria"] for categoria in dados["categorias"]])[:-1]

    #categorias = ['Total de Textos', 'Total de Telas', 'Telas Conformes', "Textos Conformes"]
    
    cores = plt.cm.tab20c(np.linspace(0, 1, len(categorias)))
    
    # Criar gráfico
    plt.figure(figsize=(12, 8))
    bars = plt.bar(categorias, valores, color=cores)
    plt.xticks(rotation=90)
    # Adicionar títulos e rótulos
    plt.title('Aplicativos por Categoria')
    plt.ylabel('Quantidade de Aplicativos')
    plt.legend(bars, categorias, loc="best", bbox_to_anchor=(1, 1), title="Categorias")
    plt.tight_layout()
    
            
    
    # Exibir gráfico
    plt.savefig('data/imgs/aplicativos_por_categoria.png')
    plt.show()

def aplicativos_invalidos_por_categoria():
    with open('data/apps_metrics.json', 'r') as arquivo:
        dados = json.load(arquivo)
        categorias = list([categoria["nome"] for categoria in dados["categorias"]])[:-1]
        valores = list([categoria["qtd_apps_reprovados"] for categoria in dados["categorias"]])[:-1]
        valoresTotais = list([categoria["total_apps_na_categoria"] for categoria in dados["categorias"]])[:-1]
        porcentagens = [(valor/total*100) for valor, total in zip(valores, valoresTotais)]

    #categorias = ['Total de Textos', 'Total de Telas', 'Telas Conformes', "Textos Conformes"]
    
    cores = plt.cm.tab20c(np.linspace(0, 1, len(categorias)))
    
    # Criar gráfico
    plt.figure(figsize=(12, 8))
    bars = plt.bar(categorias, valores, color=cores, width=0.5)
    plt.xticks(rotation=90)
    # Adicionar títulos e rótulos
    plt.title('Aplicativos por Categoria')
    plt.ylabel('Quantidade de Aplicativos')
    # Adicionando as porcentagens acima de cada barra
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height,
                 f'{porcentagens[i]:.1f}%', ha='center', va='bottom')
    plt.legend(bars, categorias, loc="best", bbox_to_anchor=(1, 1), title="Categorias")
    plt.tight_layout()
    
            
    
    # Exibir gráfico
    plt.savefig('data/imgs/aplicativos_invalidos_por_categoria.png')
    plt.show()


def porcentagens_de_aceite():
    # Dados
    categorias = ['100%', '99.9% - 75%', '74.9% - 50%', '49.9% - 25%', '24.9% - 0%', 'Sem Telas']
    valores = [583, 3893, 3446, 1116, 215, 131]
    cores = plt.cm.tab20c(np.linspace(0, 1, len(categorias)))

    porcentagens = [(583/9384*100), (3893/9384*100), (3446/9384*100), (1116/9384*100), (215/9384*100), (131/9384*100)]
    # Criar gráfico
    plt.figure(figsize=(12, 8))
    plt.bar(categorias, valores, color=cores)
    # Adicionar títulos e rótulos
    plt.title('Porcentagem de Elementos Válidos por Aplicativo')
    plt.ylabel('Valores')
    barras = plt.bar(categorias, valores, color=cores)
    
    for barra, texto in zip(barras, porcentagens):
        altura = barra.get_height()
        texto_formatado = f'{texto:.1f}%'
        plt.text(barra.get_x() + barra.get_width() / 2, altura+120, texto_formatado,
                 ha='center', va='center', color='black', fontsize=10, fontweight='bold')
            
    
    # Exibir gráfico
    plt.savefig('data/imgs/porcentagem_de_elementos_validos_por_aplicativo.png')
    plt.show()
# Chamar a função para criar e mostrar o gráfico

#criar_grafico_barras()
#resultados_totais()
#aplicativos_invalidos_por_categoria()
#porcentagens_de_aceite()
#resultados_totais_pizza()
resultados_totais_pizza_telas()