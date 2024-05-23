"""Module which accomplishes data loading and result storing.
"""
import os.path
from typing import List, Dict, Tuple, Any, Hashable
import warnings
from abc import ABC, abstractmethod

import pandas as pd
from pandas import DataFrame, ExcelWriter
from openpyxl import load_workbook

from logger import logger
from singleton_meta import SingletonMeta
from .status import TestStatus

_data_dirpath = os.getenv("TEST_DATA_DIRPATH", "./tests/data")
_config_sheet_names = dict(
    activity="_active",
)


class DataSheet(ABC):
    """Object for managing a single input Excel sheet and its output.
    """
    @abstractmethod
    def inputs(self) -> List[Tuple[Hashable, Dict[str, Any]]]:
        """Loads all inputs from an input sheet.
        """
        ...

    @abstractmethod
    def update(self, index: Hashable, status: TestStatus, output: Any = "", reason: str = ""):
        """Updates a single row in the output sheet.
        """
        ...

    @abstractmethod
    def commit(self):
        """Saves the output to an output Excel file.
        """
        ...


class ActiveDataSheet(DataSheet):
    """Object for managing a single input Excel sheet and its output.

    :ivar data_dirpath: Path to the directory containing all data. Defaults to "./tests/data".
    :ivar book_relpath: Relative path from `data_dirpath` to the Excel workbook.
    :ivar sheet_name:   Name of the sheet in the workbook.
    """
    def __init__(self, book_relpath: str, sheet_name: str, data_dirpath: str = _data_dirpath):
        self.data_dirpath = data_dirpath
        self.book_relpath = book_relpath
        self.sheet_name = sheet_name

        self._df: DataFrame | None = None  # Lazy evaluation.
        self._dirty = False

    def _init_inputs(self):
        df = pd.read_excel(os.path.join(self.data_dirpath, self.book_relpath), sheet_name=self.sheet_name)
        self._df = df[df.columns.drop(list(df.filter(regex="^_")))]

    def _prepare_output(self):
        if self._df is None:
            self._init_inputs()

        self._df = self._df.assign(_result=TestStatus.INIT.code, _reason="", _output="")

    def inputs(self) -> List[Tuple[Hashable, Dict[str, Any]]]:
        if self._df is None:
            self._init_inputs()

        return [(i, r.to_dict()) for i, r in self._df.iterrows()]

    def update(self, index: Hashable, status: TestStatus, output: Any = "", reason: str = ""):
        if not self._dirty:
            self._prepare_output()
            self._dirty = True

        self._df.loc[index, "_result"] = status.code
        self._df.loc[index, "_output"] = output
        self._df.loc[index, "_reason"] = "" if status == TestStatus.PASS else reason

    def commit(self):
        if self._dirty:
            path = os.path.join(self.data_dirpath, "o_" + self.book_relpath)

            with ExcelWriter(path, mode="a", if_sheet_exists="overlay",) as writer:
                self._df.to_excel(writer, sheet_name=self.sheet_name, index=False)


class InactiveDataSheet(DataSheet):
    """Class representing an empty sheet. Used when a sheet is inactive.

    Somwehat inspired by the Null Object design pattern.
    """
    def inputs(self) -> List[Tuple[Hashable, Dict[str, Any]]]:
        return []

    def update(self, index: Hashable, status: TestStatus, output: Any = "", reason: str = ""):
        pass

    def commit(self):
        pass


class DataCache(metaclass=SingletonMeta):
    """Provides a caching service for all :class:`DataSheets`.

    :ivar data_dirpath:         Path to the directory containing all data. Defaults to "./tests/data".
    """
    def __init__(self, data_dirpath: str = _data_dirpath):
        self.data_dirpath = data_dirpath
        self.cache: Dict[str, Dict[str, DataSheet]] = {}
        self.inactive_sheets: Dict[str, List[str]] = {}

    def load_sheet_activity(self, book_relpath: str):
        df = pd.read_excel(
            os.path.join(self.data_dirpath, book_relpath),
            sheet_name=_config_sheet_names["activity"]
        )
        activity = {name: active for name, active in zip(df["sheet_name"].tolist(), df["is_active"].tolist())}
        self.inactive_sheets[book_relpath] = [name for name in activity.keys() if not activity[name]]

    def get_sheet(self, book_relpath: str, sheet_name: str) -> DataSheet:
        if book_relpath not in self.cache.keys():
            self.cache[book_relpath] = {}
            self.load_sheet_activity(book_relpath)

        if sheet_name not in self.inactive_sheets[book_relpath]:
            if sheet_name not in self.cache[book_relpath].keys():
                self.cache[book_relpath][sheet_name] = ActiveDataSheet(book_relpath, sheet_name, self.data_dirpath)

            return self.cache[book_relpath][sheet_name]
        else:
            return InactiveDataSheet()

    def inputs(self, book_relpath: str, sheet_name: str) -> List[Tuple[Hashable, Dict[str, Any]]]:
        return self.get_sheet(book_relpath, sheet_name).inputs()

    def update(self, book_relpath: str, sheet_name: str, index: Hashable,
               status: TestStatus, output: Any = "", reason: str = ""):
        self.cache[book_relpath][sheet_name].update(index, status, output, reason)

    def commit(self):
        for book_relpath, sheets in self.cache.items():
            for sheet_name, sheet in sheets.items():
                sheet.commit()


class TestManager(metaclass=SingletonMeta):
    """
    """
    def __init__(self, data_dirpath: str = _data_dirpath):
        warnings.warn(f"The class '{self.__class__.__name__}' is deprecated."
                      f"See and use {DataCache.__name__} instead.")

        self.data_dirpath = data_dirpath
        self.outputs: Dict[str, Dict[str, DataFrame]] = {}

    def inputs(self, book_relpath: str, sheet_name: str) -> List[Tuple[Hashable, Dict[str, Any]]]:
        df = pd.read_excel(os.path.join(self.data_dirpath, book_relpath), sheet_name=sheet_name)
        self.prepare_outputs(book_relpath, sheet_name, df)

        df = df[df.columns.drop(list(df.filter(regex="^_")))]
        return [(i, r.to_dict()) for i, r in df.iterrows()]

    def prepare_outputs(self, book_relpath: str, sheet_name: str, df: DataFrame):
        if book_relpath not in self.outputs.keys():
            self.outputs[book_relpath] = {}

        self.outputs[book_relpath][sheet_name] = df.assign(_result=TestStatus.INIT, _reason="", _output="")

    def update(self, book_relpath: str, sheet_name: str, index: Hashable,
               status: TestStatus, output: Any = "", reason: str = ""):
        update_df = self.outputs[book_relpath][sheet_name]
        update_df.loc[index, "_result"] = status.code
        update_df.loc[index, "_output"] = output
        update_df.loc[index, "_reason"] = "" if status == TestStatus.PASS else reason

    def commit(self):
        for book_relpath, sheets in self.outputs.items():
            path = os.path.join(self.data_dirpath, "o_" + book_relpath)

            with ExcelWriter(path) as writer:
                for sheet_name, sheet in sheets.items():
                    sheet.to_excel(writer, sheet_name=sheet_name, index=False)
