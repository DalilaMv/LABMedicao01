import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')

data = pd.read_csv('resultados.csv')
data_df = pd.DataFrame(data)

data_df = data_df.drop(['Número', 'Nome', 'Estrelas'], axis=1)


for col in data_df.columns:
    if col == 'Linguagem Primária': 
        moda = data_df[col].mode()[0]
        print('Estatísticas para a coluna', col)
        print('Moda:', moda)
        counts = data_df['Linguagem Primária'].value_counts()
        print('Quantidade de vezes que cada linguagem aparece na amostra:')
        print(counts)
        print('')
        continue
    
    media = data_df[col].mean()
    moda = data_df[col].mode()[0]
    mediana = data_df[col].median()
    desvio_padrao = data_df[col].std()

    print('Estatísticas para a coluna', col)
    print('Média:', media)
    print('Moda:', moda)
    print('Mediana:', mediana)
    print('Desvio padrão:', desvio_padrao)
    print()


# histograma "Idade (anos)"
data_df['Idade (anos)'].plot.hist(bins=20)
plt.xlabel('Idade (anos)')
plt.ylabel('Frequência')
plt.show()

data_df.boxplot(column='PRs Aprovados')
plt.show()
data_df.boxplot(column='Releases')
plt.show()