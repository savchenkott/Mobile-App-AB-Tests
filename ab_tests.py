import itertools
from scipy.stats import norm, shapiro, t, f
import numpy as np
import math
import pandas as pd
from functools import reduce
import operator


def z_score(x, mean, stdev, right_tailed=True):

    z_score = (x-mean)/stdev
    if right_tailed == True:
        p_value = (1-norm.cdf(z_score))
    elif right_tailed == False:
        p_value = (norm.cdf(z_score))
    else:
        raise ValueError("right_tailed must be True or False")
    return p_value


def z_score_for_df(point, df, column, right_tailed=True):

    mean = df[column].mean()
    stdev = df[column].std()
    normality = shapiro(df[column])[1]

    if normality <= 0.05:
        p_value = z_score(x=point, mean=mean, stdev=stdev, right_tailed=right_tailed)
    else:
        print(f"Data not normally distributed. Shapiro-Wilk test p-value is {normality}")
        p_value = z_score(x=point, mean=mean, stdev=stdev, right_tailed=right_tailed)

    return p_value


def unpaired_t_test(x1, x2, std1, std2, n1, n2, tail='two'):

    se1 = (std1 ** 2)/ n1
    se2 = (std2 ** 2) / n2
    t_stat = (x1-x2)/math.sqrt(se1+se2)
    degrees_of_freedom = (n1+n2)-2

    if tail == 'right':
        p_value = 1 - t.cdf(t_stat, df=degrees_of_freedom)
    elif tail == 'left':
        p_value = t.cdf(t_stat, df=degrees_of_freedom)
    elif tail == 'two':
        p_value = 2 * (1 - abs(t.cdf(abs(t_stat), df=degrees_of_freedom)))
    else:
        raise ValueError("tail must be 'right', 'left', or 'two'")

    return p_value


def unpaired_t_test_for_df(df, category_column, group1, group2, numerical_column, tail='two'):

    df_for_group1 = df[df[category_column] == group1]
    df_for_group2 = df[df[category_column] == group2]

    x1 = df_for_group1[numerical_column].mean()
    x2 = df_for_group2[numerical_column].mean()
    std1 = df_for_group1[numerical_column].std()
    std2 = df_for_group2[numerical_column].std()
    n1 = len(df_for_group1)
    n2 = len(df_for_group2)

    p_value = unpaired_t_test(x1=x1, x2=x2, std1=std1, std2=std2, n1=n1, n2=n2, tail=tail)

    return p_value


def paired_t_test(differences_mean, differences_stdev, n, tail='two'):

    t_stat = (differences_mean * math.sqrt(n)) / differences_stdev
    degrees_of_freedom = n - 1

    if tail == 'right':
        p_value = 1 - t.cdf(t_stat, df=degrees_of_freedom)
    elif tail == 'left':
        p_value = t.cdf(t_stat, df=degrees_of_freedom)
    elif tail == 'two':
        p_value = 2 * (1 - abs(t.cdf(abs(t_stat), df=degrees_of_freedom)))
    else:
        raise ValueError("tail must be 'right', 'left', or 'two'")

    return p_value


def paired_t_test_for_df(df, id_column, period_column, period1, period2, numerical_column, tail='two'):
    list_of_differences = []

    for unique_id in df[id_column].unique():
        dataframe = df[df[id_column] == unique_id]
        if period1 in dataframe[period_column].values and period2 in dataframe[period_column].values:
            value_period1 = dataframe[dataframe[period_column] == period1][numerical_column].values[0]
            value_period2 = dataframe[dataframe[period_column] == period2][numerical_column].values[0]
            difference = value_period1 - value_period2
            list_of_differences.append(difference)

    differences_mean = np.mean(list_of_differences)
    differences_stdev = np.std(list_of_differences, ddof=1)
    n = len(list_of_differences)
    p_value = paired_t_test(differences_mean=differences_mean, differences_stdev=differences_stdev, n=n, tail=tail)
    return p_value


def one_way_anova(sst, ssw, n, k):
    ssb = sst - ssw
    degrees_of_freedom_within = n - k
    degrees_of_freedom_between = k - 1

    msw = ssw / degrees_of_freedom_within
    msb = ssb / degrees_of_freedom_between
    f_stat = msb / msw

    p_value = f.sf(f_stat, degrees_of_freedom_between, degrees_of_freedom_within)

    return p_value


def one_way_anova_for_df(df, category_column, group_of_interest, numerical_column):
    df_for_anova = df[df[category_column].isin(group_of_interest)]
    grand_mean = df_for_anova[numerical_column].mean()

    sst = 0
    for row in df_for_anova[numerical_column]:
        sst += ((row - grand_mean) ** 2)

    ssw = 0
    for group in group_of_interest:
        df_of_a_group = df_for_anova[df_for_anova[category_column] == group]
        group_mean = df_of_a_group[numerical_column].mean()
        for row in df_of_a_group[numerical_column]:
            ssw += ((row - group_mean) ** 2)

    n = len(df_for_anova)
    k = len(group_of_interest)

    p_value = one_way_anova(sst=sst, ssw=ssw, n=n, k=k)

    return p_value


def two_way_anova(ssa, ssb, ssw, ssi, n, k_a, k_b):

    degrees_of_freedom_within = n - (k_a * k_b) # n - k_a * k_b
    degrees_of_freedom_a = k_a - 1
    degrees_of_freedom_b = k_b - 1
    degrees_of_freedom_interaction = (k_a - 1) * (k_b - 1)

    msw = ssw / degrees_of_freedom_within
    msa = ssa / degrees_of_freedom_a
    msb = ssb / degrees_of_freedom_b
    msi = ssi / degrees_of_freedom_interaction

    f_stat_a = msa / msw
    f_stat_b = msb / msw
    f_stat_interaction = msi / msw

    p_value_a = f.sf(f_stat_a, degrees_of_freedom_a, degrees_of_freedom_within)
    p_value_b = f.sf(f_stat_b, degrees_of_freedom_b, degrees_of_freedom_within)
    p_value_interaction = f.sf(f_stat_interaction, degrees_of_freedom_interaction, degrees_of_freedom_within)

    return p_value_a, p_value_b, p_value_interaction


def two_way_anova_for_df(df, dictionary_with_groups, numerical_column):

    var1 = list(dictionary_with_groups.keys())[0]
    var2 = list(dictionary_with_groups.keys())[1]

    df_for_two_way_anova = df[[var1, var2, numerical_column]]

    group_of_interest_1 = dictionary_with_groups[var1]
    group_of_interest_2 = dictionary_with_groups[var2]

    df1 = df_for_two_way_anova[df_for_two_way_anova[var1].isin(group_of_interest_1)]
    df2 = df_for_two_way_anova[df_for_two_way_anova[var2].isin(group_of_interest_2)]

    k_a = len(group_of_interest_1)
    k_b = len(group_of_interest_2)

    grand_mean = df_for_two_way_anova[numerical_column].mean()

    ssa = 0
    for level in group_of_interest_1:
        df1_group = df1[df1[var1] == level][numerical_column]
        df1_group_mean = df1_group.mean()
        ssa += ((df1_group_mean - grand_mean) ** 2)

    ssb = 0
    for group in group_of_interest_2:
        df2_group = df2[df2[var2] == group][numerical_column]
        df2_group_mean = df2_group.mean()
        ssb += ((df2_group_mean - grand_mean) ** 2)

    ssw = 0
    for level_a in group_of_interest_1:
        for level_b in group_of_interest_2:
            df_group = df_for_two_way_anova[(df_for_two_way_anova[var1] == level_a) &
                                            (df_for_two_way_anova[var2] == level_b)][numerical_column]
            group_mean = df_group.mean()
            for row in df_group:
                ssw += ((row - group_mean) ** 2)

    sst = 0
    for level_a in group_of_interest_1:
        for level_b in group_of_interest_2:
            df_ab = df_for_two_way_anova[(df_for_two_way_anova[var1] == level_a) & (
                        df_for_two_way_anova[var2] == level_b)][numerical_column]
            for row in df_ab:
                sst += ((row - grand_mean) ** 2)

    ssi = sst - ssa - ssb - ssw

    n = len(df_for_two_way_anova)

    p_value_a, p_value_b, p_value_interaction = two_way_anova(ssa=ssa, ssb=ssb, ssw=ssw, ssi=ssi, n=n, k_a=k_a, k_b=k_b)

    p_values = {var1: p_value_a, var2: p_value_b, 'interaction': p_value_interaction}

    return p_values


def n_way_anova(ss_n, ssw, ssi, n, k_n, groups):

    degrees_of_freedom = []
    degrees_of_freedom_within = n - (reduce(operator.mul, k_n))
    for k in k_n:
        degree_of_freedom = k -1
        degrees_of_freedom.append(degree_of_freedom)
    k_n_minus_1 = [x - 1 for x in k_n]
    degrees_of_freedom_interaction = reduce(operator.mul, k_n_minus_1)

    msw = ssw / degrees_of_freedom_within
    ms_n = []
    for num, ss in enumerate(ss_n, start=0):
        ms = ss / degrees_of_freedom[num]
        ms_n.append(ms)
    msi = ssi / degrees_of_freedom_interaction

    f_stat_n = []
    for ms in ms_n:
        f_stat = ms / msw
        f_stat_n.append(f_stat)
    f_stat_interaction = msi / msw

    p_value_n = []
    for degree, f_stat in enumerate(f_stat_n, start=0):
        p_value = f.sf(f_stat, degrees_of_freedom[degree], degrees_of_freedom_within)
        p_value_n.append(p_value)
    p_value_interaction = f.sf(f_stat_interaction, degrees_of_freedom_interaction, degrees_of_freedom_within)

    results = []
    for group, p_value in enumerate(p_value_n):
        results.append([groups[group], p_value])
    results.append(['interaction', p_value_interaction])

    return results


def n_way_anova_for_df(df, dictionary_with_groups, numerical_column):

    var_n = []
    for i, key in enumerate(list(dictionary_with_groups.keys()), start=0):
        var = list(dictionary_with_groups.keys())[i]
        var_n.append(var)

    group_names = var_n

    df_for_n_way_anova = df[var_n + [numerical_column]]

    group_of_interests_n = []
    for var in var_n:
        group_of_interests = dictionary_with_groups[var]
        group_of_interests_n.append(group_of_interests)

    df_n = []
    for group, var in enumerate(var_n, start=0):
        df = df_for_n_way_anova[df_for_n_way_anova[var].isin(group_of_interests_n[group])]
        df_n.append(df)

    k_n = []
    for n, group in enumerate(group_of_interests_n, start=0):
        k = len(group_of_interests_n[n])
        k_n.append(k)

    # print(f"K: {k_n}")

    grand_mean = df_for_n_way_anova[numerical_column].mean()

    ss_n = []
    for i in range(len(group_of_interests_n)):
        ss_nn = 0
        for group in group_of_interests_n[i]:
            df_group = df_n[i][df_n[i][var_n[i]] == group][numerical_column]
            df_group_mean = df_group.mean()
            ss_nn += ((df_group_mean - grand_mean) ** 2)
        ss_n.append(ss_nn)

    ssw = 0
    combinations = list(itertools.product(*group_of_interests_n))

    for combination in combinations:
        masks = [df_for_n_way_anova[var] == level for var, level in zip(var_n, combination)]
        combined_mask = masks[0]
        for mask in masks[1:]:
            combined_mask &= mask
        df_group = df_for_n_way_anova[combined_mask][numerical_column]
        group_mean = df_group.mean()
        for row in df_group:
            ssw += ((row - group_mean) ** 2)

    sst = 0
    for group_of_interest, var in zip(group_of_interests_n, var_n):
        for level in group_of_interest:
            df_group = df_for_n_way_anova[df_for_n_way_anova[var] == level][numerical_column]
            for row in df_group:
                sst += ((row - grand_mean) ** 2)

    ssi = sst - sum([(-1)*ss for ss in ss_n]) - ssw

    n = len(df_for_n_way_anova)

    p_values = n_way_anova(ss_n=ss_n, ssw=ssw, ssi=ssi, n=n, k_n=k_n, groups=group_names)

    return p_values
