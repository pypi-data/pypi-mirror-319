"""
Module containing the SERRF class and a function to perform cross-validation.

The SERRF class is a scikit-learn-like implementation of the SERRF algorithm.

The SERRF class is a transformer that normalizes sample data using the SERRF
algorithm. The input is a pandas DataFrame, and the output is a pandas DataFrame
with the same shape as the input, but with the samples normalized using the
SERRF algorithm.

The cross_validate function performs N-fold stratified cross validation on the 
QC samples and returns the coefficient of variation over the N folds for each metabolite
"""

from multiprocessing import Pool
from sklearn.utils.validation import check_is_fitted
from sklearn.model_selection import StratifiedKFold
import pandas as pd
import numpy as np
from tqdm import tqdm
from scipy.stats import variation
from pyserrf import utils


class SERRF:
    """
    This class implements the SERRF (Systematical Error Removal using Random Forest) method,
    which is a qc-based sample normalization method designed for large-scale
    untargeted metabolomics data.
    data. The method was developed by the Fan et al. in 2015 [1]_
    (see https://slfan2013.github.io/SERRF-online/).

    The class takes as input a pandas DataFrame containing metabolomic data and
    sample metadata, and outputs a pandas DataFrame with the normalized data.

    Parameters
    ----------
    sample_type_column : str, optional
        The name of the column in the sample metadata with the sample type
        information (i.e qc or normal sample). The default value is
        'sampleType'.
    batch_column : str, optional
        The name of the column in the sample metadata with the batch
        information. If None, all samples are considered as part the same
        batch. The default value is 'batch'.
    time_column: str, optional
        The name of the column in the sample metadata with the injection time
        information.The default value is 'time'.
    other_columns : list of str or None, optional
        A list with the names of other metadata columns in the dataset; it is
        important to specify all the metadata columns to separate them from
        the metabolite abundance values. The default value is None
    random_state : int, RandomState instance, or None, optional
        The random seed used for all methods with a random component (i.e
        numpy normal distribution, sklearn random forest regressor). The
        default value is None, which means that a random seed is generated
        automatically. To obtain reproducible results, set a specific random
        seed.
    n_correlated_metabolites : int, optional
        The number of metabolites with the highest correlation to the
        metabolite to be normalized. The default value is 10.
    threads: int, optional
        Number of threads to use for parallel processing
    References
    ----------
    .. [1] Fan et al.:
        Systematic Error Removal using Random Forest (SERRF) for Normalizing
        Large-Scale Untargeted Lipidomics Data
        Analytical Chemistry DOI: 10.1021/acs.analchem.8b05592
        https://slfan2013.github.io/SERRF-online/
    """

    def __init__(
        self,
        sample_type_column="sampleType",
        batch_column="batch",
        time_column="time",
        other_columns=None,
        n_correlated_metabolites=10,
        random_state=None,
        threads=1,
    ):
        """
        Initialize the class.
        """
        # attributes for the preprocessing
        self.sample_type_column = sample_type_column
        self.batch_column = batch_column
        self.time_column = time_column
        self.other_columns = other_columns
        # attributes for the analysis
        self.random_state = random_state
        self.threads = threads
        self.n_correlated_metabolites = n_correlated_metabolites
        # internal class attributes obtained from preprocessing
        self._metabolite_dict = None
        self._metabolite_ids = None
        self._metabolite_names = None
        self._dataset = None
        self._sample_metadata = None
        self.normalized_data = None
        self.normalized_dataset = None
        self.n_features_ = None
        self.qc_dataset = None
        self.target_dataset = None

    def fit(self, X):
        """
        Fit the transformer on the data X and returns self.

        Parameters
        ----------
        X : pandas DataFrame of shape (n_samples, n_features)
            The input dataset.

        Returns
        -------
        self

        """

        return self._fit(X)

    def transform(self, X, return_data_only=False):
        """
        Apply the SERRF normalization to the data X.

        Parameters
        ----------
        X : pandas DataFrame of shape (n_samples, n_features)
            The input data.

        Returns
        -------
        X_transformed : pandas DataFrame of shape (n_samples, n_features)
            The transformed data.

        """
        check_is_fitted(self, "n_features_")

        return self._transform(X, return_data_only=return_data_only)

    def fit_transform(self, X, return_data_only=False):
        """
        Fit the transformer on the data X and returns the transformed data.

        Parameters
        ----------
        X : pandas DataFrame of shape (n_samples, n_features)
            The input dataset.
        y : None
            There is no need of a target in a transformer, yet the pipeline API
            requires this parameter.
        return_data_only : bool, default=False
            If True, the transformed data is returned, else the transformed
            dataset with the sample metadata is returned.

        Returns
        -------
        X_transformed : pandas DataFrame of shape (n_samples, n_features)
            The transformed data.

        """
        self._fit(X)
        return self._transform(X, return_data_only=return_data_only)

    def _fit(self, dataset):
        if self.batch_column is None:
            dataset["batch"] = 1
            self.batch_column = "batch"

        metadata_columns = [
            self.sample_type_column,
            self.batch_column,
            self.time_column,
        ]
        if self.other_columns:
            metadata_columns.extend(self.other_columns)

        dataset[self.sample_type_column] = dataset[self.sample_type_column].str.lower()
        self._sample_metadata = dataset[metadata_columns]
        data = dataset.drop(columns=metadata_columns)
        data = data.astype(float)

        # Create new column names with prefix 'MET_'
        metabolite_ids = [f"MET_{i}" for i in range(1, len(data.columns) + 1)]

        # Store the mapping between the new and old column names
        self._metabolite_dict = dict(zip(metabolite_ids, data.columns))
        self._metabolite_names = list(data.columns)
        self._metabolite_ids = metabolite_ids

        # Rename the columns
        data.columns = self._metabolite_ids

        self.n_features_ = len(self._metabolite_ids)
        # Concatenate the metadata and data to form the preprocessed dataset
        self._dataset = pd.concat([self._sample_metadata, data], axis=1)
        if self.time_column is not None:
            self._dataset = self._dataset.sort_values(by=self.time_column)
        self.qc_dataset = self._dataset[self._dataset[self.sample_type_column] == "qc"]
        self.target_dataset = self._dataset[
            self._dataset[self.sample_type_column] != "qc"
        ]

    def _transform(self, X, return_data_only):
        """
        Apply the transformation on the data X.

        Parameters
        ----------
        X : pandas DataFrame of shape (n_samples, n_features)
            The input dataset.
        return_data_only : bool, default=False
            If True, the transformed data is returned, else the transformed
            dataset with the sample metadata is returned.

        Returns
        -------
        X_transformed : pandas DataFrame of shape (n_samples, n_features) or
            pandas DataFrame of shape (n_samples, n_features + n_sample_metadata_columns)
            The transformed data or the transformed dataset with the sample
            metadata.

        """

        with Pool(
            processes=self.threads,
        ) as p:
            normalized_metabolites = list(
                tqdm(
                    p.imap(self._normalize_metabolite, self._metabolite_ids),
                    total=len(self._metabolite_ids),
                )
            )
        self.normalized_data = pd.concat(normalized_metabolites, axis=1)
        self.normalized_data.columns = [
            self._metabolite_dict[i] for i in self.normalized_data.columns
        ]
        self.normalized_dataset = pd.concat(
            [self._sample_metadata, self.normalized_data], axis=1
        )
        if return_data_only:
            X = self.normalized_data
        else:
            X = self.normalized_dataset
        return X

    def _group_by_batch(self) -> pd.core.groupby.groupby.GroupBy:
        """
        Group the dataset by batch.

        Returns
        -------
        pd.core.groupby.groupby.GroupBy
            The grouped data.
        """
        return self._dataset.groupby(by=self.batch_column)

    def _split_by_sample_type(
        self, group: pd.DataFrame
    ) -> (pd.DataFrame, pd.DataFrame):
        """
        Split the given group by sample type.

        Parameters
        ----------
        group : pd.DataFrame
            The data for a single batch.

        Returns
        -------
        pd.DataFrame
            The data for the qc samples in the given batch.
        pd.DataFrame
            The data for the target samples in the given batch.

        """
        qc = group[group[self.sample_type_column] == "qc"]
        target = group[group[self.sample_type_column] != "qc"]
        return qc, target

    def _get_corrs_by_sample_type_and_batch(self):
        """
        Get the Spearman's correlations between metabolites grouped by sample type and batch.

        Returns
        -------
        corrs_qc : dict
            The correlations for the qc data, keyed by batch.
        corrs_target : dict
            The correlations for the target data, keyed by batch.
        """
        corrs_qc = {}
        corrs_target = {}

        for batch, group in self._group_by_batch():
            # Get the qc and target data for this batch
            qc_group, target_group = self._split_by_sample_type(group)
            qc_group = group[group[self.sample_type_column] == "qc"]
            qc_group_scaled = utils.standard_scaler(qc_group[self._metabolite_ids])

            # Calculate the correlations for this batch
            corrs_qc[batch] = qc_group_scaled.corr(method="spearman")
            if len(target_group) == 0:
                # If there is no target data for this batch, set the
                # correlation to NaN
                corrs_target[batch] = np.nan
            else:
                target_group_scaled = utils.standard_scaler(
                    target_group[self._metabolite_ids]
                )
                corrs_target[batch] = target_group_scaled.corr(method="spearman")
        return corrs_qc, corrs_target

    def _normalize_qc_with_prediction(self, metabolite, group, prediction):
        """
        Normalize the qc data for the given metabolite using the given prediction.

        The normalization formula is:

        norm_qc = qc_data / ((qc_prediction + qc_data.mean())
                            / qc_dataset.mean())
        norm_qc = norm_qc / (norm_qc.median() / qc_dataset.median())

        The normalization is done by dividing the qc data by the ratio of the
        qc prediction and the mean of the qc dataset.  The result is then divided by the
        ratio of the median of the normalized qc data and the median of the
        qc dataset.

        Parameters
        ----------
        metabolite : str
            The name of the metabolite to normalize.
        group : pandas.DataFrame
            The qc data for the given metabolite.
        prediction : pandas.DataFrame
            The prediction for the given metabolite.

        Returns
        -------
        norm_qc : pandas.DataFrame
            The normalized qc data.
        """
        norm_qc = group[metabolite] / (
            (prediction + group[metabolite].mean()) / self.qc_dataset[metabolite].mean()
        )
        norm_qc = norm_qc / (norm_qc.median() / self.qc_dataset[metabolite].median())

        return norm_qc

    def _normalize_target_with_prediction(self, metabolite, group, prediction):
        """
        Normalize the target data for the given metabolite using the given prediction.

        The normalization formula is:

        norm_target = target_data / ((prediction + target_data.mean() - prediction.mean())
                                    / target_dataset.median())
        norm_target = norm_target / (norm_target.median() / target_dataset.median())

        The normalization is done by dividing the target data by the ratio of the
        prediction and the median of the target dataset.  The result is then
        divided by the ratio of the median of the normalized target data and the
        median of the target dataset.

        Parameters
        ----------
        metabolite : str
            The name of the metabolite to normalize.
        group : pandas.DataFrame
            The target data for the given metabolite.
        prediction : pandas.DataFrame
            The prediction for the given metabolite.

        Returns
        -------
        norm_target : pandas.DataFrame
            The normalized target data.
        """
        norm_target = group[metabolite] / (
            (prediction + group[metabolite].mean() - prediction.mean())
            / self.target_dataset[metabolite].median()
        )
        # Set negative values to the original value
        norm_target[norm_target < 0] = group[metabolite].loc[
            norm_target[norm_target < 0].index
        ]
        norm_target = norm_target / (
            norm_target.median() / self.target_dataset[metabolite].median()
        )
        return norm_target

    def _merge_and_normalize(
        self, metabolite, norm_qc, norm_target, target_group, target_prediction
    ):
        """
        TODO: function could probably be simpler, refactor and maybe split

        Merges the qc and target data and replaces outliers in the target data.

        Parameters
        ----------
        metabolite : str
            The name of the metabolite to normalize.
        norm_qc : pandas Series
            The normalized qc data.
        norm_target : pandas Series
            The normalized target data.
        target_group : pandas DataFrame
            The target data group.
        target_prediction : pandas Series
            The predicted values for the target data.

        Returns
        -------
        norm : pandas Series
            The normalized data.
        """
        norm = pd.concat([norm_qc, norm_target]).sort_index()
        outliers = utils.detect_outliers(data=norm, threshold=3)
        outliers = outliers[outliers]
        outliers_in_target = outliers.index.intersection(norm_target.index)

        # Replace outlier values in the target data with the mean of the outlier
        # values in the target data minus the mean of the predicted values for the
        # target data

        replaced_outliers = (
            target_group[metabolite]
            - (
                (target_prediction + target_group[metabolite].mean())
                - (self.target_dataset[metabolite].median())
            )
        ).loc[outliers_in_target]

        norm_target.loc[outliers_in_target] = replaced_outliers

        # Set negative values to the original value
        if len(norm_target[norm_target < 0]) > 0:
            norm_target[norm_target < 0] = target_group.loc[
                norm_target[norm_target < 0].index
            ][metabolite]

        norm = pd.concat([norm_qc, norm_target]).sort_index()
        # MANCA FUNZIONE PER RIMPIAZZARE INF O NAN - ORIGINALE QUA SOTTO:
        # norm[!is.finite(norm)] =
        # rnorm(length(norm[!is.finite(norm)]), sd = sd(norm[is.finite(norm)], na.rm = TRUE) * 0.01)

        return norm

    def _normalize_metabolite(self, metabolite):
        """
        Normalizes the given metabolite
        Parameters
        ----------
        metabolite : str
            The name of the metabolite to normalize.

        Returns
        -------
        normalized : pandas Series
            The normalized data.
        """
        corrs_qc, corrs_target = self._get_corrs_by_sample_type_and_batch()

        normalized_metabolite = []
        for batch, group in self._group_by_batch():
            # Get the groups for the qc and target data
            qc_group, target_group = self._split_by_sample_type(group)

            # Get the order of correlation for the qc and target data
            corr_qc_order = utils.get_sorted_correlation(corrs_qc[batch], metabolite)
            corr_target_order = utils.get_sorted_correlation(
                corrs_target[batch], metabolite
            )

            # Get the top correlated metabolites from both data sets
            top_correlated = utils.get_top_values_in_both_correlations(
                corr_target_order, corr_qc_order, self.n_correlated_metabolites
            )
            # this is to avoid different order of same 10 metabolites
            # which in turn gives different RF results

            top_correlated = list(top_correlated)
            # Scale the data
            target_data_x = utils.scale_columns(target_group, top_correlated)
            qc_data_x = utils.scale_columns(qc_group, top_correlated)
            # Get the target values for the qc data
            # qc_data_y = self._get_qc_data_y(qc_group, target_group, metabolite) #outdated function
            qc_data_y = utils.center_data(qc_group[metabolite])

            # If there is no QC data, just return the original data
            if qc_data_x.empty:
                norm = group[metabolite]

            # Otherwise, predict and normalize the data
            else:
                qc_prediction, target_prediction = utils.predict_values(
                    qc_data_x, qc_data_y, target_data_x, random_state=self.random_state
                )
                norm_qc = self._normalize_qc_with_prediction(
                    metabolite, qc_group, qc_prediction
                )
                norm_target = self._normalize_target_with_prediction(
                    metabolite, target_group, target_prediction
                )
                norm = self._merge_and_normalize(
                    metabolite, norm_qc, norm_target, target_group, target_prediction
                )

            normalized_metabolite.append(norm)

        normalized_metabolite = pd.concat(normalized_metabolite)
        return normalized_metabolite


def cross_validate(
    dataset,
    n_splits=5,
    sample_type_column="sampleType",
    batch_column="batch",
    time_column="time",
    other_columns=None,
    n_correlated_metabolites=10,
    random_state=None,
    threads=1,
):
    """Perform cross-validation of the SERRF algorithm using the QC samples

    Parameters
    ----------
    dataset : Pandas DataFrame
        The SERRF-compatible dataset.
    n_splits : int, optional
        The number of CV folds to use, by default 5
    sample_type_column : str, optional
        The name of the column in the dataset that contains the sample type
        information, by default "sampleType"
    batch_column : str, optional
        The name of the column in the dataset that contains the batch
        information, by default "batch"
    time_column : str, optional
        The name of the column in the dataset that contains the injection time
        information, by default "time"
    other_columns : list, optional
        A list of additional metadata columns to exclude from the data, by default None
    n_correlated_metabolites : int, optional
        The number of correlated metabolites to use for the normalization, by default 10
    random_state : int, optional
        The random state, by default None
    threads : int, optional
        The number of threads, by default 1

    Returns
    -------
    raw_variation : Pandas DataFrame
        The coefficient of variation of each metabolite in the raw data
    normalized_variation : Pandas DataFrame
        The coefficient of variation of the normalized data
    """
    raw_variations = []
    normalized_variations = []
    # Filter out QC samples
    dataset = dataset[dataset[sample_type_column] == "qc"]
    dataset = dataset.reset_index(drop=True)
    # Add a batch column if it is None
    if batch_column is None:
        dataset["batch"] = 1
        batch_column = "batch"
    # Get the batch labels
    y = dataset[batch_column]
    # Create a StratifiedKFold object
    skf = StratifiedKFold(n_splits=n_splits, shuffle=False)
    # Perform CV
    for i, (train_index, test_index) in enumerate(skf.split(dataset, y)):
        print(f"CV {i}/{n_splits}")
        # Create training and target dataframes
        temp_qc = dataset.loc[train_index]
        temp_target = dataset.loc[test_index]
        # Change the target type to "sample"
        temp_target[sample_type_column] = "sample"
        # Concatenate the two dataframes
        tempdf = pd.concat([temp_qc, temp_target])
        # Sort the data by time if time_column is not None
        if time_column is not None:
            tempdf = tempdf.sort_values(by=time_column)
        # Create a SERRF object
        tempserrf = SERRF(
            sample_type_column=sample_type_column,
            batch_column=batch_column,
            time_column=time_column,
            other_columns=other_columns,
            random_state=random_state,
            n_correlated_metabolites=n_correlated_metabolites,
            threads=threads,
        )
        # Fit and transform the data
        normalized = tempserrf.fit_transform(tempdf)
        # Select the normalized target samples
        normalized_target = normalized[normalized["sampleType"] == "sample"]
        # Select the raw target samples
        raw_target = temp_target
        # Compute the RSD of the raw target samples
        raw_target_variation = raw_target[tempserrf.normalized_data.columns].apply(
            variation
        )
        # Compute the RSD of the normalized target samples
        normalized_target_variation = normalized_target[
            tempserrf.normalized_data.columns
        ].apply(variation)
        # Add the index to the RSD DataFrame
        raw_target_variation.name = f"{i}"
        normalized_target_variation.name = f"{i}"
        # Append the RSD data to the list
        raw_variations.append(raw_target_variation)
        normalized_variations.append(normalized_target_variation)
    # Concatenate the RSD dataframes
    raw_variations = pd.concat(raw_variations, axis=1)
    normalized_variations = pd.concat(normalized_variations, axis=1)
    return raw_variations, normalized_variations
