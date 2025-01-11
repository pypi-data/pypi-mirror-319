import pandas as pd
import numpy as np
import datetime as dt
from functools import partial
from collections.abc import Callable

from sklearn.utils.validation import check_is_fitted
from scipy.ndimage import gaussian_filter1d

from tide.base import BaseProcessing, BaseFiller, BaseOikoMeteo
from tide.math import time_gradient
from tide.utils import (
    get_data_blocks,
    get_outer_timestamps,
    check_and_return_dt_index_df,
    parse_request_to_col_names,
    ensure_list,
)
from tide.regressors import SkSTLForecast
from tide.classifiers import STLEDetector
from tide.meteo import sun_position, beam_component, sky_diffuse, ground_diffuse

MODEL_MAP = {"STL": SkSTLForecast}

OIKOLAB_DEFAULT_MAP = {
    "temperature": "t_ext__°C__outdoor__meteo",
    "dewpoint_temperature": "t_dp__°C__outdoor__meteo",
    "mean_sea_level_pressure": "pressure__Pa__outdoor__meteo",
    "wind_speed": "wind_speed__m/s__outdoor__meteo",
    "100m_wind_speed": "100m_wind_speed__m/s__outdoor__meteo",
    "relative_humidity": "rh__0-1RH__outdoor__meteo",
    "surface_solar_radiation": "gho__w/m²__outdoor__meteo",
    "direct_normal_solar_radiation": "dni__w/m²__outdoor__meteo",
    "surface_diffuse_solar_radiation": "dhi__w/m²__outdoor__meteo",
    "surface_thermal_radiation": "thermal_radiation__w/m²__outdoor__meteo",
    "total_cloud_cover": "total_cloud_cover__0-1cover__outdoor__meteo",
    "total_precipitation": "total_precipitation__mm__outdoor__meteo",
}


class Identity(BaseProcessing):
    """
    A custom transformer that returns the input data without any modifications.

    This transformer is useful when you want to include an identity transformation step
    in a scikit-learn pipeline, where the input data should be returned unchanged.

    Parameters:
    -----------
    None

    Methods:
    --------
    fit(X, y=None):
        This method does nothing and simply returns the transformer instance.

        Parameters:
        -----------
        X : array-like, shape (n_samples, n_features)
            The input data.

        y : array-like, shape (n_samples,), optional (default=None)
            The target values.

        Returns:
        --------
        self : object
            The transformer instance itself.

    transform(X):
        This method returns the input data without any modifications.

        Parameters:
        -----------
        X : array-like, shape (n_samples, n_features)
            The input data.

        Returns:
        --------
        transformed_X : array-like, shape (n_samples, n_features)
            The input data without any modifications.
    """

    def __init__(self):
        super().__init__()

    def _fit_implementation(self, X: pd.Series | pd.DataFrame, y=None):
        return self

    def _transform_implementation(self, X: pd.Series | pd.DataFrame):
        return X


class ReplaceDuplicated(BaseProcessing):
    """This transformer replaces duplicated values in each column by
    specified new value.

    Parameters
    ----------
    keep : str, default 'first'
        Specify which of the duplicated (if any) value to keep.
        Allowed arguments : ‘first’, ‘last’, False.

    Attributes
    ----------
    value : str, default np.nan
        value used to replace not kept duplicated.

    Methods
    -------
    fit(X, y=None)
        Returns self.

    transform(X)
        Drops the duplicated values in the Pandas DataFrame `X`
        Returns the DataFrame with the duplicated filled with 'value'
    """

    def __init__(self, keep="first", value=np.nan):
        super().__init__()
        self.keep = keep
        self.value = value

    def _fit_implementation(self, X: pd.Series | pd.DataFrame, y=None):
        return self

    def _transform_implementation(self, X: pd.Series | pd.DataFrame):
        for col in X.columns:
            X.loc[X[col].duplicated(keep=self.keep), col] = self.value
        return X


class Dropna(BaseProcessing):
    """A class to drop NaN values in a Pandas DataFrame.

    Parameters
    ----------
    how : str, default 'all'
        How to drop missing values in the data. 'all' drops the row/column if
        all the values are missing, 'any' drops the row/column if any value is
        missing, and a number 'n' drops the row/column if there are at least
        'n' missing values.

    Attributes
    ----------
    how : str
        How to drop missing values in the data.

    Methods
    -------
    fit(X, y=None)
        Returns self.

    transform(X)
        Drops the NaN values in the Pandas DataFrame `X` based on the `how`
        attribute.
        Returns the DataFrame with the NaN values dropped.
    """

    def __init__(self, how="all"):
        super().__init__()
        self.how = how

    def _fit_implementation(self, X: pd.Series | pd.DataFrame, y=None):
        return self

    def _transform_implementation(self, X: pd.Series | pd.DataFrame):
        return X.dropna(how=self.how)


class RenameColumns(BaseProcessing):
    """
    Scikit-learn transformer that renames columns of a Pandas DataFrame.

    Parameters
    ----------
    new_names: list or dict
        A list or a dictionary of new names for columns of a DataFrame.
        If it is a list, it must have the same length as the number of columns
        in the DataFrame. If it is a dictionary, keys must be the old names of
        columns and values must be the new names.

    Attributes
    ----------
    new_names: list or dict
        A list or a dictionary of new names for columns of a DataFrame.

    Methods
    -------
    fit(self, x, y=None)
       No learning is performed, the method simply returns self.

    transform(self, x)
        Renames columns of a DataFrame.

    inverse_transform(self, x)
        Renames columns of a DataFrame.
    """

    def __init__(self, new_names: list[str] | dict[str, str]):
        super().__init__()
        self.new_names = new_names

    def _fit_implementation(self, X, y=None):
        self.feature_names_in_ = list(X.columns)
        if isinstance(self.new_names, list):
            self.removed_columns = list(X.columns)
            self.added_columns = self.new_names
        else:
            self.removed_columns = self.required_columns = list(self.new_names.keys())
            self.added_columns = list(self.new_names.values())

        return self

    def _transform_implementation(self, X: pd.Series | pd.DataFrame):
        check_is_fitted(self, attributes=["feature_names_in_"])
        if isinstance(self.new_names, list):
            if len(self.new_names) != len(X.columns):
                raise ValueError(
                    "Length of new_names list must match the number "
                    "of columns in the DataFrame."
                )
            X.columns = self.new_names
        elif isinstance(self.new_names, dict):
            X.rename(columns=self.new_names, inplace=True)
        return X

    def inverse_transform(self, X: pd.Series | pd.DataFrame):
        check_is_fitted(self, attributes=["feature_names_in_"])
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)
        X.columns = self.feature_names_in_
        return self.transform(X)


class SkTransform(BaseProcessing):
    """A transformer class to apply scikit transformers on a pandas DataFrame

    This class takes in a scikit-learn transformers as input and applies the
    transformer to a pandas DataFrame. The resulting data will be a pandas
    DataFrame with the same index and columns as the input DataFrame.

    Parameters
    ----------
    transformer : object
        A scikit-learn transformer to apply on the data.

    Attributes
    ----------
    transformer : object
        A scikit-learn transformer that is fitted on the data.

    Methods
    -------
    fit(x, y=None)
        Fit the scaler to the input data `x`

    transform(x)
        Apply the transformer to the input data `x` and return the result
        as a pandas DataFrame.

    inverse_transform(x)
        Apply the inverse transformer to the input data `x` and return the
        result as a pandas DataFrame.

    """

    def __init__(self, transformer):
        super().__init__()
        self.transformer = transformer

    def _fit_implementation(self, X: pd.Series | pd.DataFrame, y=None):
        self.transformer.fit(X)
        return self

    def _transform_implementation(self, X: pd.Series | pd.DataFrame):
        check_is_fitted(self, attributes=["feature_names_in_"])
        return pd.DataFrame(
            data=self.transformer.transform(X), index=X.index, columns=X.columns
        )

    def inverse_transform(self, X: pd.Series | pd.DataFrame):
        check_is_fitted(self, attributes=["feature_names_in_"])
        X = check_and_return_dt_index_df(X)
        return pd.DataFrame(
            data=self.transformer.inverse_transform(X), index=X.index, columns=X.columns
        )


class ReplaceThreshold(BaseProcessing):
    """Class replacing values in a pandas DataFrame by "value" based on
    threshold values.

    This class implements the scikit-learn transformer API and can be used in
    a scikit-learn pipeline.

    Parameters
    ----------
    upper : float, optional (default=None)
        The upper threshold for values in the DataFrame. Values greater than
        The upper threshold for values in the DataFrame. Values greater than
        this threshold will be replaced.
    lower : float, optional (default=None)
        The lower threshold for values in the DataFrame. Values less than
        this threshold will be replaced.
    value : (default=np.nan)The value to replace the targeted values in X DataFrame
    """

    def __init__(self, upper=None, lower=None, value=np.nan):
        super().__init__()
        self.lower = lower
        self.upper = upper
        self.value = value

    def _fit_implementation(self, X: pd.Series | pd.DataFrame, y=None):
        return self

    def _transform_implementation(self, X: pd.Series | pd.DataFrame):
        if self.lower is not None:
            lower_mask = X < self.lower
        else:
            lower_mask = pd.DataFrame(
                np.full(X.shape, False), index=X.index, columns=X.columns
            )

        if self.upper is not None:
            upper_mask = X > self.upper
        else:
            upper_mask = pd.DataFrame(
                np.full(X.shape, False), index=X.index, columns=X.columns
            )

        X[np.logical_or(lower_mask, upper_mask)] = self.value

        return X


class DropTimeGradient(BaseProcessing):
    """
    A transformer that removes values in a DataFrame based on the time gradient.

    The time gradient is calculated as the difference of consecutive values in
    the time series divided by the time delta between each value.
    If the gradient is below the `lower_rate` or above the `upper_rate`,
    then the value is set to NaN.

    Parameters
    ----------
    dropna : bool, default=True
        Whether to remove NaN values from the DataFrame before processing.
    upper_rate : float, optional
        The upper rate threshold. If the gradient is greater than or equal to
        this value, the value will be set to NaN.
    lower_rate : float, optional
        The lower rate threshold. If the gradient is less than or equal to
         this value, the value will be set to NaN.

    Attributes
    ----------
    None

    Methods
    -------
    fit(X, y=None)
        No learning is performed, the method simply returns self.
    transform(X)
        Removes values in the DataFrame based on the time gradient.

    Returns
    -------
    DataFrame
        The transformed DataFrame.
    """

    def __init__(self, dropna=True, upper_rate=None, lower_rate=None):
        super().__init__()
        self.dropna = dropna
        self.upper_rate = upper_rate
        self.lower_rate = lower_rate

    def _fit_implementation(self, X: pd.Series | pd.DataFrame, y=None):
        return self

    def _transform_implementation(self, X: pd.Series | pd.DataFrame):
        X_transformed = []
        for column in X.columns:
            X_column = X[column]
            if self.dropna:
                original_index = X_column.index.copy()
                X_column = X_column.dropna()

            time_delta = X_column.index.to_series().diff().dt.total_seconds()
            abs_der = abs(X_column.diff().divide(time_delta, axis=0))
            abs_der_two = abs(X_column.diff(periods=2).divide(time_delta, axis=0))
            if self.upper_rate is not None:
                mask_der = abs_der >= self.upper_rate
                mask_der_two = abs_der_two >= self.upper_rate
            else:
                mask_der = pd.Series(
                    np.full(X_column.shape, False),
                    index=X_column.index,
                    name=X_column.name,
                )
                mask_der_two = mask_der

            if self.lower_rate is not None:
                mask_constant = abs_der <= self.lower_rate
            else:
                mask_constant = pd.Series(
                    np.full(X_column.shape, False),
                    index=X_column.index,
                    name=X_column.name,
                )

            mask_to_remove = np.logical_and(mask_der, mask_der_two)
            mask_to_remove = np.logical_or(mask_to_remove, mask_constant)

            X_column[mask_to_remove] = np.nan
            if self.dropna:
                X_column = X_column.reindex(original_index)
            X_transformed.append(X_column)
        return pd.concat(X_transformed, axis=1)


class ApplyExpression(BaseProcessing):
    """A transformer class to apply a mathematical expression on a Pandas
    DataFrame.

    This class implements a transformer that can be used to apply a
     mathematical expression to a Pandas DataFrame.
    The expression can be any valid Python expression that
    can be evaluated using the `eval` function.

    Parameters
    ----------
    expression : str
        A string representing a valid Python expression.
        The expression can use any variables defined in the local scope,
        including the `X` variable that is passed to the `transform` method
         as the input data.

    Attributes
    ----------
    expression : str
        The mathematical expression that will be applied to the input data.

    """

    def __init__(self, expression):
        super().__init__()
        self.expression = expression

    def _fit_implementation(self, X: pd.Series | pd.DataFrame, y=None):
        return self

    def _transform_implementation(self, X: pd.Series | pd.DataFrame):
        return eval(self.expression)


class TimeGradient(BaseProcessing):
    """
    A class to calculate the time gradient of a pandas DataFrame,
     which is the derivative of the data with respect to time.

    Parameters
    ----------
    dropna : bool, optional (default=True)
        Whether to drop NaN values before calculating the time gradient.

    Attributes
    ----------
    dropna : bool
        The dropna attribute of the class.

    Methods
    -------
    fit(X, y=None)
        Fits the transformer to the data. Does not modify the input data.

    transform(X)
        Transforms the input data by calculating the time gradient of
         the data.

    """

    def __init__(self):
        super().__init__()

    def _fit_implementation(self, X: pd.Series | pd.DataFrame, y=None):
        return self

    def _transform_implementation(self, X: pd.Series | pd.DataFrame):
        original_index = X.index.copy()
        derivative = time_gradient(X)
        return derivative.reindex(original_index)


class Ffill(BaseFiller, BaseProcessing):
    """
    A class to front-fill missing values in a Pandas DataFrame.
    the limit argument allows the function to stop frontfilling at a certain
    number of missing value

    Parameters:
        limit: int, default None If limit is specified, this is the maximum number
        of consecutive NaN values to forward/backward fill.
        In other words, if there is a gap with more than this number of consecutive
        NaNs, it will only be partially filled.
        If limit is not specified, this is the maximum number of entries along
        the entire axis where NaNs will be filled. Must be greater than 0 if not None.

    Methods:
        fit(self, X, y=None):
            Does nothing. Returns the object itself.
        transform(self, X):
            Fill missing values in the input DataFrame.
    """

    def __init__(
        self,
        limit: int = None,
        gaps_lte: str | pd.Timedelta | dt.timedelta = None,
        gaps_gte: str | pd.Timedelta | dt.timedelta = None,
    ):
        BaseFiller.__init__(self)
        BaseProcessing.__init__(self)
        self.limit = limit
        self.gaps_gte = gaps_gte
        self.gaps_lte = gaps_lte

    def _fit_implementation(self, X: pd.Series | pd.DataFrame, y=None):
        return self

    def _transform_implementation(self, X: pd.Series | pd.DataFrame):
        filled_x = X.ffill(limit=self.limit)

        if not (self.gaps_gte or self.gaps_lte):
            return filled_x

        gaps_mask = self.get_gaps_mask(X)
        X[gaps_mask] = filled_x[gaps_mask]
        return X


class Bfill(BaseFiller, BaseProcessing):
    """
    A class to back-fill missing values in a Pandas DataFrame.
    the limit argument allows the function to stop backfilling at a certain
    number of missing value

    Parameters:
        limit: int, default None If limit is specified, this is the maximum number
        of consecutive NaN values to forward/backward fill.
        In other words, if there is a gap with more than this number of consecutive
        NaNs, it will only be partially filled.
        If limit is not specified, this is the maximum number of entries along
        the entire axis where NaNs will be filled. Must be greater than 0 if not None.

    Methods:
        fit(self, X, y=None):
            Does nothing. Returns the object itself.
        transform(self, X):
            Fill missing values in the input DataFrame.
    """

    def __init__(
        self,
        limit: int = None,
        gaps_lte: str | pd.Timedelta | dt.timedelta = None,
        gaps_gte: str | pd.Timedelta | dt.timedelta = None,
    ):
        BaseFiller.__init__(self)
        BaseProcessing.__init__(self)
        self.limit = limit
        self.gaps_gte = gaps_gte
        self.gaps_lte = gaps_lte

    def _fit_implementation(self, X: pd.Series | pd.DataFrame, y=None):
        return self

    def _transform_implementation(self, X: pd.Series | pd.DataFrame):
        filled_x = X.bfill(limit=self.limit)

        if not (self.gaps_gte or self.gaps_lte):
            return filled_x

        gaps_mask = self.get_gaps_mask(X)
        X[gaps_mask] = filled_x[gaps_mask]
        return X

        # https://stackoverflow.com/questions/34321025/replace-values-in-numpy-2d-array-based-on-pandas-dataframe
        # x_arr = np.array(X)
        # gaps_mask = self.get_gaps_mask(X)
        # gaps_idx_raveled = np.where(gaps_mask.to_numpy().ravel())[0]
        # x_arr.flat[gaps_idx_raveled] = filled_x.to_numpy().ravel()[gaps_idx_raveled]
        # return pd.DataFrame(data=x_arr, columns=X.columns, index=X.index)


class FillNa(BaseFiller, BaseProcessing):
    """
    A class that extends scikit-learn's TransformerMixin and BaseEstimator
    to fill missing values in a Pandas DataFrame.

    Parameters:
        value: scalar, dict, Series, or DataFrame
            Value(s) used to replace missing values.

    Methods:
        fit(self, X, y=None):
            Does nothing. Returns the object itself.
        transform(self, X):
            Fill missing values in the input DataFrame.
    """

    def __init__(
        self,
        value: float,
        gaps_lte: str | pd.Timedelta | dt.timedelta = None,
        gaps_gte: str | pd.Timedelta | dt.timedelta = None,
    ):
        BaseFiller.__init__(self)
        BaseProcessing.__init__(self)
        self.value = value
        self.gaps_gte = gaps_gte
        self.gaps_lte = gaps_lte

    def _fit_implementation(self, X: pd.Series | pd.DataFrame, y=None):
        return self

    def _transform_implementation(self, X: pd.Series | pd.DataFrame):
        if self.gaps_gte or self.gaps_lte:
            gaps = self.get_gaps_dict_to_fill(X)
            for col, gaps in gaps.items():
                for gap in gaps:
                    X.loc[gap, col] = X.loc[gap, col].fillna(self.value)
            return X
        else:
            return X.fillna(self.value)


class Interpolate(BaseFiller, BaseProcessing):
    """A class that implements interpolation of missing values in
     a Pandas DataFrame.

    This class is a transformer that performs interpolation of missing
    values in a Pandas DataFrame, using the specified `method`.
    It will interpolate the gaps of size greater or equal to gaps_gte OR less than
    or equal to gaps_lte.

    Parameters:
    -----------
    method : str or None, default None
        The interpolation method to use. If None, the default interpolation
         method of the Pandas DataFrame `interpolate()` method will be used.
         ["linear", "time", "index", "values", "nearest", "zero", "slinear",
         "quadratic", "cubic", "barycentric", "polynomial", "krogh",
         "piecewise_polynomial", "spline", "pchip", "akima", "cubicspline",
         "from_derivatives"]

    gaps_lte: str | pd.Timedelta | dt.timedelta: Interpolate gaps of size less or
        equal to gaps lte

    gaps_gte: str | pd.Timedelta | dt.timedelta: Interpolate gaps of size greater or
        equal to gaps lte

    Attributes:
    -----------
    columns : Index or None
        The columns of the input DataFrame. Will be set during fitting.
    index : Index or None
        The index of the input DataFrame. Will be set during fitting.

    Methods:
    --------
    fit(X, y=None):
        Fit the transformer to the input DataFrame X. This method will set
         the `columns` and `index` attributes of the transformer,
          and return the transformer instance.
    transform(X):
        Transform the input DataFrame X by performing interpolation of
         missing values using the
        specified `method`. Returns the transformed DataFrame.

    Returns:
    -------
    A transformed Pandas DataFrame with interpolated missing values.
    """

    def __init__(
        self,
        method: str = "linear",
        gaps_lte: str | pd.Timedelta | dt.timedelta = None,
        gaps_gte: str | pd.Timedelta | dt.timedelta = None,
    ):
        BaseFiller.__init__(self)
        BaseProcessing.__init__(self)
        self.method = method
        self.gaps_gte = gaps_gte
        self.gaps_lte = gaps_lte

    def _fit_implementation(self, X: pd.Series | pd.DataFrame, y=None):
        return self

    def _transform_implementation(self, X: pd.Series | pd.DataFrame):
        gaps_mask = self.get_gaps_mask(X)
        X_full = X.interpolate(method=self.method)
        X[gaps_mask] = X_full[gaps_mask]
        return X


class Resample(BaseProcessing):
    """
    Resample time series data in a pandas DataFrame according to rule.
    Allow column wise resampling methods.

    Parameters
    ----------
    rule : str
        The pandas timedelta or object representing the target resampling
        frequency.
    method : str | Callable
        The default method for resampling.
        It Will be overridden if a specific method
        is specified in columns_method
    tide_format_methods:
        Allow the use of tide column format name__unit__bloc to specify
        column aggregation method.
        Warning using this argument will override columns_methods argument.
        Requires fitting operation before transformation
    columns_methods : list of Tuples Optional
        List of tuples containing a list of column names and associated
        resampling method.
        The method should be a string or callable that can be passed
        to the `agg()` method of a pandas DataFrame.
    """

    def __init__(
        self,
        rule: str | pd.Timedelta | dt.timedelta,
        method: str | Callable = "mean",
        tide_format_methods: dict[str, str | Callable] = None,
        columns_methods: list[tuple[list[str], str | Callable]] = None,
    ):
        super().__init__()
        self.rule = rule
        self.method = method
        self.tide_format_methods = tide_format_methods
        self.columns_methods = columns_methods

    def _fit_implementation(self, X: pd.Series | pd.DataFrame, y=None):
        if self.tide_format_methods:
            self.columns_methods = []
            for req, method in self.tide_format_methods.items():
                self.columns_methods.append(
                    (parse_request_to_col_names(X.columns, req), method)
                )

        return self

    def _transform_implementation(self, X: pd.Series | pd.DataFrame):
        check_is_fitted(self, attributes=["feature_names_in_"])
        if not self.columns_methods:
            agg_dict = {col: self.method for col in X.columns}
        else:
            agg_dict = {col: agg for cols, agg in self.columns_methods for col in cols}
            for col in X.columns:
                if col not in agg_dict.keys():
                    agg_dict[col] = self.method

        return X.resample(rule=self.rule).agg(agg_dict)[X.columns]


class AddTimeLag(BaseProcessing):
    """
     PdAddTimeLag - A transformer that adds lagged features to a pandas
     DataFrame.

    This transformer creates new features based on the provided features
    lagged by the given time lag.

    Parameters:
    -----------
    time_lag : datetime.timedelta
        The time lag used to shift the provided features. A positive time lag
        indicates that the new features will contain information from the past,
         while a negative time lag indicates that the new features will
        contain information from the future.

    features_to_lag : list of str or str or None, optional (default=None)
        The list of feature names to lag. If None, all features in the input
         DataFrame will be lagged.

    feature_marker : str or None, optional (default=None)
        The string used to prefix the names of the new lagged features.
        If None, the feature names will be prefixed with the string
        representation of the `time_lag` parameter followed by an underscore.

    drop_resulting_nan : bool, optional (default=False)
        Whether to drop rows with NaN values resulting from the lag operation.

    """

    def __init__(
        self,
        time_lag: str | pd.Timedelta | dt.timedelta = "1h",
        features_to_lag: str | list[str] = None,
        feature_marker: str = None,
        drop_resulting_nan=False,
    ):
        BaseProcessing.__init__(self)
        self.time_lag = time_lag
        self.features_to_lag = features_to_lag
        self.feature_marker = feature_marker
        self.drop_resulting_nan = drop_resulting_nan

    def _fit_implementation(self, X: pd.Series | pd.DataFrame, y=None):
        if self.features_to_lag is None:
            self.features_to_lag = X.columns
        else:
            self.features_to_lag = (
                [self.features_to_lag]
                if isinstance(self.features_to_lag, str)
                else self.features_to_lag
            )
        self.feature_marker = (
            str(self.time_lag) + "_"
            if self.feature_marker is None
            else self.feature_marker
        )
        self.required_columns = self.features_to_lag
        self.added_columns = [
            self.feature_marker + name for name in self.required_columns
        ]
        self.is_fitted_ = True
        return self

    def _transform_implementation(self, X: pd.Series | pd.DataFrame):
        check_is_fitted(self, attributes=["is_fitted_"])
        to_lag = X[self.features_to_lag].copy()
        to_lag.index = to_lag.index + self.time_lag
        to_lag.columns = self.feature_marker + to_lag.columns
        X_transformed = pd.concat([X, to_lag], axis=1)
        if self.drop_resulting_nan:
            X_transformed = X_transformed.dropna()
        return X_transformed


class GaussianFilter1D(BaseProcessing):
    """
    A transformer that applies a 1D Gaussian filter to a Pandas DataFrame.
    The Gaussian filter is a widely used smoothing filter that effectively
    reduces the high-frequency noise in an input signal.

    Parameters
    ----------
    sigma : float, default=5
        Standard deviation of the Gaussian kernel.
        In practice, the value of sigma determines the level of smoothing
        applied to the input signal. A larger value of sigma results in a
         smoother output signal, while a smaller value results in less
          smoothing. However, too large of a sigma value can result in the
           loss of important features or details in the input signal.

    mode : str, default='nearest'
        Points outside the boundaries of the input are filled according to
        the given mode. The default, 'nearest' mode is used to set the values
        beyond the edge of the array equal to the nearest edge value.
        This avoids introducing new values into the smoothed signal that
        could bias the result. Using 'nearest' mode can be particularly useful
        when smoothing a signal with a known range or limits, such as a time
        series with a fixed start and end time.

    truncate : float, default=4.
        The filter will ignore values outside the range
        (mean - truncate * sigma) to (mean + truncate * sigma).
        The truncate parameter is used to define the length of the filter
        kernel, which determines the degree of smoothing applied to the input
        signal.

    Attributes
    ----------
    columns : list
        The column names of the input DataFrame.
    index : pandas.Index
        The index of the input DataFrame.

    Methods
    -------
    get_feature_names_out(input_features=None)
        Get output feature names for the transformed data.
    fit(X, y=None)
        Fit the transformer to the input data.
    transform(X, y=None)
        Transform the input data by applying the 1D Gaussian filter.

    """

    def __init__(self, sigma=5, mode="nearest", truncate=4.0):
        super().__init__()
        self.sigma = sigma
        self.mode = mode
        self.truncate = truncate

    def _fit_implementation(self, X: pd.Series | pd.DataFrame, y=None):
        return self

    def _transform_implementation(self, X: pd.Series | pd.DataFrame):
        check_is_fitted(self, attributes=["feature_names_in_"])
        gauss_filter = partial(
            gaussian_filter1d, sigma=self.sigma, mode=self.mode, truncate=self.truncate
        )

        return X.apply(gauss_filter)


class CombineColumns(BaseProcessing):
    """
    A class that combines multiple columns in a pandas DataFrame using a specified
    function.

    Parameters
    ----------
        function (callable or None): A function or method to apply for combining
            columns.
        tide_format_columns str: Tide request format. Columns are determined using
            tide columns format name__unit__bloc. It override the columns attribute
        columns (list or None): A list of column names to combine.
            If None, all columns will be combined.

        function_kwargs (dict or None): Additional keyword arguments to pass to the
            combining function.
        drop_columns (bool): If True, the original columns to combine will be dropped
            from the DataFrame. If False, the original columns will be retained.
        label_name (str): The name of the new column that will store the combined
            values.

    Attributes
    ----------
        columns : list
            The column names of the input DataFrame.
        index : pandas.Index
            The index of the input DataFrame.

    Methods
    -------
        get_feature_names_out(input_features=None)
            Get output feature names for the transformed data.
        fit(X, y=None)
            Fit the transformer to the input data.
        transform(X, y=None)
            Transform the input data by applying the function
    """

    def __init__(
        self,
        function: Callable,
        tide_format_columns: str = None,
        columns=None,
        function_kwargs: dict = {},
        drop_columns: bool = False,
        label_name: str = "combined",
    ):
        BaseProcessing.__init__(self, added_columns=[label_name])
        self.function = function
        self.tide_format_columns = tide_format_columns
        self.columns = columns
        self.function_kwargs = function_kwargs
        self.drop_columns = drop_columns
        self.label_name = label_name

    def _fit_implementation(self, X: pd.Series | pd.DataFrame, y=None):
        if self.columns is None and self.tide_format_columns is None:
            raise ValueError("Provide at least one of columns or tide_format_columns")

        self.columns_to_combine_ = (
            parse_request_to_col_names(X.columns, self.tide_format_columns)
            if self.tide_format_columns
            else self.columns
        )
        self.required_columns = self.columns_to_combine_
        self.removed_columns = self.columns_to_combine_ if self.drop_columns else None
        return self

    def _transform_implementation(self, X: pd.Series | pd.DataFrame):
        check_is_fitted(self, attributes=["columns_to_combine_"])
        X[self.label_name] = self.function(
            X[self.columns_to_combine_], **self.function_kwargs
        )

        if self.drop_columns:
            col_to_return = [
                col for col in X.columns if col not in self.columns_to_combine_
            ]
            return X[col_to_return]
        else:
            return X


class STLFilter(BaseProcessing):
    """
    A transformer that applies Seasonal-Trend decomposition using LOESS (STL)
    to a pandas DataFrame, and filters outliers based on an absolute threshold
    from the residual (error) component of the decomposition.
    Detected outliers are replaced with NaN values.

    Parameters
    ----------
    period : int | str | timedelta
        The periodicity of the seasonal component. Can be specified as:
        - an integer for the number of observations in one seasonal cycle,
        - a string representing the time frequency (e.g., '15T' for 15 minutes),
        - a timedelta object representing the duration of the seasonal cycle.

    trend : int | str | dt.timedelta, optional
        The length of the trend smoother. Must be odd and larger than season
        Statsplot indicate it is usually around 150% of season.
        Strongly depends on your time series.

    absolute_threshold : int | float
        The threshold for detecting anomalies in the residual component.
        Any value in the residual that exceeds this threshold (absolute value)
         is considered an anomaly and replaced by NaN.

    seasonal : int | str | timedelta, optional
        The length of the smoothing window for the seasonal component.
        If not provided, it is inferred based on the period.
        Must be an odd integer if specified as an int.
        Can also be specified as a string representing a time frequency or a
        timedelta object.

    stl_additional_kwargs : dict[str, float], optional
        Additional keyword arguments to pass to the STL decomposition.

    Methods
    -------
    fit(X, y=None)
        Stores the columns and index of the input DataFrame but does not change
        the data. The method is provided for compatibility with the
        scikit-learn pipeline.

    transform(X)
        Applies the STL decomposition to each column of the input DataFrame `X`
        and replaces outliers detected in the residual component with NaN values.
        The outliers are determined based on the provided `absolute_threshold`.

    Returns
    -------
    pd.DataFrame
        The transformed DataFrame with outliers replaced by NaN.
    """

    def __init__(
        self,
        period: int | str | dt.timedelta,
        trend: int | str | dt.timedelta,
        absolute_threshold: int | float,
        seasonal: int | str | dt.timedelta = None,
        stl_additional_kwargs: dict[str, float] = None,
    ):
        super().__init__()
        self.period = period
        self.trend = trend
        self.absolute_threshold = absolute_threshold
        self.seasonal = seasonal
        self.stl_additional_kwargs = stl_additional_kwargs

    def _fit_implementation(self, X: pd.Series | pd.DataFrame, y=None):
        self.stl_ = STLEDetector(
            self.period,
            self.trend,
            self.absolute_threshold,
            self.seasonal,
            self.stl_additional_kwargs,
        )
        self.stl_.fit(X)
        return self

    def _transform_implementation(self, X: pd.Series | pd.DataFrame):
        check_is_fitted(self, attributes=["feature_names_in_", "stl_"])
        errors = self.stl_.predict(X)
        errors = errors.astype(bool)
        for col in errors:
            X.loc[errors[col], col] = np.nan

        return X


class FillGapsAR(BaseFiller, BaseProcessing):
    """
    A class designed to identify gaps in time series data and fill them using
    a specified model.

    1- The class identified the gaps to fill and filter them using upper and lower gap
    thresholds.
    2- The biggest group of valid data is identified and is used to fit the model.
    3- The neighboring gaps are filled using backcasting or forecasting.
    4- OPTIONAL When the data's timestep is too short compared to the periodic behavior
    (e.g., 5-min data for a 24h pattern):
        - Resample data to a larger timestep
        - Perform predictions at the resampled timestep
        - Use linear interpolation to restore original data resolution


    The process is repeated at step 2 until there are no more gaps to fill

    Parameters
    ----------
    model_name : str, optional
        The name of the model to be used for filling gaps, by default "STL".
        It must be a key of MODEL_MAP
    model_kwargs : dict, optional
        A dictionary containing the arguments of the model.
    lower_gap_threshold : str or datetime.datetime, optional
        The lower threshold for the size of gaps to be considered, by default None.
    upper_gap_threshold : str or datetime.datetime, optional
        The upper threshold for the size of gaps to be considered, by default None.
    resample_at_td: str or time delta, optinal
        The time delta to resample fitting data before prediction

    Attributes
    ----------
    model_ : callable
        The predictive model class used to fill gaps, determined by `model_name`.
    features_ : list
        The list of feature columns present in the data.
    index_ : pd.Index
        The index of the data passed during the `fit` method.
    """

    def __init__(
        self,
        model_name: str = "STL",
        model_kwargs: dict = {},
        gaps_lte: str | dt.datetime | pd.Timestamp = None,
        gaps_gte: str | dt.datetime | pd.Timestamp = None,
        resample_at_td: str | dt.timedelta | pd.Timedelta = None,
    ):
        BaseFiller.__init__(self, gaps_lte, gaps_gte)
        BaseProcessing.__init__(self)
        self.model_name = model_name
        self.model_kwargs = model_kwargs
        self.resample_at_td = resample_at_td
        gaps_lte = pd.Timedelta(gaps_lte) if isinstance(gaps_lte, str) else gaps_lte
        resample_at_td = (
            pd.Timedelta(resample_at_td)
            if isinstance(resample_at_td, str)
            else resample_at_td
        )
        if (
            resample_at_td is not None
            and gaps_lte is not None
            and gaps_lte < resample_at_td
        ):
            raise ValueError(
                f"Cannot predict data for gaps LTE to {gaps_lte} with data"
                f"at a {resample_at_td} timestep"
            )

    def _fit_and_fill_x(self, X, biggest_group, col, idx, backcast):
        check_is_fitted(self, attributes=["model_"])
        bc_model = self.model_(backcast=backcast, **self.model_kwargs)
        if self.resample_at_td is not None:
            x_fit = X.loc[biggest_group, col].resample(self.resample_at_td).mean()
            idx_origin = idx
            if backcast:
                idx = pd.date_range(
                    idx[0],
                    x_fit.index[0] - pd.Timedelta(self.resample_at_td),
                    freq=self.resample_at_td,
                )
            else:
                idx = pd.date_range(
                    x_fit.index[-1] + pd.Timedelta(self.resample_at_td),
                    idx[-1],
                    freq=self.resample_at_td,
                )
        else:
            x_fit = X.loc[biggest_group, col]
            idx_origin = None

        bc_model.fit(x_fit)
        to_predict = idx.to_series()
        to_predict.name = col
        X.loc[idx, col] = bc_model.predict(to_predict).to_numpy().flatten()
        if self.resample_at_td is not None:
            beg = idx_origin[0] - idx_origin.freq
            end = idx_origin[-1] + idx_origin.freq
            # Interpolate linearly between inferred values and using neighbor data
            X.loc[idx_origin, col] = X.loc[beg:end, col].interpolate()
            # If gap is at boundaries
            if beg < X.index[0]:
                X.loc[idx_origin, col] = X.loc[idx_origin, col].bfill()
            if end > X.index[-1]:
                X.loc[idx_origin, col] = X.loc[idx_origin, col].ffill()

    def _fit_implementation(self, X: pd.Series | pd.DataFrame, y=None):
        self.model_ = MODEL_MAP[self.model_name]
        return self

    def _transform_implementation(self, X: pd.Series | pd.DataFrame):
        check_is_fitted(self, attributes=["model_"])
        gaps = self.get_gaps_dict_to_fill(X)
        for col in X:
            while gaps[col]:
                data_blocks = get_data_blocks(X[col], return_combination=False)[col]
                data_timedelta = [block[-1] - block[0] for block in data_blocks]
                biggest_group = data_blocks[data_timedelta.index(max(data_timedelta))]
                start, end = get_outer_timestamps(biggest_group, X.index)

                indices_to_delete = []
                for i, idx in enumerate(gaps[col]):
                    if start in idx:
                        self._fit_and_fill_x(X, biggest_group, col, idx, backcast=True)
                        indices_to_delete.append(i)
                    elif end in idx:
                        self._fit_and_fill_x(X, biggest_group, col, idx, backcast=False)
                        indices_to_delete.append(i)

                for i in sorted(indices_to_delete, reverse=True):
                    del gaps[col][i]

        return X


class ExpressionCombine(BaseProcessing):
    """
    Performs specified operations on selected columns, creating a new column
    based on the provided expression.
    Useful for aggregation in a single column, or physical expression.
    The transformer can also optionally drop the columns used in the expression
    after computation.

    Parameters
    ----------
    variables_dict : dict[str, str]
        A dictionary mapping variable names (as used in the expression) to the
        column names in the X DataFrame. Keys are variable names in the expression,
        and values are the corresponding column names in the DataFrame.

    expression : str
        A mathematical expression in string format, which will be evaluated using the
        specified columns from the DataFrame. Variables in the expression should
        match the keys in `variables_dict`.

    result_col_name : str
        Name of the new column in which the result of the evaluated expression
        will be stored.

    drop_variables : bool, default=False
        If True, the columns used in the calculation will be dropped
        from the resulting DataFrame after the transformation.

    Examples
    --------
    combiner = Combiner(
        variables_dict={
            "T1": "Tin__°C__building",
            "T2": "Text__°C__outdoor",
            "m": "mass_flwr__m3/h__hvac",
        },
        expression="(T1 - T2) * m * 1004 * 1.204",
        result_col_name="loss_ventilation__J__hvac",
        drop_variables = True
    )
    """

    def __init__(
        self,
        variables_dict: dict[str, str],
        expression: str,
        result_col_name: str,
        drop_variables: bool = False,
    ):
        BaseProcessing.__init__(
            self,
            required_columns=list(variables_dict.values()),
            removed_columns=list(variables_dict.values()) if drop_variables else None,
            added_columns=result_col_name,
        )

        self.variables_dict = variables_dict
        self.expression = expression
        self.result_col_name = result_col_name
        self.drop_variables = drop_variables

    def _fit_implementation(self, X, y=None):
        return self

    def _transform_implementation(self, X: pd.Series | pd.DataFrame):
        exp = self.expression
        for key, val in self.variables_dict.items():
            exp = exp.replace(key, f'X["{val}"]')

        X.loc[:, self.result_col_name] = pd.eval(exp, target=X)
        if self.drop_variables:
            return X[
                [col for col in X.columns if col not in self.variables_dict.values()]
            ]
        else:
            return X


class FillOikoMeteo(BaseFiller, BaseOikoMeteo, BaseProcessing):
    """
    A processor that fills gaps using meteorological data from the Oikolab API.

    This class extends BaseFiller to provide functionality for
    filtering gaps based onthere size. It fills them with corresponding
    meteorological data retrieved from the Oikolab API.

    Attributes:
    -----------
    lat : float
        Latitude of the location for which to retrieve meteorological data.
    lon : float
        Longitude of the location for which to retrieve meteorological data.
    param_map : dict[str, str]
        Mapping of input columns to Oikolab API parameters. Oikolab parameters are :
        'temperature', 'dewpoint_temperature', 'mean_sea_level_pressure',
        'wind_speed', '100m_wind_speed', 'relative_humidity',
        'surface_solar_radiation', 'direct_normal_solar_radiation',
        'surface_diffuse_solar_radiation', 'surface_thermal_radiation',
        'total_cloud_cover', 'total_precipitation'
    model : str
        The meteorological model to use for data retrieval (default is "era5").
    env_oiko_api_key : str
        The name of the environement variable that holds the Oikolab API key
        (set during fitting).

    Example:
    --------
    >>> filler = FillOikoMeteo(gaps_gte="1h", gaps_lte="24h", lat=43.47, lon=-1.51)
    >>> filler.fit(X)
    >>> X_filled = filler.transform(X)

    Notes:
    ------
    - The class requires an Oikolab API key to be set as an environment
    variable env_oiko_api_key.
    - If param_map is not provided, all columns will be filled with temperature data.
    This dumb behavior ensures the processing object is working with default values
    to comply with scikit learn API recomandation.
    - The class handles different frequencies of input data, interpolating or
    resampling as needed.
    """

    def __init__(
        self,
        gaps_lte: str | pd.Timedelta | dt.timedelta = None,
        gaps_gte: str | pd.Timedelta | dt.timedelta = None,
        lat: float = 43.47,
        lon: float = -1.51,
        columns_param_map: dict[str, str] = None,
        model: str = "era5",
        env_oiko_api_key: str = "OIKO_API_KEY",
    ):
        BaseFiller.__init__(self, gaps_lte, gaps_gte)
        BaseOikoMeteo.__init__(self, lat, lon, model, env_oiko_api_key)
        BaseProcessing.__init__(self)
        self.columns_param_map = columns_param_map

    def _fit_implementation(self, X, y=None):
        if self.columns_param_map is None:
            # Dumb action fill everything with temperature
            self.columns_param_map = {col: "temperature" for col in X.columns}
        self.get_api_key_from_env()
        self.fitted_ = True
        return self

    def _transform_implementation(self, X: pd.Series | pd.DataFrame):
        check_is_fitted(self, attributes=["fitted_", "api_key_"])
        gaps_dict = self.get_gaps_dict_to_fill(X)
        for col, idx_list in gaps_dict.items():
            if col in self.columns_param_map.keys():
                for idx in idx_list:
                    df = self.get_meteo_from_idx(idx, [self.columns_param_map[col]])
                    X.loc[idx, col] = df.loc[idx, self.columns_param_map[col]]
        return X


class AddOikoData(BaseOikoMeteo, BaseProcessing):
    """
    A transformer class to fetch and integrate Oikolab meteorological data
    into a given time-indexed DataFrame or Series.

    It retrieves weather data such as temperature, wind speed, or humidity
    at specified latitude and longitude, and adds it to the input DataFrame
    under user-specified column names.

    Parameters
    ----------
    lat : float, optional
        Latitude of the location for which meteorological data is to be fetched.
        Default is 43.47.
    lon : float, optional
        Longitude of the location for which meteorological data is to be fetched.
        Default is -1.51.
    param_columns_map : dict[str, str], optional
        A mapping of meteorological parameter names (keys) to column names (values)
        in the resulting DataFrame. Default is `OIKOLAB_DEFAULT_MAP`.
        Example:
         `{"temperature": "text__°C__meteo", "wind_speed": "wind__m/s__meteo"}`
    model : str, optional
        The meteorological model to use for fetching data. Default is "era5".
    env_oiko_api_key : str, optional
        The name of the environment variable containing the Oikolab API key.
        Default is "OIKO_API_KEY".

    Methods
    -------
    fit(X: pd.Series | pd.DataFrame, y=None)
        Checks the input DataFrame for conflicts with target column names
        and validates the API key availability.

    transform(X: pd.Series | pd.DataFrame)
        Fetches meteorological data and appends it to the input DataFrame
        under the specified column names at given frequency.

    Notes
    -----
    - This class requires access to the Oikolab API, and a valid API key must
      be set as an environment variable.
    - The input DataFrame must have a DateTimeIndex for fetching data at specific
      time frequencies.
    """

    def __init__(
        self,
        lat: float = 43.47,
        lon: float = -1.51,
        param_columns_map: dict[str, str] = OIKOLAB_DEFAULT_MAP,
        model: str = "era5",
        env_oiko_api_key: str = "OIKO_API_KEY",
    ):
        BaseOikoMeteo.__init__(self, lat, lon, model, env_oiko_api_key)
        BaseProcessing.__init__(self)
        self.param_columns_map = param_columns_map
        self.added_columns = list(self.param_columns_map.values())

    def _fit_implementation(self, X: pd.Series | pd.DataFrame, y=None):
        mask = X.columns.isin(self.param_columns_map.values())
        if mask.any():
            raise ValueError(
                f"Cannot add Oikolab meteo data. {X.columns[mask]} already in columns"
            )
        self.get_api_key_from_env()
        self.added_columns = list(self.param_columns_map.values())
        self.columns_check_ = True
        return self

    def _transform_implementation(self, X: pd.Series | pd.DataFrame):
        check_is_fitted(self, attributes=["columns_check_", "api_key_"])
        df = self.get_meteo_from_idx(X.index, list(self.param_columns_map.keys()))
        X.loc[:, list(self.param_columns_map.values())] = df.to_numpy()
        return X


class AddSolarAngles(BaseProcessing):
    """
    Transformer that adds solar elevation and azimuth angle to passed DataFrame.

    Attributes:
        lat (float): The latitude of the location in degrees.
        lon (float): The longitude of the location in degrees.
        data_bloc (str): Identifier for the tide data block.
        Default to "OTHER".
        data_sub_bloc (str): Identifier for the data sub-block;
        Default to "OTHER_SUB_BLOC".
    """

    def __init__(
        self,
        lat: float = 43.47,
        lon: float = -1.51,
        data_bloc: str = "OTHER",
        data_sub_bloc: str = "OTHER_SUB_BLOC",
    ):
        self.lat = lat
        self.lon = lon
        self.data_bloc = data_bloc
        self.data_sub_bloc = data_sub_bloc
        BaseProcessing.__init__(self)

    def _fit_implementation(self, X: pd.Series | pd.DataFrame, y=None):
        self.added_columns = [
            f"sun_el__angle_deg__{self.data_bloc}__{self.data_sub_bloc}",
            f"sun_az__angle_deg__{self.data_bloc}__{self.data_sub_bloc}",
        ]

    def _transform_implementation(self, X: pd.Series | pd.DataFrame):
        df = pd.DataFrame(
            data=np.array([sun_position(date, self.lat, self.lon) for date in X.index]),
            columns=self.added_columns,
            index=X.index,
        )
        return pd.concat([X, df], axis=1)


class ProjectSolarRadOnSurfaces(BaseProcessing):
    """
    Project solar radiation on various surfaces with specific orientations and tilts.

    Attributes:
        bni_column_name (str): Name of the column containing beam normal irradiance
            (BNI) data.
        dhi_column_name (str): Name of the column containing diffuse horizontal
            irradiance (DHI) data.
        ghi_column_name (str): Name of the column containing global horizontal
            irradiance (GHI) data.
        lat (float): Latitude of the location (default is 43.47).
        lon (float): Longitude of the location (default is -1.51).
        surface_azimuth_angles (int | float | list[int | float]): Azimuth angles of
            the surfaces in degrees east of north (default is 180.0,
            which corresponds to a south-facing surface in the northern hemisphere).
        surface_tilt_angle (float | list[float]): Tilt angles of the surfaces in
            degrees (default is 35.0). 0 is façing ground.
        albedo (float): Ground reflectivity or albedo (default is 0.25).
        surface_name (str | list[str]): Names for the surfaces
            (default is "az_180_tilt_35").
        data_bloc (str): Tide bloc name Default is "OTHER".
        data_sub_bloc (str): Tide sub_bloc_name default is "OTHER_SUB_BLOC".

    Raises:
        ValueError: If the number of azimuth angles, tilt angles, and surface names
        do not match.
    """

    def __init__(
        self,
        bni_column_name: str,
        dhi_column_name: str,
        ghi_column_name: str,
        lat: float = 43.47,
        lon: float = -1.51,
        surface_azimuth_angles: int | float | list[int | float] = 180.0,
        surface_tilt_angle: float | list[float] = 35.0,
        albedo: float = 0.25,
        surface_name: str | list[str] = "az_180_tilt_35",
        data_bloc: str = "OTHER",
        data_sub_bloc: str = "OTHER_SUB_BLOC",
    ):
        BaseProcessing.__init__(self)
        self.bni_column_name = bni_column_name
        self.dhi_column_name = dhi_column_name
        self.ghi_column_name = ghi_column_name
        self.lat = lat
        self.lon = lon
        self.surface_azimuth_angles = surface_azimuth_angles
        self.surface_tilt_angle = surface_tilt_angle
        self.albedo = albedo
        self.surface_name = surface_name
        self.data_bloc = data_bloc
        self.data_sub_bloc = data_sub_bloc

    def _fit_implementation(self, X: pd.Series | pd.DataFrame, y=None):
        if (
            not len(ensure_list(self.surface_azimuth_angles))
            == len(ensure_list(self.surface_tilt_angle))
            == len(ensure_list(self.surface_name))
        ):
            raise ValueError("Number of surface azimuth, tilt and name does not match")

        self.required_columns = [
            self.bni_column_name,
            self.dhi_column_name,
            self.ghi_column_name,
        ]
        self.added_columns = [
            f"{name}__W/m²__{self.data_bloc}__{self.data_sub_bloc}"
            for name in ensure_list(self.surface_name)
        ]

    def _transform_implementation(self, X: pd.Series | pd.DataFrame):
        sun_pos = np.array([sun_position(date, self.lat, self.lon) for date in X.index])
        for az, til, name in zip(
            ensure_list(self.surface_azimuth_angles),
            ensure_list(self.surface_tilt_angle),
            self.added_columns,
        ):
            X[name] = (
                beam_component(
                    til, az, 90 - sun_pos[:, 0], sun_pos[:, 1], X[self.bni_column_name]
                )
                + sky_diffuse(til, X[self.dhi_column_name])
                + ground_diffuse(til, X[self.ghi_column_name], self.albedo)
            )

        return X


class FillOtherColumns(BaseFiller, BaseProcessing):
    """
    Fill gaps in specified columns using corresponding values from
    other columns

    Parameters
    ----------
    gaps_lte : str | pd.Timedelta | dt.timedelta, optional
        Fill gaps of duration less than or equal to gaps_lte.
        If None, no upper limit is applied.
    gaps_gte : str | pd.Timedelta | dt.timedelta, optional
        Fill gaps of duration greater than or equal to gaps_gte.
        If None, no lower limit is applied.
    columns_map : dict[str, str], optional
        A mapping of target columns to the columns that will be used for filling
        their gaps. Keys represent the columns with gaps, and values represent the
        corresponding filler columns.
    drop_filling_columns : bool, default=False
        If True, removes the filler columns after filling the gaps.
    """

    def __init__(
        self,
        gaps_lte: str | pd.Timedelta | dt.timedelta = None,
        gaps_gte: str | pd.Timedelta | dt.timedelta = None,
        columns_map: dict[str, str] = {},
        drop_filling_columns: bool = False,
    ):
        BaseFiller.__init__(self, gaps_lte, gaps_gte)
        BaseProcessing.__init__(self)
        self.columns_map = columns_map
        self.drop_filling_columns = drop_filling_columns

    def _fit_implementation(self, X: pd.Series | pd.DataFrame, y=None):
        self.required_columns = list(self.columns_map.keys()) + list(
            self.columns_map.values()
        )
        if self.drop_filling_columns:
            self.removed_columns = list(self.columns_map.values())

    def _transform_implementation(self, X: pd.Series | pd.DataFrame):
        gap_dict = self.get_gaps_dict_to_fill(X[list(self.columns_map.keys())])
        for col, idxs in gap_dict.items():
            for idx in idxs:
                X.loc[idx, col] = X.loc[idx, self.columns_map[col]]
        return (
            X.drop(self.removed_columns, axis="columns")
            if self.drop_filling_columns
            else X
        )


class DropColumns(BaseProcessing):
    """
    Drop specified columns.

    Parameters
    ----------
    columns : str or list[str], optional
        The column name or a list of column names to be dropped.
        If None, no columns are dropped.

    """

    def __init__(self, columns: str | list[str] = None):
        self.columns = columns
        BaseProcessing.__init__(self)

    def _fit_implementation(self, X: pd.Series | pd.DataFrame, y=None):
        self.required_columns = self.columns
        self.removed_columns = self.columns

    def _transform_implementation(self, X: pd.Series | pd.DataFrame):
        return (
            X.drop(self.removed_columns, axis="columns")
            if self.columns is not None
            else X
        )
