import matplotlib.pyplot as plt
import pandas as pd
import os
from scipy.stats import shapiro
from scipy import stats
import numpy as np

# Get current working directory
cwd = os.getcwd()

# Read in MAP/MPE results
MAP_5 = pd.read_csv(f'{cwd}/results/5/MAP.csv')
MPE_5 = pd.read_csv(f'{cwd}/results/5/MPE.csv')

MAP_15 = pd.read_csv(f'{cwd}/results/15/MAP.csv')
MPE_15 = pd.read_csv(f'{cwd}/results/15/MPE.csv')

MAP_25 = pd.read_csv(f'{cwd}/results/25/MAP.csv')
MPE_25 = pd.read_csv(f'{cwd}/results/25/MPE.csv')





MAP_5_min_degree = list(MAP_5['runtime_degree'])
MAP_5_min_fill = list(MAP_5['runtime_minfill'])
MAP_5_random = list(MAP_5['runtime_random'])

MAP_15_min_degree = list(MAP_15['runtime_degree'])
MAP_15_min_fill = list(MAP_15['runtime_minfill'])
MAP_15_random = list(MAP_15['runtime_random'])

MAP_25_min_degree = list(MAP_25['runtime_degree'])
MAP_25_min_fill = list(MAP_25['runtime_minfill'])
MAP_25_random = list(MAP_25['runtime_random'])

MPE_5_min_degree = list(MPE_5['runtime_degree'])
MPE_5_min_fill = list(MPE_5['runtime_minfill'])
MPE_5_random = list(MPE_5['runtime_random'])

MPE_15_min_degree = list(MPE_15['runtime_degree'])
MPE_15_min_fill = list(MPE_15['runtime_minfill'])
MPE_15_random = list(MPE_15['runtime_random'])

MPE_25_min_degree = list(MPE_25['runtime_degree'])
MPE_25_min_fill = list(MPE_25['runtime_minfill'])
MPE_25_random = list(MPE_25['runtime_random'])


# NORMALITY

########MAP:
print('######-----NORMALITY for MAP:\n')


# net5
print('---for NET 5')

# Normally distributed:
stat, p = shapiro(MAP_5_min_degree)
print('Normality min_degree:','Statistics=%.3f, p=%.3f' % (stat, p))
stat, p = shapiro(MAP_5_min_fill)
print('Normality min_fill:','Statistics=%.3f, p=%.3f' % (stat, p))
stat, p = shapiro(MAP_5_random)
print('Normality random:','Statistics=%.3f, p=%.3f' % (stat, p))

# net15
print('---for NET 15')

# Normally distributed:
stat, p = shapiro(MAP_15_min_degree)
print('Normality min_degree:','Statistics=%.3f, p=%.3f' % (stat, p))
stat, p = shapiro(MAP_15_min_fill)
print('Normality min_fill:','Statistics=%.3f, p=%.3f' % (stat, p))
stat, p = shapiro(MAP_15_random)
print('Normality random:','Statistics=%.3f, p=%.3f' % (stat, p))

# net25
print('---for NET 25')

# Normally distributed:
stat, p = shapiro(MAP_25_min_degree)
print('Normality min_degree:','Statistics=%.3f, p=%.3f' % (stat, p))
stat, p = shapiro(MAP_25_min_fill)
print('Normality min_fill:','Statistics=%.3f, p=%.3f' % (stat, p))
stat, p = shapiro(MAP_25_random)
print('Normality random:','Statistics=%.3f, p=%.3f' % (stat, p))


########MAP:
print('\n\n######-----NORMALITY for MEP:\n')


# net5
print('---for NET 5')

# Normally distributed:
stat, p = shapiro(MPE_5_min_degree)
print('Normality min_degree:','Statistics=%.3f, p=%.3f' % (stat, p))
stat, p = shapiro(MPE_5_min_fill)
print('Normality min_fill:','Statistics=%.3f, p=%.3f' % (stat, p))
stat, p = shapiro(MPE_5_random)
print('Normality random:','Statistics=%.3f, p=%.3f' % (stat, p))

# net15
print('---for NET 15')

# Normally distributed:
stat, p = shapiro(MPE_15_min_degree)
print('Normality min_degree:','Statistics=%.3f, p=%.3f' % (stat, p))
stat, p = shapiro(MPE_15_min_fill)
print('Normality min_fill:','Statistics=%.3f, p=%.3f' % (stat, p))
stat, p = shapiro(MPE_15_random)
print('Normality random:','Statistics=%.3f, p=%.3f' % (stat, p))

# net25
print('---for NET 25')

# Normally distributed:
stat, p = shapiro(MPE_25_min_degree)
print('Normality min_degree:','Statistics=%.3f, p=%.3f' % (stat, p))
stat, p = shapiro(MPE_25_min_fill)
print('Normality min_fill:','Statistics=%.3f, p=%.3f' % (stat, p))
stat, p = shapiro(MPE_25_random)
print('Normality random:','Statistics=%.3f, p=%.3f' % (stat, p))



# SIGNIFICANCE

########MAP:
print('\n\n\n######-----SIGNIFICANCE for MAP:\n')


# net5
print('---for NET 5')


# Significance distributed:
stat, p = stats.mannwhitneyu(MAP_5_min_degree, MAP_5_min_fill)
print('Significance min_degree & min_fill:', 'Statistics=%.3f, p=%.3f' % (stat, p))
stat, p = stats.mannwhitneyu(MAP_5_min_degree, MAP_5_random, alternative= 'greater')
print('Significance min_degree & random:', 'Statistics=%.3f, p=%.3f' % (stat, p))
stat, p = stats.mannwhitneyu(MAP_5_min_fill, MAP_5_random,alternative= 'greater')
print('Significance min_fill & random:', 'Statistics=%.3f, p=%.3f' % (stat, p))

print('---for NET 15')

# Significance distributed:
stat, p = stats.mannwhitneyu(MAP_15_min_degree, MAP_15_min_fill)
print('Significance min_degree & min_fill:', 'Statistics=%.3f, p=%.3f' % (stat, p))
stat, p = stats.mannwhitneyu(MAP_15_min_degree, MAP_15_random)
print('Significance min_degree & random:', 'Statistics=%.3f, p=%.3f' % (stat, p))
stat, p = stats.mannwhitneyu(MAP_15_min_fill, MAP_15_random)
print('Significance min_fill & random:', 'Statistics=%.3f, p=%.3f' % (stat, p))

print('---for NET 25')

# Significance distributed:
stat, p = stats.mannwhitneyu(MAP_25_min_degree, MAP_25_min_fill)
print('Significance min_degree & min_fill:', 'Statistics=%.3f, p=%.3f' % (stat, p))
stat, p = stats.mannwhitneyu(MAP_25_min_degree, MAP_25_random)
print('Significance min_degree & random:', 'Statistics=%.3f, p=%.3f' % (stat, p))
stat, p = stats.mannwhitneyu(MAP_25_min_fill, MAP_25_random)
print('Significance min_fill & random:', 'Statistics=%.3f, p=%.3f' % (stat, p))




########MEP:
print('\n\n######-----SIGNIFICANCE for MEP:\n')


# net5
print('---for NET 5')


# Significance distributed:
stat, p = stats.mannwhitneyu(MPE_5_min_degree, MPE_5_min_fill)
print('Significance min_degree & min_fill:', 'Statistics=%.3f, p=%.3f' % (stat, p))
stat, p = stats.mannwhitneyu(MPE_5_min_degree, MPE_5_random)
print('Significance min_degree & random:', 'Statistics=%.3f, p=%.3f' % (stat, p))
stat, p = stats.mannwhitneyu(MPE_5_min_fill, MPE_5_random)
print('Significance min_fill & random:', 'Statistics=%.3f, p=%.3f' % (stat, p))

print('---for NET 15')

# Significance distributed:
stat, p = stats.mannwhitneyu(MPE_15_min_degree, MPE_15_min_fill)
print('Significance min_degree & min_fill:', 'Statistics=%.3f, p=%.3f' % (stat, p))
stat, p = stats.mannwhitneyu(MPE_15_min_degree, MPE_15_random)
print('Significance min_degree & random:', 'Statistics=%.3f, p=%.3f' % (stat, p))
stat, p = stats.mannwhitneyu(MPE_15_min_fill, MPE_15_random)
print('Significance min_fill & random:', 'Statistics=%.3f, p=%.3f' % (stat, p))

print('---for NET 25')

# Significance distributed:
stat, p = stats.mannwhitneyu(MPE_25_min_degree, MPE_25_min_fill,alternative='less')
print('Significance min_degree & min_fill:', 'Statistics=%.3f, p=%.8f' % (stat, p))
stat, p = stats.mannwhitneyu(MPE_25_min_degree, MPE_25_random, alternative='less')
print('Significance min_degree & random:', 'Statistics=%.3f, p=%.8f' % (stat, p))
stat, p = stats.mannwhitneyu(MPE_25_min_fill, MPE_25_random, alternative='less')
print('Significance min_fill & random:', 'Statistics=%.3f, p=%.8f' % (stat, p))



########MEP:
print('\n\n######-----MEAN/SD/MIN/MAX for MAP:\n')


# net5
print('---for NET 5')


# Significance distributed:
mean = np.mean(MAP_5_min_degree)
median = np.median(MAP_5_min_degree)
sd = np.std(MAP_5_min_degree)
max = np.max(MAP_5_min_degree)
min = np.min(MAP_5_min_degree)

print('Min degree:', 'mean:', mean, ',| median:', median, '| sd:', '| max:', max, '| min:', min)
mean = np.mean(MAP_5_min_fill)
median = np.median(MAP_5_min_fill)
sd = np.std(MAP_5_min_fill)
max = np.max(MAP_5_min_fill)
min = np.min(MAP_5_min_fill)

print('Min fill:', 'mean:', mean, ',| median:', median, '| sd:', '| max:', max, '| min:', min)
mean = np.mean(MAP_5_random)
median = np.median(MAP_5_random)
sd = np.std(MAP_5_random)
max = np.max(MAP_5_random)
min = np.min(MAP_5_random)

print('random:', 'mean:', mean, ',| median:', median, '| sd:', '| max:', max, '| min:', min)

print('---for NET 15')

mean = np.mean(MAP_15_min_degree)
median = np.median(MAP_15_min_degree)
sd = np.std(MAP_15_min_degree)
max = np.max(MAP_15_min_degree)
min = np.min(MAP_15_min_degree)

print('Min degree:', 'mean:', mean, ',| median:', median, '| sd:', '| max:', max, '| min:', min)
mean = np.mean(MAP_15_min_fill)
median = np.median(MAP_15_min_fill)
sd = np.std(MAP_15_min_fill)
max = np.max(MAP_15_min_fill)
min = np.min(MAP_15_min_fill)

print('Min fill:', 'mean:', mean, ',| median:', median, '| sd:', '| max:', max, '| min:', min)
mean = np.mean(MAP_15_random)
median = np.median(MAP_15_random)
sd = np.std(MAP_15_random)
max = np.max(MAP_15_random)
min = np.min(MAP_15_random)

print('random:', 'mean:', mean, ',| median:', median, '| sd:', '| max:', max, '| min:', min)

print('---for NET 25')

# Significance distributed:
mean = np.mean(MAP_25_min_degree)
median = np.median(MAP_25_min_degree)
sd = np.std(MAP_25_min_degree)
max = np.max(MAP_25_min_degree)
min = np.min(MAP_25_min_degree)

print('Min degree:', 'mean:', mean, ',| median:', median, '| sd:', '| max:', max, '| min:', min)
mean = np.mean(MAP_25_min_fill)
median = np.median(MAP_25_min_fill)
sd = np.std(MAP_25_min_fill)
max = np.max(MAP_25_min_fill)
min = np.min(MAP_25_min_fill)

print('Min fill:', 'mean:', mean, ',| median:', median, '| sd:', '| max:', max, '| min:', min)
mean = np.mean(MAP_25_random)
median = np.median(MAP_25_random)
sd = np.std(MAP_25_random)
max = np.max(MAP_25_random)
min = np.min(MAP_25_random)

print('random:', 'mean:', mean, ',| median:', median, '| sd:', '| max:', max, '| min:', min)


print('\n\n######-----MEAN/SD/MIN/MAX for MEP:\n')


# net5
print('---for NET 5')


# Significance distributed:
mean = np.mean(MPE_5_min_degree)
median = np.median(MPE_5_min_degree)
sd = np.std(MPE_5_min_degree)
max = np.max(MPE_5_min_degree)
min = np.min(MPE_5_min_degree)

print('Min degree:', 'mean:', mean, ',| median:', median, '| sd:', '| max:', max, '| min:', min)
mean = np.mean(MPE_5_min_fill)
median = np.median(MPE_5_min_fill)
sd = np.std(MPE_5_min_fill)
max = np.max(MPE_5_min_fill)
min = np.min(MPE_5_min_fill)

print('Min fill:', 'mean:', mean, ',| median:', median, '| sd:', '| max:', max, '| min:', min)
mean = np.mean(MPE_5_random)
median = np.median(MPE_5_random)
sd = np.std(MPE_5_random)
max = np.max(MPE_5_random)
min = np.min(MPE_5_random)

print('random:', 'mean:', mean, ',| median:', median, '| sd:', '| max:', max, '| min:', min)

print('---for NET 15')

mean = np.mean(MPE_15_min_degree)
median = np.median(MPE_15_min_degree)
sd = np.std(MPE_15_min_degree)
max = np.max(MPE_15_min_degree)
min = np.min(MPE_15_min_degree)

print('Min degree:', 'mean:', mean, ',| median:', median, '| sd:', '| max:', max, '| min:', min)
mean = np.mean(MPE_15_min_fill)
median = np.median(MPE_15_min_fill)
sd = np.std(MPE_15_min_fill)
max = np.max(MPE_15_min_fill)
min = np.min(MPE_15_min_fill)

print('Min fill:', 'mean:', mean, ',| median:', median, '| sd:', '| max:', max, '| min:', min)
mean = np.mean(MPE_15_random)
median = np.median(MPE_15_random)
sd = np.std(MPE_15_random)
max = np.max(MPE_15_random)
min = np.min(MPE_15_random)

print('random:', 'mean:', mean, ',| median:', median, '| sd:', '| max:', max, '| min:', min)

print('---for NET 25')

# Significance distributed:
mean = np.mean(MPE_25_min_degree)
median = np.median(MPE_25_min_degree)
sd = np.std(MPE_25_min_degree)
max = np.max(MPE_25_min_degree)
min = np.min(MPE_25_min_degree)

print('Min degree:', 'mean:', mean, ',| median:', median, '| sd:', '| max:', max, '| min:', min)
mean = np.mean(MPE_25_min_fill)
median = np.median(MPE_25_min_fill)
sd = np.std(MPE_25_min_fill)
max = np.max(MPE_25_min_fill)
min = np.min(MPE_25_min_fill)

print('Min fill:', 'mean:', mean, ',| median:', median, '| sd:', '| max:', max, '| min:', min)
mean = np.mean(MPE_25_random)
median = np.median(MPE_25_random)
sd = np.std(MPE_25_random)
max = np.max(MPE_25_random)
min = np.min(MPE_25_random)

print('random:', 'mean:', mean, ',| median:', median, '| sd:', '| max:', max, '| min:', min)


# # Uncomment for MAP:
# net5 = []
# net5.append(MAP_5_min_degree)
# net5.append(MAP_5_min_fill)
# net5.append(MAP_5_random)

# net15 = []
# net15.append(MAP_15_min_degree)
# net15.append(MAP_15_min_fill)
# net15.append(MAP_15_random)

# net25 = []
# net25.append(MAP_25_min_degree)
# net25.append(MAP_25_min_fill)
# net25.append(MAP_25_random)

# Uncomment for MPE:
net5 = []
net5.append(MPE_5_min_degree)
net5.append(MPE_5_min_fill)
net5.append(MPE_5_random)

net15 = []
net15.append(MPE_15_min_degree)
net15.append(MPE_15_min_fill)
net15.append(MPE_15_random)

net25 = []
net25.append(MPE_25_min_degree)
net25.append(MPE_25_min_fill)
net25.append(MPE_25_random)


min_degree = []
min_degree.append(net5[0])
min_degree.append(net15[0])
min_degree.append(net25[0])

min_fill = []
min_fill.append(net5[2])
min_fill.append(net15[2])
min_fill.append(net25[1])

random = []
random.append(net5[1])
random.append(net15[1])
random.append(net25[2])

left_positions = [-0.6, 1.9, 4.4]
middle_positions = [0, 2.5, 5]
right_positions = [0.6, 3.1, 5.6]

# Nice equal distribution on x-axis
ticks = [0, 2.5, 5]
labels = ['5 variables', '15 variables', '25 variables']

# Lagarithmic x-axis for readability
plt.yscale('log')
plt.boxplot(min_degree, positions = left_positions, showfliers=False, )
plt.boxplot(min_fill, positions = middle_positions, showfliers=False)
plt.boxplot(random, positions = right_positions, showfliers=False)
plt.yscale = 'log'
plt.xticks(ticks, labels)
plt.yscale = 'log'
plt.legend(['min degree', 'min fill', 'random'], loc='upper left')
plt.ylabel('runtime (s)')
plt.suptitle('MEP runtimes per variable size/heurstic')
plt.yscale = 'log'
plt.savefig(f'plots.jpg')
plt.show



