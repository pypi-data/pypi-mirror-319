from typing import Union
import pandas as pd
import polars as pl

from groupcorr.exceptions import PerfectMappingError


def check_perfect_match(df, feature_set, target):
    """
    Asserts that no feature in the feature set has a perfect mapping with the target.

    Parameters:
    - df (pd.DataFrame): The dataframe containing the features and target.
    - feature_set (list): List of feature column names to check.
    - target (str): The name of the target column.

    Raises:
    - PerfectMappingError: If any feature has a perfect mapping with the target, listing the features.

    Returns:
    - None
    """
    matching_features = []

    for feature in feature_set:
        # Check if the feature has a bijective mapping with the target
        feature_to_target = df.groupby(feature)[target].nunique()
        target_to_feature = df.groupby(target)[feature].nunique()
        
        if feature_to_target.max() == 1 and target_to_feature.max() == 1:
            matching_features.append(feature)

    # Raise custom exception if any matching features are found
    if matching_features:
        raise PerfectMappingError(
            f"The following features have a perfect 1-to-1 mapping with the target: {matching_features}"
        )


def calculate_group_corr(df, feature_set, target, group_column):
    if isinstance(df, pd.DataFrame):
        corr_df = pl.from_pandas(df)
    agg_cols = [pl.corr(feature_col, target, method="spearman") for feature_col in feature_set]
    
    return corr_df.group_by(group_column).agg(agg_cols).to_pandas()


def plot_importance(df):
    df.reset_index().rename(columns={"index":"feature"}).sort_values("importance").plot(x="feature", y="importance", xerr="std", kind='barh')