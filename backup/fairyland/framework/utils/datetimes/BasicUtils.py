# coding: utf8
"""
@ File: BasicUtils.py
@ Editor: PyCharm
@ Author: Austin (From Chengdu, China) https://fairy.host
@ HomePage: https://github.com/AustinFairyland
@ OS: Linux Ubuntu 22.04.4 Kernel 6.2.0-36-generic 
@ CreatedTime: 2023/11/26
"""
from __future__ import annotations

import sys
import warnings
import platform
import asyncio

sys.dont_write_bytecode = True
warnings.filterwarnings("ignore")
if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from typing import Union, Any
from types import FunctionType, MethodType

from datetime import datetime, timedelta
import time
import re
from dateutil.relativedelta import relativedelta

from fairyland.framework.modules.abnormal import ParameterError
from fairyland.framework.modules.enumeration import DateTimeFormatEnum


class DateTimeUtils:
    """DateTimeUtils"""

    @classmethod
    def normtimestamp(cls) -> int:
        """
        Standard 10-bit timestamps
        @return: 10-bit timestamps: Integer
        """
        return time.time().__int__()

    @classmethod
    def normdatetime(cls) -> datetime:
        """
        Get the current date and time.
        @return: Current date and time
        @rtype: datetime
        """
        return datetime.now()

    @classmethod
    def normnowtime(cls) -> datetime:
        """
        Get the current time.
        @return: Current time
        @rtype: datetime
        """
        return datetime.now().time()

    @classmethod
    def normnowdate(cls) -> datetime:
        """
        Get the current date.
        @return: Current date
        @rtype: datetime
        """
        return datetime.now().date()

    @classmethod
    def normdatetime_to_str(cls) -> str:
        """
        Get the current date and time as a formatted string.
        @return: Formatted date and time string
        @rtype: str
        """
        return datetime.now().strftime(DateTimeFormatEnum.datetime.value)

    @classmethod
    def normnowtime_to_str(cls) -> str:
        """
        Get the current time as a formatted string.
        @return: Formatted time string
        @rtype: str
        """
        return datetime.now().time().strftime(DateTimeFormatEnum.time.value)

    @classmethod
    def normnowdate_to_str(cls) -> str:
        """
        Get the current date as a formatted string.
        @return: Formatted date string
        @rtype: str
        """
        return datetime.now().date().strftime(DateTimeFormatEnum.date.value)

    @classmethod
    def timestamp_nbit(cls, n: int) -> str:
        """
        n-bit timestamps
        @param n: n-bit: Integer
        @return: n-bit timestamps: String
        """
        if not isinstance(n, int):
            raise TypeError("The n argument must be of type int.")
        timestamp_str = time.time().__str__().replace(".", "")
        if n <= 16:
            result = timestamp_str[:n]
        else:
            result = "".join((timestamp_str, (n - len(timestamp_str)) * "0"))
        return result

    @classmethod
    def timestamp_to_datetime(cls, timestamp: Union[int, float]) -> datetime:
        """
        Convert timestamp to datetime
        @param timestamp: Timestamp value
        @type timestamp: Union[int, float]
        @return: Corresponding datetime
        @rtype: datetime
        """
        return datetime.fromtimestamp(timestamp)

    @classmethod
    def datetime_to_timestamp(cls, datetime_object: datetime) -> float:
        """
        Convert datetime to timestamp
        @param datetime_object: Datetime object
        @type datetime_object: datetime
        @return: Corresponding timestamp
        @rtype: float
        """
        return datetime_object.timestamp() if datetime_object else datetime.now().timestamp()

    @classmethod
    def datetime_to_str(cls, datetime_object: datetime, format: str = DateTimeFormatEnum.datetime.value) -> str:
        """
        Convert datetime to string
        @param datetime_object: Datetime object
        @type datetime_object: datetime
        @param format: Format string
        @type format: str
        @return: Formatted string
        @rtype: str
        """
        return datetime_object.strftime(format)

    @classmethod
    def str_to_datetime(cls, datatime_str: str, format: str = DateTimeFormatEnum.datetime.value) -> datetime:
        """
        Convert string to datetime
        @param datatime_str: String representation of datetime
        @type datatime_str: str
        @param format: Format string
        @type format: str
        @return: Corresponding datetime
        @rtype: datetime
        """
        return datetime.strptime(datatime_str, format)

    @classmethod
    def timestamp_to_str(cls, timestamp: Union[int, float] = None, format: str = DateTimeFormatEnum.datetime.value) -> str:
        """
        Convert timestamp to formatted string
        @param timestamp: Timestamp value
        @type timestamp: Union[int, float]
        @param format: Format string
        @type format: str
        @return: Formatted string
        @rtype: str
        """
        return datetime.fromtimestamp(timestamp).strftime(format)

    @classmethod
    def str_to_timestamp(cls, string: str, format: str = DateTimeFormatEnum.datetime.value) -> float:
        """
        Convert string to timestamp
        @param string: String representation of datetime
        @type string: str
        @param format: Format string
        @type format: str
        @return: Corresponding timestamp
        @rtype: float
        """
        return time.mktime(time.strptime(string, format))

    @classmethod
    def add_datetime(cls, years: int = 0, months: int = 0, days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0, **kwargs: Any) -> datetime:
        """
        Adds the specified number of years, months, days, hours, minutes, and seconds to the current date and time.
        @param years: The number of years to add.
        @type years: int
        @param months: The number of months to add.
        @type months: int
        @param days: The number of days to add.
        @type days: int
        @param hours: The number of hours to add.
        @type hours: int
        @param minutes: The number of minutes to add.
        @type minutes: int
        @param seconds: The number of seconds to add.
        @type seconds: int
        @param kwargs: Additional optional parameters.
        @type kwargs: Any
        @return: The calculated date and time.
        @rtype: datetime
        """
        return datetime.now() + relativedelta(years=years, months=months, days=days, hours=hours, minutes=minutes, seconds=seconds, **kwargs)

    @classmethod
    def sub_datetime(cls, years: int = 0, months: int = 0, days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0, **kwargs: Any) -> datetime:
        """
        Subtracts the specified number of years, months, days, hours, minutes, and seconds from the current date and time.
        @param years: The number of years to subtract.
        @type years: int
        @param months: The number of months to subtract.
        @type months: int
        @param days: The number of days to subtract.
        @type days: int
        @param hours: The number of hours to subtract.
        @type hours: int
        @param minutes: The number of minutes to subtract.
        @type minutes: int
        @param seconds: The number of seconds to subtract.
        @type seconds: int
        @param kwargs: Additional optional parameters.
        @type kwargs: Any
        @return: The calculated date and time.
        @rtype: datetime
        """
        return datetime.now() - relativedelta(years=years, months=months, days=days, hours=hours, minutes=minutes, seconds=seconds, **kwargs)

    @classmethod
    def yesterday(cls) -> datetime:
        """
        Get the datetime for yesterday.
        @return: Yesterday's datetime.
        @rtype: datetime
        """
        return cls.sub_datetime(days=1)

    @classmethod
    def tomorrow(cls) -> datetime:
        """
        Get the datetime for tomorrow.
        @return: Tomorrow's datetime.
        @rtype: datetime
        """
        return cls.add_datetime(days=1)

    @classmethod
    def week_later(cls) -> datetime:
        """
        Get the datetime for a week later.
        @return: Datetime for a week later.
        @rtype: datetime
        """
        return cls.add_datetime(days=7)

    @classmethod
    def month_later(cls) -> datetime:
        """
        Get the datetime for a month later.
        @return: Datetime for a month later.
        @rtype: datetime
        """
        return cls.add_datetime(months=1)

    @classmethod
    def datetimedelta_days(cls, normdatetime: str) -> int:
        """
        Calculate the difference in days between the given date and the current date.
        @param normdatetime: The normalized date in the format 'YYYY-MM-DD'.
        @type normdatetime: str
        @return: The difference in days.
        @rtype: int
        """
        if not isinstance(normdatetime, str):
            raise TypeError("The normdatetime argument must be of type str.")
        try:
            given_date = datetime.strptime(normdatetime, DateTimeFormatEnum.date.value)
        except Exception:
            raise ValueError("Invalid date format. The date should be in the format 'YYYY-MM-DD'.")
        delta = datetime.now() - given_date
        return abs(delta.days)

    @classmethod
    def datetimerelative(cls, days: int) -> str:
        """
        Calculate the date that is 'days' days away from the current date.
        @param days: The number of days, positive or negative.
        @type days: int
        @return: The calculated date.
        @rtype: str
        """
        if not isinstance(days, int):
            raise TypeError("The days argument must be of type int.")
        relative_date = (datetime.now() + timedelta(days=days)).strftime(DateTimeFormatEnum.datetime.value)
        return relative_date

    @classmethod
    def current_milliseconds(cls) -> int:
        """
        Get the current time in milliseconds.
        @return: The current time in milliseconds
        @rtype: int
        """
        return round(time.time() * 1000)

    @classmethod
    def today_timestamp(cls) -> int:
        """
        The timestamp of the day at 0:00
        @return: Norm Timestamp
        @rtype: int
        """
        return round(time.mktime(datetime.date.today().timetuple()))
