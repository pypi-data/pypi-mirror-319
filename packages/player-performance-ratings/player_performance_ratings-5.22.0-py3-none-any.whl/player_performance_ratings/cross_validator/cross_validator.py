import copy
from datetime import datetime
from typing import Optional

import narwhals as nw
from narwhals.typing import FrameT, IntoFrameT
from player_performance_ratings import ColumnNames

from player_performance_ratings.scorer.score import BaseScorer
from player_performance_ratings.transformers.base_transformer import (
    BaseTransformer,
    BaseLagGenerator,
)

from player_performance_ratings.cross_validator._base import CrossValidator
from player_performance_ratings.predictor._base import BasePredictor
from player_performance_ratings.utils import convert_pandas_to_polars, validate_sorting


class MatchKFoldCrossValidator(CrossValidator):
    """
    Performs cross-validation by splitting the data into n_splits based on match_ids.
    """

    def __init__(
        self,
        match_id_column_name: str,
        date_column_name: str,
        predictor: BasePredictor,
        scorer: Optional[BaseScorer] = None,
        min_validation_date: Optional[str] = None,
        n_splits: int = 3,
    ):
        """
        :param match_id_column_name: The column name of the match_id
        :param date_column_name: The column name of the date
        :param scorer: The scorer to use for measuring the accuracy of the predictions on the validation dataset
        :param min_validation_date: The minimum date for which the cross-validation should start
        :param n_splits: The number of splits to perform
        """
        super().__init__(
            scorer=scorer, min_validation_date=min_validation_date, predictor=predictor
        )
        self.match_id_column_name = match_id_column_name
        self.date_column_name = date_column_name
        self.n_splits = n_splits
        self.min_validation_date = min_validation_date

    @nw.narwhalify
    def generate_validation_df(
        self,
        df: FrameT,
        column_names: ColumnNames,
        return_features: bool = False,
        add_train_prediction: bool = True,
    ) -> IntoFrameT:
        """
        Generate predictions on validation dataset.
        Training is performed N times on previous match_ids and predictions are made on match_ids that take place in the future.
        :param df: The dataframe to generate the validation dataset from
        :param predictor: The predictor to use for generating the predictions
        :param column_names: The column names to use for the match_id, team_id, and player_id
        :param estimator_features: The features to use for the estimator. If passed in, it will override the estimator_features in the predictor
        :param pre_lag_transformers: The transformers to use before the lag generators
        :param lag_generators: The lag generators to use
        :param post_lag_transformers: The transformers to use after the lag generators
        :param return_features: Whether to return the features generated by the generators and the lags. If false it will only return the original columns and the predictions
        :param add_train_prediction: Whether to also calculate and return predictions for the training dataset.
            This can be beneficial for 2 purposes:
            1. To see how well the model is fitting the training data
            2. If the output of the predictions is used as input for another model

            If set to false it will only return the predictions for the validation dataset
        """

        if "__row_index" in df.columns:
            df = df.drop("__row_index")

        if self.validation_column_name in df.columns:
            df = df.drop(self.validation_column_name)

        predictor = copy.deepcopy(self.predictor)
        validation_dfs = []
        ori_cols = df.columns

        if not self.min_validation_date:
            unique_dates = df[self.date_column_name].unique(maintain_order=True)
            median_number = len(unique_dates) // 2
            self.min_validation_date = unique_dates[median_number]

        df = df.with_columns(
            (
                nw.col(self.match_id_column_name)
                != nw.col(self.match_id_column_name).shift(1)
            )
            .cum_sum()
            .fill_null(0)
            .alias("__cv_match_number")
        )
        if df["__cv_match_number"].min() == 0:
            df = df.with_columns(nw.col("__cv_match_number") + 1)

        if isinstance(self.min_validation_date, str) and df.schema.get(
            self.date_column_name
        ) in (nw.Date, nw.Datetime):
            min_validation_date = datetime.strptime(
                self.min_validation_date, "%Y-%m-%d"
            )
        else:
            min_validation_date = self.min_validation_date

        min_validation_match_number = (
            df.filter(nw.col(self.date_column_name) >= nw.lit(min_validation_date))
            .select(nw.col("__cv_match_number").min())
            .head(1)
            .item()
        )

        max_match_number = df.select(nw.col("__cv_match_number").max()).to_numpy()[0][0]
        train_cut_off_match_number = min_validation_match_number
        step_matches = (max_match_number - min_validation_match_number) / self.n_splits

        train_df = df.filter(nw.col("__cv_match_number") < train_cut_off_match_number)
        if len(train_df) == 0:
            raise ValueError(
                f"train_df is empty. train_cut_off_day_number: {train_cut_off_match_number}. Select a lower validation_match value."
            )



        validation_df = df.filter(
            (nw.col("__cv_match_number") >= train_cut_off_match_number)
            & (nw.col("__cv_match_number") <= train_cut_off_match_number + step_matches)
        )

        for idx in range(self.n_splits):

            predictor.train(train_df)

            if idx == 0 and add_train_prediction:
                columns_to_keep = [
                    c for c in train_df.columns if c not in predictor.columns_added
                ]
                train_df = train_df.select(columns_to_keep)
                train_df = nw.from_native(
                    predictor.predict(train_df, cross_validation=True)
                )
                train_df = train_df.with_columns(
                    nw.lit(0).alias(self.validation_column_name)
                )
                validation_dfs.append(train_df)

            columns_to_keep = [
                c for c in validation_df.columns if c not in predictor.columns_added
            ]
            validation_df = validation_df.select(columns_to_keep)
            validation_df = nw.from_native(
                predictor.predict(validation_df, cross_validation=True)
            )
            validation_df = validation_df.with_columns(
                nw.lit(1).alias(self.validation_column_name)
            )
            if validation_dfs:
                validation_dfs.append(validation_df.select(validation_dfs[0].columns))
            else:
                validation_dfs.append(validation_df)

            train_cut_off_match_number += step_matches
            train_df = df.filter(
                nw.col("__cv_match_number") < train_cut_off_match_number
            )

            if idx == self.n_splits - 2:
                validation_df = df.filter(
                    nw.col("__cv_match_number") >= train_cut_off_match_number
                )
            else:
                validation_df = df.filter(
                    (nw.col("__cv_match_number") >= train_cut_off_match_number)
                    & (
                        nw.col("__cv_match_number")
                        < train_cut_off_match_number + step_matches
                    )
                )

        concat_validation_df = nw.concat(validation_dfs).drop("__cv_match_number")

        if not return_features:
            concat_validation_df = concat_validation_df.select(
                [*ori_cols, *predictor.columns_added, self.validation_column_name]
            )

        concat_validation_df = concat_validation_df.unique(
            subset=[
                column_names.match_id,
                column_names.team_id,
                column_names.player_id,
            ],
            keep="first",
            maintain_order=True,
        )
        validate_sorting(df=concat_validation_df, column_names=column_names)
        return concat_validation_df
