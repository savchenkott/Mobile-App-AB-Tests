import itertools
from scipy.stats import norm, shapiro, t, f, chi2
import numpy as np
import math
from functools import reduce
import operator


def z_test(x, mean, stdev, right_tailed=True):
    """
    Calculates the p-value for a given z-score.
    H0: the observed value x is not significantly different from the population mean.

    :param x: float, The observed value
    :param mean: float, The mean of the population
    :param stdev: float, The standard deviation of the population
    :param right_tailed: bool, optional, If True, performs a right-tailed test. If False, performs a left-tailed test. Defaults to True.
    :return: float, The calculated p-value
    """

    z_score = (x-mean)/stdev
    if right_tailed == True:
        p_value = (1-norm.cdf(z_score))
    elif right_tailed == False:
        p_value = (norm.cdf(z_score))
    else:
        raise ValueError("right_tailed must be True or False")
    return p_value


def z_test_for_df(point, df, column, right_tailed=True):
    """
    Calculates the p-value for a given point from a dataframe column using the z-test.
    H0: the observed value x is not significantly different from the population mean.

    :param point: float, The observed value
    :param df: pandas.DataFrame, The dataframe containing the data
    :param column: str, The column in the dataframe to perform the test on
    :param right_tailed: bool, optional, If True, performs a right-tailed test. If False, performs a left-tailed test. Defaults to True.
    :return: float, The calculated p-value
    """

    mean = df[column].mean()
    stdev = df[column].std()
    normality = shapiro(df[column])[1]

    if normality <= 0.05:
        p_value = z_test(x=point, mean=mean, stdev=stdev, right_tailed=right_tailed)
    else:
        print(f"Data not normally distributed. Shapiro-Wilk test p-value is {normality}")
        p_value = z_test(x=point, mean=mean, stdev=stdev, right_tailed=right_tailed)

    return p_value


def unpaired_t_test(x1, x2, std1, std2, n1, n2, tail='two'):
    """
    Calculates the p-value for an unpaired t-test.
    H0: the mean of the first sample x1 is not significantly different from the mean of the second sample x2.

    :param x1: float, The mean of the first sample
    :param x2: float, The mean of the second sample
    :param std1: float, The standard deviation of the first sample
    :param std2: float, The standard deviation of the second sample
    :param n1: int, The size of the first sample
    :param n2: int, The size of the second sample
    :param tail: str, optional, The type of test to perform. Must be 'right', 'left', or 'two'. Defaults to 'two'.
    :return: float, The calculated p-value
    """

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
    """
    Calculates the p-value for an unpaired t-test for a given point from a dataframe column.
    H0: The mean of the first sample x1 is not significantly different from the mean of the second sample x2.

    :param df: pandas.DataFrame, The dataframe containing the data
    :param category_column: str, The column in the dataframe to group by
    :param group1: str, The first group to compare
    :param group2: str, The second group to compare
    :param numerical_column: str, The column in the dataframe to perform the test on
    :param tail: str, optional, The type of test to perform. Must be 'right', 'left', or 'two'. Defaults to 'two'.
    :return: float, The calculated p-value
    """

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
    """
    Calculates the p-value for a paired t-test.
    H0: the mean of the differences differences_mean is not significantly different from zero.

    :param differences_mean: float, The mean of the differences
    :param differences_stdev: float, The standard deviation of the differences
    :param n: int, The number of differences
    :param tail: str, optional, The type of test to perform. Must be 'right', 'left', or 'two'. Defaults to 'two'.
    :return: float, The calculated p-value
    """

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
    """
    Calculates the p-value for a paired t-test for a given point from a dataframe column.
    H0: the mean of the differences is not significantly different from zero.

    :param df: pandas.DataFrame, The dataframe containing the data
    :param id_column: str, The column in the dataframe to identify unique entities
    :param period_column: str, The column in the dataframe to identify the periods
    :param period1: str, The first period to compare
    :param period2: str, The second period to compare
    :param numerical_column: str, The column in the dataframe to perform the test on
    :param tail: str, optional, The type of test to perform. Must be 'right', 'left', or 'two'. Defaults to 'two'.
    :return: float, The calculated p-value
    """

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
    """
    Calculates the p-value for a one-way ANOVA test.
    H0: all group means are equal.

    :param sst: float, The total sum of squares
    :param ssw: float, The sum of squares within groups
    :param n: int, The total number of observations
    :param k: int, The number of groups
    :return: float, The calculated p-value
    """

    ssb = sst - ssw
    degrees_of_freedom_within = n - k
    degrees_of_freedom_between = k - 1

    msw = ssw / degrees_of_freedom_within
    msb = ssb / degrees_of_freedom_between
    f_stat = msb / msw

    p_value = f.sf(f_stat, degrees_of_freedom_between, degrees_of_freedom_within)

    return p_value


def one_way_anova_for_df(df, category_column, group_of_interest, numerical_column):
    """
    Calculates the p-value for a one-way ANOVA test for a given point from a dataframe column.
    H0: all group means are equal.

    :param df: pandas.DataFrame, The dataframe containing the data
    :param category_column: str, The column in the dataframe to group by
    :param group_of_interest: list, The groups to compare
    :param numerical_column: str, The column in the dataframe to perform the test on
    :return: float, The calculated p-value
    """

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
    """
    Calculates the p-values for a two-way ANOVA test.
    H0 for the first factor: All group means are equal at each level of the first factor.
    H0 for the second factor: All group means are equal at each level of the second factor.
    H0 for the interaction effect: There is no interaction effect between the two factors.

    :param ssa: float, The sum of squares for the first factor
    :param ssb: float, The sum of squares for the second factor
    :param ssw: float, The sum of squares within groups
    :param ssi: float, The sum of squares for the interaction
    :param n: int, The total number of observations
    :param k_a: int, The number of levels for the first factor
    :param k_b: int, The number of levels for the second factor
    :return: tuple, The calculated p-values for the first factor, the second factor, and the interaction
    """

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
    """
    Calculates the p-values for a two-way ANOVA test for a given point from a dataframe column.
    H0 for the first factor: All group means are equal at each level of the first factor.
    H0 for the second factor: All group means are equal at each level of the second factor.
    H0 for the interaction effect: There is no interaction effect between the two factors.

    :param df: pandas.DataFrame, The dataframe containing the data
    :param dictionary_with_groups: dict, The dictionary with the two factors and their levels
    :param numerical_column: str, The column in the dataframe to perform the test on
    :return: dict, The calculated p-values for the first factor, the second factor, and the interaction
    """

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
    """
    Calculates the p-values for an n-way ANOVA test.
    H0 for each factor: All group means are equal at each level of each factor.
    H0 for the interaction effect: There is no interaction effect among the factors.

    :param ss_n: list, The sum of squares for each factor
    :param ssw: float, The sum of squares within groups
    :param ssi: float, The sum of squares for the interaction
    :param n: int, The total number of observations
    :param k_n: list, The number of levels for each factor
    :param groups: list, The names of the groups
    :return: list, The calculated p-values for each factor and the interaction
    """

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
    """
    Calculates the p-values for an n-way ANOVA test for a given point from a dataframe column.
    H0 for each factor: All group means are equal at each level of each factor.
    H0 for the interaction effect: There is no interaction effect among the factors.

    :param df: pandas.DataFrame, The dataframe containing the data
    :param dictionary_with_groups: dict, The dictionary with the factors and their levels
    :param numerical_column: str, The column in the dataframe to perform the test on
    :return: list, The calculated p-values for each factor and the interaction
    """

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


def one_sample_proportion_test(sample_proportion, h0_proportion, n, tail='two'):
    """
    Calculates the p-value for a one-sample proportion test.
    H0: the sample proportion is not significantly different from the hypothesized proportion h0_proportion.

    :param sample_proportion: float, The proportion of the sample
    :param h0_proportion: float, The null hypothesis proportion
    :param n: int, The total number of observations
    :param tail: str, optional, The type of test to perform. Must be 'right', 'left', or 'two'. Defaults to 'two'.
    :return: float, The calculated p-value
    """

    z_numerator = (sample_proportion - h0_proportion)
    z_denominator = math.sqrt((h0_proportion*(1-h0_proportion))/n)
    
    z_score = z_numerator / z_denominator
    if tail == 'right':
        p_value = 1 - norm.cdf(z_score)
    elif tail == 'left':
        p_value = norm.cdf(z_score)
    elif tail == 'two':
        if z_score > 0:
            p_value = 2 * (1 - norm.cdf(z_score))
        else:
            p_value = 2 * norm.cdf(z_score)
    else:
        raise ValueError("tail must be 'right', 'left', or 'two'")

    return p_value


def one_sample_proportion_test_for_df(df, categorical_column, value, h0_proportion, tail='two'):
    """
    Calculates the p-value for a one-sample proportion test for a given point from a dataframe column.
    H0: the sample proportion is not significantly different from the hypothesized proportion h0_proportion

    :param df: pandas.DataFrame, The dataframe containing the data
    :param categorical_column: str, The column in the dataframe to perform the test on
    :param value: str, The value in the categorical column to test
    :param h0_proportion: float, The null hypothesis proportion
    :param tail: str, optional, The type of test to perform. Must be 'right', 'left', or 'two'. Defaults to 'two'.
    :return: float, The calculated p-value
    """

    value_occurrence = len(df[df[categorical_column] == value])
    n = len(df)
    sample_proportion = value_occurrence / n

    p_value = one_sample_proportion_test(sample_proportion=sample_proportion, h0_proportion=h0_proportion,
                                         n=n, tail=tail)
    return p_value


def two_sample_proportion_test(sample_proportion1, sample_proportion2, n1, n2, tail='two'):
    """
    Calculates the p-value for a two-sample proportion test.
    H0: the proportion of the first sample sample_proportion1 is not significantly different from the proportion of
    the second sample sample_proportion2.

    :param sample_proportion1: float, The proportion of the first sample
    :param sample_proportion2: float, The proportion of the second sample
    :param n1: int, The total number of observations in the first sample
    :param n2: int, The total number of observations in the second sample
    :param tail: str, optional, The type of test to perform. Must be 'right', 'left', or 'two'. Defaults to 'two'.
    :return: float, The calculated p-value
    """

    proportion = (sample_proportion1 + sample_proportion2) / (n1 + n2)
    z_numerator = (sample_proportion1-sample_proportion2)
    z_denominator = math.sqrt((proportion*(1-proportion))*(1/n1 + 1/n2))
    z_score = z_numerator/z_denominator

    if tail == 'right':
        p_value = 1 - norm.cdf(z_score)
    elif tail == 'left':
        p_value = norm.cdf(z_score)
    elif tail == 'two':
        p_value = 2 * (1 - (norm.cdf(abs(z_score))))
    else:
        raise ValueError("tail must be 'right', 'left', or 'two'")

    return p_value


def two_sample_proportion_test_for_df(df, categorical_column1, categorical_column2, value1, value2, tail='two'):
    """
    Calculates the p-value for a two-sample proportion test for a given point from a dataframe column.
    H0: the proportion of the first sample is not significantly different from the proportion of the second sample.

    :param df: pandas.DataFrame, The dataframe containing the data
    :param categorical_column1: str, The first column in the dataframe to perform the test on
    :param categorical_column2: str, The second column in the dataframe to perform the test on
    :param value1: str, The value in the first categorical column to test
    :param value2: str, The value in the second categorical column to test
    :param tail: str, optional, The type of test to perform. Must be 'right', 'left', or 'two'. Defaults to 'two'.
    :return: float, The calculated p-value
    """

    value1_occurrence = len(df[df[categorical_column1] == value1])
    n1 = len(df)

    value2_occurrence = len(df[df[categorical_column2] == value2])
    n2 = len(df)

    sample_proportion1 = value1_occurrence / n1
    sample_proportion2 = value2_occurrence / n2

    p_value = two_sample_proportion_test(sample_proportion1=sample_proportion1, sample_proportion2=sample_proportion2,
                                         n1=n1, n2=n2, tail=tail)

    return p_value


def chi_square_independence_test(frequencies, cell_values, n_categories, n_groups):
    """
    Calculates the p-value for a Chi-square test of independence.
    H0: the categorical variables represented by the frequencies and cell_values are independent.

    :param frequencies: list, The expected frequencies
    :param cell_values: list, The observed frequencies
    :param n_categories: int, The number of categories
    :param n_groups: int, The number of groups
    :return: float, The calculated p-value
    """

    chi2_stat = 0
    for freq, cell in zip(frequencies, cell_values):
        chi2_stat += ((cell-freq)**2)/freq

    degrees_of_freedom = (n_categories - 1) * (n_groups - 1)
    p_value = 1 - chi2.cdf(chi2_stat, df=degrees_of_freedom)

    return p_value


def chi_square_independence_test_for_df(df, group_column, category_column, value_column, value):
    """
    Calculates the p-value for a Chi-square test of independence for a given point from a dataframe column.
    H0: the categorical variables represented by the group_column and category_column in the dataframe df are independent.

    :param df: pandas.DataFrame, The dataframe containing the data
    :param group_column: str, The column in the dataframe to group by
    :param category_column: str, The column in the dataframe to categorize by
    :param value_column: str, The column in the dataframe to perform the test on
    :param value: str, The value in the value column to test
    :return: float, The calculated p-value
    """

    row_totals = []
    for group in df[group_column].unique():
        row = len(df[(df[group_column] == group) & (df[value_column] == value)])
        row_totals.append(row)

    column_totals = []
    for category in df[category_column].unique():
        column = len(df[(df[category_column] == category) & (df[value_column] == value)])
        column_totals.append(column)

    grand_total = sum(row_totals)

    frequencies = []
    cell_values = []
    for g, group in enumerate(df[group_column].unique(), start=0):
        for c, category in enumerate(df[category_column].unique(), start=0):
            value_n = len(df[(df[group_column] == group) & (df[category_column] == category) & (df[value_column] == value)])
            cell_values.append(value_n)
            freq_n = row_totals[g] * column_totals[c] / grand_total
            frequencies.append(freq_n)

    n_categories = len(df[group_column].unique())
    n_groups = len(df[category_column].unique())

    p_value = chi_square_independence_test(frequencies=frequencies, cell_values=cell_values, n_categories=n_categories, n_groups=n_groups)

    return p_value


def chi_square_goodness_of_fit_test(expected_values, observed_values):
    """
    Calculates the p-value for a Chi-square goodness of fit test.
    H0: the observed frequencies observed_values are not significantly different from the expected frequencies
    expected_values.

    :param expected_values: dict, The expected frequencies
    :param observed_values: dict, The observed frequencies
    :return: float, The calculated p-value
    """

    chi2_stat = 0
    for key in observed_values:
        obs = observed_values[key]
        exp = expected_values[key]
        chi2_stat += ((obs-exp)**2)/exp

    k = len(observed_values)
    degrees_of_freedom = k - 1

    p_value = 1 - chi2.cdf(chi2_stat, df=degrees_of_freedom)

    return p_value


def chi_square_goodness_of_fit_test_for_df(df, category_column, expected_values):
    """
    Calculates the p-value for a Chi-square goodness of fit test for a given point from a dataframe column.
    H0: the observed frequencies of each value in the category_column in the dataframe df are not significantly
    different from the expected frequencies expected_values

    :param df: pandas.DataFrame, The dataframe containing the data
    :param category_column: str, The column in the dataframe to perform the test on
    :param expected_values: dict, The expected frequencies
    :return: float, The calculated p-value
    """

    observed_values = {key: len(df[df[category_column] == key]) for key in expected_values}
    p_value = chi_square_goodness_of_fit_test(expected_values=expected_values, observed_values=observed_values)

    return p_value

