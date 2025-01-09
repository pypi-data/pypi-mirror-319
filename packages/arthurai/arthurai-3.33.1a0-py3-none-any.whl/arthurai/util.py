"""

"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Type, Union

import numpy as np
import pandas as pd
import pytz

import arthurai.core.util as core_util
from arthurai.common.constants import InferenceType, TimestampInferenceType, ValueType
from arthurai.common.exceptions import (
    UnexpectedValueError,
    UserTypeError,
    UserValueError,
)

logger = logging.getLogger(__name__)


"""
Only client facing functions should live in this module. If a util  is used for a specific package and not client facing
it should be added to that packages util.py file.
"""


def format_timestamps(
    inferences: List[Dict[str, Any]],
    tz: Optional[Union[timezone, str]] = None,
    timestamp_attributes: Optional[List[str]] = None,
    time_series_attributes: Optional[List[str]] = None,
    is_reference_data: bool = False,
) -> List[Dict[str, Any]]:
    """Checks list of json inferences to ensure their timestamps have been converted to ISO8601 conventions.

    :param inferences: inferences from input to `send_inferences()` function or output from `nest_reference_data()`
        function. This enforces requirement that the inference has an `"inference_data"` or `"reference_data"` field.
    :param tz: datetime timezone object or timezone string
    :param timestamp_attributes: List of attributes of the model of timestamp type
    :param time_series_attributes: List of attributes of the model of time series type
    :param is_reference_data: True if data to be formatted is reference data, False if inference data or ground truth
     data

    :return: updated list of json inferences with ISO8601 formatted timestamps
    :raises TypeError: timestamp is not of type `datetime.datetime`
    :raises ValueError: timestamp is not timezone aware and no location data is provided to remedy
    """
    inference_key = (
        InferenceType.INFERENCE_DATA
        if not is_reference_data
        else InferenceType.REFERENCE_DATA
    )
    if len(inferences) > 0:
        for inference in inferences:
            if TimestampInferenceType.INFERENCE_TIMESTAMP in inference:
                inference_timestamp = inference[
                    TimestampInferenceType.INFERENCE_TIMESTAMP
                ]
                inference[TimestampInferenceType.INFERENCE_TIMESTAMP] = (
                    format_timestamp(inference_timestamp, tz)
                )
            if TimestampInferenceType.GROUND_TRUTH_TIMESTAMP in inference:
                gt_timestamp = inference[TimestampInferenceType.GROUND_TRUTH_TIMESTAMP]
                inference[TimestampInferenceType.GROUND_TRUTH_TIMESTAMP] = (
                    format_timestamp(gt_timestamp, tz)
                )
            if timestamp_attributes is not None:
                for attr in timestamp_attributes:
                    attr_timestamp = inference[inference_key].get(attr)
                    if attr_timestamp is not None:
                        inference[inference_key][attr] = format_timestamp(
                            attr_timestamp, tz
                        )
            if time_series_attributes is not None:
                inference[inference_key] = format_time_series_attr_timestamps(
                    inference, time_series_attributes, tz, is_reference_data
                )

    return inferences


def format_timestamp(
    timestamp: Union[datetime, str],
    tz: Optional[Union[timezone, str]] = None,
    col_name: str = "",
) -> str:
    """Check if timestamp is time aware and convert to ISO8601 conventioned string.

    This helper function converts datetime objects into timezone aware ISO8601 strings, which is necessary when sending
    JSON to Arthur's backend. If `timestamp` argument is timezone aware, no `location` needs to be provided; otherwise,
    a string pytz `location` like "US/Eastern" needs to be provided to establish timezone. String `timestamp` are
    supported for backwards compatability and for simplicity are assumed to already be in UTC format, but string support
    will be deprecated.

    :param timestamp: timestamp to format
    :param tz: datetime timezone object or timezone string
    :param col_name: Optionally used to specify a column the timestamp originates from in the error message

    :return: ISO8601 formatted timestamp
    :raises TypeError: timestamp is not of type `datetime.datetime`
    :raises ValueError: timestamp is not timezone aware and no location data is provided to remedy
    """
    if col_name != "":
        col_name = " in column " + col_name

    if isinstance(timestamp, datetime):
        is_timezone_aware = (
            timestamp.tzinfo is not None
            and timestamp.tzinfo.utcoffset(timestamp) is not None
        )
        if is_timezone_aware:
            return timestamp.isoformat()
        else:
            # Convert string tzinfo into a datetime object
            if tz and isinstance(tz, str):
                localization = pytz.timezone(tz)
                return localization.localize(timestamp).astimezone(pytz.utc).isoformat()
            # Convert timezone object into a datetime object
            if tz and isinstance(tz, timezone):
                return timestamp.replace(tzinfo=tz).astimezone(pytz.utc).isoformat()
            else:
                raise UserValueError(
                    f"Timestamps{col_name} should be timezone aware. "
                    f"Please specify a pytz tz or set the timezone in the datetime object"
                )
    elif isinstance(timestamp, str):
        if is_valid_datetime_string(timestamp):
            return timestamp
        else:
            raise UserValueError(
                f"Timestamp '{timestamp}'{col_name} is not in ISO8601 format."
            )
    else:
        raise UserTypeError(
            f"Timestamps{col_name} must be of type datetime or string. Provided type: {str(type(timestamp))}"
        )


def format_time_series_attr_timestamps(
    inference: Dict[str, Any],
    time_series_attributes: List[str],
    tz: Optional[Union[timezone, str]] = None,
    is_reference_data: bool = False,
) -> Dict[str, Any]:
    """Formats time series timestamps in json inference to ISO8601 conventions.

    If a passed time series attribute is missing or the attribute is missing a timestamp field it will be skipped
    without raising an error.

    :param inference: Single inference from input to `send_inferences()` function or output from `nest_reference_data()`
        function. This enforces requirement that the inference has an `"inference_data"` or `"reference_data"` field.
    :param time_series_attributes: List of names of attributes of the model of time series value type
    :param tz: datetime timezone object or timezone string
    :param is_reference_data: True if reformatting reference data, False if reformatting inference data

    :returns: updated json inference_data or reference_data field
    :raises TypeError: timestamp is not of type `datetime.datetime`
    :raises ValueError: timestamp is not timezone aware and no location data is provided to remedy or inference
        does not match expected formatting
    """
    if not isinstance(inference, dict):
        raise UserValueError("inference is not a dictionary")

    inference_key = (
        InferenceType.INFERENCE_DATA
        if not is_reference_data
        else InferenceType.REFERENCE_DATA
    )
    for attr in time_series_attributes:
        if inference.get(inference_key) is None or not isinstance(
            inference.get(inference_key), dict
        ):
            raise UserValueError(
                f"inference does not have the expected {inference_key} field"
            )
        time_series_data = inference[inference_key].get(attr)
        if time_series_data is not None and core_util.is_list_like(time_series_data):
            for i in range(len(time_series_data)):
                time_series_timestamp = time_series_data[i].get("timestamp")
                if time_series_timestamp is not None:
                    inference[inference_key][attr][i]["timestamp"] = format_timestamp(
                        time_series_timestamp, tz, col_name=attr
                    )
    return inference[inference_key]


def is_valid_datetime_string(dt_obj: Any) -> bool:
    """ "
    Determines if an object is a string and in correct ISO8601 format

    :param dt_obj: possible datetime object
    :return: bool
    """
    if isinstance(dt_obj, str):
        try:
            timestamp = datetime.fromisoformat(dt_obj.replace("Z", "+00:00"))
            is_timezone_aware = (
                timestamp.tzinfo is not None
                and timestamp.tzinfo.utcoffset(timestamp) is not None
            )

            return True if is_timezone_aware else False
        # Case where string is not in valid iso-format
        except ValueError:
            return False
    else:
        return False


def normal_random_ints_fixed_sum(
    num_values: int, total_sum: int, relative_std_dev: float = 0.5
) -> np.ndarray:
    """
    Return `num_values` roughly normally-distributed integers summing to `total_sum`. Numbers are first sampled from
    the normal distribution, then adjusted to fit the sum. Adjustments are made first by shifting the resulting
    distribution to be at least `total_sum`, then decrementing a subset of the values to match `total_sum`.
    :param num_values: number of integers to return
    :param total_sum: total sum the integers returned
    :param relative_std_dev: the relative standard deviation (std_dev / mean) of the initial distribution.
    :return:
    """
    # first pull from the normal distribution to get some initial values
    mean_value = total_sum / num_values
    std_dev = mean_value * relative_std_dev
    initial_values = np.round(
        np.random.normal(loc=mean_value, scale=std_dev, size=num_values)
    ).astype(np.int64)
    # bump any negatives values up to zero
    positive_values = np.clip(initial_values, a_min=0, a_max=None)

    # shift the distribution to get close to the correct sum
    mean_diff_floor = np.floor((positive_values.sum() - total_sum) / num_values).astype(
        np.int64
    )
    values = positive_values - mean_diff_floor

    # now our difference must be less than the length of the array, and positive
    final_difference = values.sum() - total_sum
    # we can simply subtract 1 from however many indices we need to to reach the exact sum
    inds_to_decrement = np.random.choice(
        num_values, size=final_difference, replace=False
    )
    values[inds_to_decrement] -= 1

    # failsafe check
    if values.sum() != total_sum:
        raise UnexpectedValueError(
            "Computed random integers do not sum to expected total. Please report to Arthur with "
            f"the following debug info: total_sum={total_sum}, num_values={num_values}, "
            f"mean_diff_floor={mean_diff_floor}, final_difference={final_difference}, "
            f"positive_values={positive_values}, inds_to_decrement={inds_to_decrement}"
        )

    return values


def _parse_duration(time_ref: str) -> timedelta:
    """
    Parses a time duration string. Supports days and hours, e.g. "14d", "-3h", etc.
    :param time_ref: the time string to parse
    :return: timedelta of the parsed value
    """
    raw_value, unit = time_ref[:-1], time_ref[-1:]
    try:
        value = int(raw_value)
    except ValueError as e:
        raise UserValueError(
            f"Cannot parse time reference value {raw_value}, must be an integer"
        ) from e
    if unit == "d":
        return timedelta(days=value)
    elif unit == "h":
        return timedelta(hours=value)
    else:
        raise UserValueError(
            f"Cannot parse time reference unit {unit}, only days ('d') and hours ('h') are supported"
        )


# for mocking datetime.now without clobbering the entire datetime class
def _datetime_now(*args, **kwargs):
    return datetime.now(*args, **kwargs)


def generate_timestamps(
    total: int,
    duration: Union[str, timedelta] = "7d",
    end: Union[str, datetime] = "now",
    freq: Union[str, pd.DateOffset] = "D",
    noisiness: float = 0.3,
) -> List[datetime]:
    """
    Generates timestamps over a period of time, defaulting to daily timestamps over the last week. Creates `uniques`
    unique timestamp values evenly spaced between `start` and `end` inclusively. Repeats values if
    total ≠ uniques. This is useful for generating timestamps for test inferences outside of a production setting.

    :param total: the total number of timestamps to generate
    :param end: the final timestamp value
    :param duration: the difference between the first and last timestamp values. day or hour strings (e.g. "7d", "4h")
        and timedelta objects are supported
    :param freq: the frequency with which to generate unique values. See
        `Pandas Offset Aliases <https://pandas.pydata.org/docs/user_guide/timeseries.html#offset-aliases>`_ for values
    :param noisiness: how much to noise to add to the number of timestamps repeated at each interval. specifically, the
        coefficient of variation (standard deviation / mean) to use when selecting the number of times to repeat each
        timestamp
    :raises UserValueError: if an input is invalid or values contain future timestamps and allow_future is False
    :return: a list of generated timestamps
    """
    if end == "now":
        end_dt = _datetime_now(pytz.utc)
    elif not isinstance(end, datetime):
        raise UserTypeError(
            f"'end' should be string 'now' or a datetime object, got type {type(end)} with value {end}"
        )
    else:
        end_dt = end

    if isinstance(duration, str):
        duration = _parse_duration(duration)

    try:
        unique_values = pd.date_range(
            start=(end_dt - duration), end=end_dt, freq=freq
        ).to_pydatetime()
    except ValueError as e:
        raise UserValueError(e) from e
    unique_count = len(unique_values)

    if unique_count > total:
        raise UserValueError(
            f"Timestamps with duration {duration} and frequency {freq} yield {unique_count} unique "
            f"values, but you asked for {total} total values. Total values must be greater than or "
            "equal to the number of unique timestamps."
        )

    # determine how many times each timestamp should be repeated
    repeat_counts = normal_random_ints_fixed_sum(
        unique_count, total, relative_std_dev=noisiness
    )
    timestamps = unique_values.repeat(repeat_counts).tolist()

    return timestamps


def value_type_to_python_type(value_type: ValueType) -> Type:
    if value_type == ValueType.Integer:
        return int
    elif value_type == ValueType.Float:
        return float
    elif value_type == ValueType.Boolean:
        return bool
    elif value_type in (
        ValueType.String,
        ValueType.Unstructured_Text,
        ValueType.Image,
    ):  # image attributes contain strings referencing images
        return str
    elif value_type == ValueType.BoundingBox:
        return list
    else:
        raise UserValueError(f"Can't convert value type {value_type} to Python type")
