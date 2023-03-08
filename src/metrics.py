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


# Q01 - boxplot"
data_df.boxplot(column='Idade (anos)')
plt.show()

# Q02 - boxplot"
data_df.boxplot(column='PRs Aprovados')
plt.show()

# Q03 - boxplot"
data_df.boxplot(column='Releases')
plt.show()

# Q04 - boxplot"
data_df.boxplot(column='Dias sem Update')
plt.show()

# Q05 - histograma
counts = data_df['Linguagem Primária'].value_counts()
plt.bar(counts.index, counts.values)
plt.xticks(rotation=90)
plt.show()

# Q06 - boxplot"
data_df.boxplot(column='Razão de Issues Fechadas')
plt.show()
