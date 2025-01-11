from typing import Union
from polars import DataFrame as pl_df
from pandas import DataFrame as pd_df

from groupcorr.utils import calculate_group_corr
from groupcorr.utils import check_perfect_match
from groupcorr.utils import plot_importance


class GroupCorr:
    def __init__(self, df : Union[pd_df, pl_df], feature_set, target, group_col):
        #check_perfect_match(df, feature_set, target)
        self.feature_set = list(feature_set)
        self.target = target
        self.corr_df = calculate_group_corr(df, feature_set, target, group_col)
        self.eps = 1e-10
        self.importance_df = None

    def group_correlations(self):
        return self.corr_df
    
    def get_importances(self):
        df = self.corr_df[self.feature_set].describe().loc[["mean","std"]].T.reset_index()
        df["importance"] = df["mean"].abs() / (df["std"]+self.eps)
        self.importance_df = df.sort_values("importance", ascending=False, ignore_index=True)
        return self.importance_df
    
    def importance_plot(self):
        if self.importance_df is None:
            self.get_importances()
        plot_importance(self.importance_df)






