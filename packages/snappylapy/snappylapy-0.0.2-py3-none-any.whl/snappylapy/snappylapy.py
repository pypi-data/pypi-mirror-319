"""Jest style testing"""
from typing import Any, TypeVar, Generic, List, Optional, Union
from abc import ABC, abstractmethod
import pathlib
import inspect
from dataclasses import dataclass
from .serialization import JsonSerializer, StringSerializer, BytesSerializer

@dataclass
class Settings:
    """Shared setting for all the strategies for doing snapshot testing."""
    snapshot_dir: pathlib.Path = pathlib.Path("__snapshots__")
    test_results_dir: pathlib.Path = pathlib.Path("__test_results__")
    snapshot_update: bool = False
    filename: str = "no_filename"


T = TypeVar('T')
class BaseSnapshot(ABC, Generic[T]):
    """Base class for snapshot testing."""

    def __init__(self, update_snapshots: bool, settings: Settings) -> None:
        """Initialize the base snapshot."""
        self.settings = settings
        self.snapshot_update: bool = update_snapshots
        self._data: Optional[T] = None
        self.settings.filename = ""

    def to_match_snapshot(self) -> None:
        """Assert test results match the snapshot."""
        if not self._compare_snapshot():
            raise AssertionError("Test results do not match the snapshot.")

    def _prepare_test(self, data: T, name: str, extension: str) -> None:
        """Prepare and save test results."""
        self._data = data
        self.settings.filename = f"{name}.{extension}" if name else self._get_filename(extension)
        file_path = self.settings.test_results_dir / self.settings.filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        self._save_test_results(file_path, data)

    def _compare_snapshot(self) -> bool:
        """Compare the snapshot with test results, updating if needed."""
        if self.snapshot_update or not (self.settings.snapshot_dir / self.settings.filename).exists():
            self._update_snapshot()
        snapshot_data = self._read_file(self.settings.snapshot_dir / self.settings.filename)
        test_data = self._read_file(self.settings.test_results_dir / self.settings.filename)
        return snapshot_data == test_data

    def _update_snapshot(self) -> None:
        """Write test results to the snapshot file."""
        snap_path = self.settings.snapshot_dir / self.settings.filename
        test_path = self.settings.test_results_dir / self.settings.filename
        snap_path.parent.mkdir(parents=True, exist_ok=True)
        snap_path.write_bytes(test_path.read_bytes())

    def _read_file(self, path: pathlib.Path) -> bytes:
        """Read file bytes or return placeholder."""
        return path.read_bytes() if path.exists() else b"<No file>"

    def _get_filename(self, extension: str) -> str:
        """Derive a filename from the call stack."""
        frame = inspect.currentframe()
        while frame:
            if frame.f_code.co_filename != __file__:
                return f"{frame.f_code.co_name}.{extension}"
            frame = frame.f_back
        raise ValueError("Could not derive filename from stack.")

    @abstractmethod
    def _save_test_results(self, path: pathlib.Path, data: T) -> None:
        """Save data for test results."""
        raise NotImplementedError


class DictExpect(BaseSnapshot[dict]):
    """Snapshot testing for dictionaries."""
    def __call__(self, data_to_snapshot: dict,
                 name: str = "",
                 filetype="dict.json") -> "DictExpect":
        """Prepare a dictionary for snapshot testing."""
        self._prepare_test(data_to_snapshot, name, filetype)
        return self

    def _save_test_results(self, path: pathlib.Path, data: dict) -> None:
        """Save dictionary data to a file."""
        data_bin = JsonSerializer[dict]().serialize(data)
        path.write_bytes(data_bin)

class ListExpect(BaseSnapshot[List[Any]]):
    """Snapshot testing for lists."""
    def __call__(self, data_to_snapshot: List[Any],
                 name: str = "",
                 filetype="list.json") -> "ListExpect":
        """Prepare a list for snapshot testing."""
        self._prepare_test(data_to_snapshot, name, filetype)
        return self

    def _save_test_results(self, path: pathlib.Path, data: List[Any]) -> None:
        """Save list data to a file."""
        data_bin = JsonSerializer[List[Any]]().serialize(data)
        path.write_bytes(data_bin)

class StringExpect(BaseSnapshot[str]):
    """Snapshot testing for strings."""

    def __call__(self, data_to_snapshot: str,
                    name: str = "",
                    filetype="string.txt") -> "StringExpect":
            """Prepare a string for snapshot testing."""
            self._prepare_test(data_to_snapshot, name, filetype)
            return self

    def _save_test_results(self, path: pathlib.Path, data: str) -> None:
        """Save string data to a file."""
        data_bin = StringSerializer().serialize(data)
        path.write_bytes(data_bin)

class BytesExpect(BaseSnapshot[bytes]):
    """Snapshot testing for bytes."""
    def __call__(self, data_to_snapshot: bytes,
                 name: str = "",
                 filetype="bytes.txt") -> "BytesExpect":
        """Prepare bytes for snapshot testing."""
        self._prepare_test(data_to_snapshot, name, filetype)
        return self

    def _save_test_results(self, path: pathlib.Path, data: bytes) -> None:
        """Save bytes data to a file."""
        data_bin = BytesSerializer().serialize(data)
        path.write_bytes(data_bin)


class Expect:
    """Snapshot testing class."""
    def __init__(self, update_snapshots: bool = False) -> None:
        self.settings = Settings()
        self.dict = DictExpect(update_snapshots, self.settings)
        self.list = ListExpect(update_snapshots, self.settings)
        self.string = StringExpect(update_snapshots, self.settings)
        self.bytes = BytesExpect(update_snapshots, self.settings)

    def read_snapshot(self) -> bytes:
        """Read the snapshot file."""
        return (self.settings.snapshot_dir / self.settings.filename).read_bytes()
    
    def read_test_results(self) -> bytes:
        """Read the test results file."""
        return (self.settings.test_results_dir / self.settings.filename).read_bytes()

    
    @property
    def snapshot_dir(self) -> pathlib.Path:
        return self.settings.snapshot_dir

    @snapshot_dir.setter
    def snapshot_dir(self, value: Union[str, pathlib.Path]) -> None:
        self.settings.snapshot_dir = pathlib.Path(value) if isinstance(value, str) else value

    @property
    def test_results_dir(self) -> pathlib.Path:
        return self.settings.test_results_dir

    @test_results_dir.setter
    def test_results_dir(self, value: Union[str, pathlib.Path]) -> None:
        self.settings.test_results_dir = pathlib.Path(value) if isinstance(value, str) else value
