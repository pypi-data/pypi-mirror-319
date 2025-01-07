# Copyright 2025 Kasma
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import datetime
from enum import Enum


class DataType(Enum):
    """Data types supported by Flavius"""

    BOOL = "BOOL"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    STRING = "STRING"
    DATE = "DATE"
    TIME = "TIME"
    DATETIME = "DATETIME"
    TIMESTAMP = "TIMESTAMP"


class TimeStamp:
    def __init__(self, dt: datetime):
        self._dt = dt

    def __str__(self) -> str:
        if self._dt.tzinfo is None:
            return self._dt.strftime("%Y-%m-%d %H:%M:%S.%f+00:00")
        else:
            return self._dt.strftime("%Y-%m-%d %H:%M:%S.%f%z")
