
def z_5_1(data, gamma, yr_qvant):
    data = f"'''{data}'''"
    print(f'''
import numpy as np
import scipy.stats as sts
import matplotlib.pyplot as plt
import pandas as pd

data = {data}
gamma = {gamma}
yr_qvant = {yr_qvant}

data = data.split(sep='; ')
data_grap = data.copy()
n = len(data)
print('Объем выборки ', n)
count_NA = data.count('NA')
print('Количество NA', count_NA)
data = [i for i in data if (i != ' NA') and (i != 'NA')]
data = pd.Series([float(i) for i in data if (i != ' NA') or (i != 'NA')])
n_without = len(data)
print('Объем без NA ', n_without)

print('Минимальное значение в вариационном ряду', min(data))
print('Максимальное значение в вариационном ряду', max(data))
print('Размах выборки', max(data) - min(data))
Q1 = np.quantile(data, 0.25)
print('Значение первой квартили (Q1)', Q1)
Q2 = np.quantile(data, 0.5)
print('Значение медианы (Q2)', Q2)
Q3 = np.quantile(data, 0.75)
print('Значение третьей квартили (Q3)', Q3)
R = Q3 - Q1
print('Квартильный размах', R)
mean = data.mean()
print('Среднее выборочное значение', mean)
std_corr = data.std(ddof=1)
print('Стандартное отклонение (S) корень из дисп.в (исправленной)', std_corr)
var_corr = data.var(ddof=1)
print('Исправленная дисперсия ', var_corr)
kurt = sts.kurtosis(data, bias=False)
print('Эксцесс (формула по умолчанию в Excel)', sts.kurtosis(data, bias=False))
skew = sts.skew(data, bias=False)
print('Коэффициент асимметрии (формула по умолчанию в Excel)', skew)
error = std_corr / n_without**0.5
print('Ошибка выборки', error)
print('Значение ', yr_qvant, ' квантили', np.quantile(data, yr_qvant))
x_stat_max = Q3 + 1.5 * R
print('Верхняя граница нормы (Xst_max)', x_stat_max)
x_stat_min = Q1 - 1.5 * R
print('Нижняя граница нормы (Xst_min)', x_stat_min)
print('Количество выбросов ниже нижней нормы', len(data[data < x_stat_min]))
print('Количество выбросов выше верхней нормы', len(data[data > x_stat_max]))
print('Общее количество выбросов', len(data[(data > Q3 + 1.5 * R) | (data < Q1 - 1.5 * R)]))

interv = sts.t.interval(gamma, n - 1, mean, std_corr / np.sqrt(n_without))
print('доверительный интервал для E(X)', gamma, ' уровняя ', interv)

chi2_gamma1 = sts.chi2.ppf((1 - gamma) / 2, n_without - 1)
chi2_gamma2 = sts.chi2.ppf((1 + gamma) / 2, n_without - 1)
print('доверительный интервал для Var(X)', gamma, ' уровняя ', 
      (n_without - 1) * var_corr / chi2_gamma2, (n_without - 1) * var_corr / chi2_gamma1)

data = pd.Series([float(i.replace(',', '.')) for i in data_grap if i != 'NA'])

plt.figure(figsize=(8, 4))
plt.hist(data, bins=10, edgecolor='black')
plt.title('Гистограмма c выбросами')
plt.show()

plt.figure(figsize=(8, 4))
plt.boxplot(data, vert=True, patch_artist=True, showmeans=True)
plt.title('Диаграмма "Ящик с усиками" с выбросами')
plt.show()

data = pd.Series([i for i in data if i != np.nan])
data = data[(data < x_stat_max) & (data > x_stat_min)]

plt.figure(figsize=(8, 4))
plt.hist(data, bins=10, edgecolor='black')
plt.title('Гистограмма без выбросов и NA ')
plt.show()

plt.figure(figsize=(8, 4))
plt.boxplot(data, vert=True, patch_artist=True, showmeans=True)
plt.title('Диаграмма "Ящик с усиками" без выбросов и NA')
plt.show()
''')

