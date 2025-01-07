# Copyright 2024 - 2025 Avram Lubkin, All Rights Reserved

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Imogen Utility Module
"""

import concurrent.futures
import hashlib
import importlib.util
import inspect
import logging
import os
import re
import shlex
import shutil
import subprocess
import time
from collections import defaultdict
from types import ModuleType, TracebackType
from typing import Any, TYPE_CHECKING, Sequence, Optional, Type, Self
from importlib.machinery import SourceFileLoader
from math import ceil
from pathlib import Path

import requests
from enlighten import format_time
from pydantic_core import CoreSchema, core_schema
from pydantic import GetCoreSchemaHandler
from requests.adapters import HTTPAdapter

from imogen.exceptions import ImogenExternalCommandError, ImogenXorrisoError

if TYPE_CHECKING:
    from imogen.config import Config


LOGGER = logging.getLogger(__name__)
RE_CHECKSUM = re.compile(r'^(\w+):(\w+)$')
CHUNK_SIZE = 10 * 1024 * 1024  # 10 MiB


def import_from_file(name: str, file_path: str) -> ModuleType:
    """
    Imports a module into the caller's namespace
    """

    if not os.path.isfile(file_path):
        raise ValueError(f'Module path is not a valid valid: {file_path}')

    spec = importlib.util.spec_from_loader(name, SourceFileLoader(name, file_path))
    if not spec:
        raise ImportError(f'Unable to import {str} from {file_path}')

    module = importlib.util.module_from_spec(spec)

    if previous_frame := getattr(inspect.currentframe(), 'f_back', None):
        previous_frame.f_globals[name] = module

    if loader := spec.loader:
        loader.exec_module(module)

    return module


class Checksum:
    """
    Checksum container and methods
    """

    def __init__(self, value: str, algorithm: str | None = None) -> None:

        # Algorithm was given
        if algorithm:
            checksum = value

        # Algorithm is include in the string
        elif match := RE_CHECKSUM.match(value):
            algorithm, checksum = match.groups()

        # Algorithm was not given and string is not valid
        else:
            raise ValueError(
                f"Checksum must be in the format 'ALGORITHM:CHECKSUM': {value}"
            )

        self.algorithm = algorithm.lower()

        if self.algorithm not in hashlib.algorithms_guaranteed:
            raise ValueError(
                f"Invalid algorithm '{algorithm}', must be one: {', '.join(hashlib.algorithms_guaranteed)}"
            )

        len(hashlib.blake2s(b'asasasasas').hexdigest())
        expected_length = len(getattr(hashlib, self.algorithm)().hexdigest())
        if len(checksum) != expected_length:
            raise ValueError(
                f"Checksum '{checksum}' has length {len(checksum)}, but length {expected_length} was expected"
            )

        self.value = checksum

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler  # pylint: disable=unused-argument
    ) -> CoreSchema:
        """
        This allows Pydantic to validate against this type
        """

        return core_schema.no_info_after_validator_function(cls, handler(str))

    def __str__(self) -> str:
        return f'{self.algorithm.upper()}:{self.value}'

    def check_file(self, file_path: Path) -> bool:
        """
        Check a local file checksum against this checksum
        """

        if file_path.is_file():
            with file_path.open('rb') as file_handle:
                checksum = hashlib.file_digest(file_handle, self.algorithm).hexdigest()

            LOGGER.debug('Local file %s has %s checksum %s', file_path, self.algorithm, checksum)
            if checksum == self.value:
                return True

        return False


class Downloader:  # pylint: disable=too-few-public-methods
    """
    Download manager
    """

    def __init__(self, config: 'Config', url: str, dest: Path) -> None:
        self.manager = config.enlighten_manager
        self.url = url
        self.dest = dest
        self.session = requests.Session()

    def _download_chunk(self, start: int, end: int) -> int:
        response = self.session.get(
            self.url, headers={'Range': f'bytes={start}-{end}'}, timeout=300
        )
        with self.dest.open('r+b') as file_handle:
            file_handle.seek(start)
            return file_handle.write(response.content)

    def threaded_download(self, workers: int = 10) -> None:
        """
        Download the URL using multiple threads

        Shows a progress bar where applicable
        """

        # Make sure thew pool size matches the number of threads
        adapter = HTTPAdapter(pool_connections=workers, pool_maxsize=workers)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

        file_size = int(self.session.head(self.url).headers['Content-Length'])
        self.dest.touch()  # Make sure file exists
        os.truncate(self.dest, file_size)  # Set file size

        # Setup progress bar
        pbar = self.manager.counter(
            total=float(file_size),
            desc=f'Download {self.dest.name}',
            unit='B',
            bar_format=(
                '{desc}{desc_pad}{percentage:3.0f}%|{bar}| {count:!.1j}{unit} / {total:!.1j}{unit} '
                '[{elapsed}<{eta}, {rate:!.2j}{unit}/s]'
            ),
            leave=False,
        )
        pbar.refresh()

        chunks = ceil(file_size / CHUNK_SIZE)
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            futures = []
            for num in range(chunks):
                start = num * CHUNK_SIZE
                end = start + CHUNK_SIZE - 1 if num < chunks - 1 else file_size - 1
                futures.append(executor.submit(self._download_chunk, start, end))

            for future in concurrent.futures.as_completed(futures):
                if exception := future.exception():
                    raise exception
                pbar.update(future.result())

        pbar.close(clear=True)


class Event:
    """
    Event timer
    """

    def __init__(self, name: str, category: str) -> None:
        self.name = name
        self.category = category
        self.start_time = time.time()
        self.stop_time = 0.0

    def stop(self) -> None:
        """Stop the timer"""
        self.stop_time = time.time()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> None:
        self.stop()

    def __repr__(self) -> str:
        return f"Event(name='{self.name}', category='{self.category}'"


class EventTimer:
    """
    Container for event timers
    """

    def __init__(self) -> None:
        self.start_time = time.time()
        self.events: list[Event] = []
        self.categories: defaultdict[str, list[Event]] = defaultdict(list)

    def start(self, name: str, category: str) -> Event:
        """
        Creates a new event and starts the timer

        returns event object
        """

        event = Event(name, category)
        self.events.append(event)
        self.categories[category].append(event)
        return event

    def __str__(self) -> str:
        out = [f"{'Total time': <25} {format_time(time.time() - self.start_time)}"]

        for category, events in self.categories.items():
            entries = []
            start = []
            stop = []
            for event in events:
                start.append(event.start_time)
                stop.append(event.stop_time)
                entries.append(
                    f'  {event.name: <23} {format_time(event.stop_time - event.start_time)}'
                )
            out.append(f'\n{category: <25} {format_time(max(stop) - min(start))}')
            out.extend(entries)

        out.append(f"{'Total time': <25} {format_time(time.time() - self.start_time)}")

        return '\n'.join(out)


def get_command(command: str, path: Path | str | None = None) -> Path:
    """
    Gets path to external command on local system
    """

    path = path or shutil.which(command)
    if path is None:
        raise ImogenExternalCommandError(f'No path found for {command}')

    path = Path(path).absolute()
    if not path.is_file():
        raise ImogenExternalCommandError(f'Invalid path for {command}: {path}')

    return path


def join_args(arguments: Sequence) -> str:
    """
    Helper function that will do a join on a sequence even if not all the items are strings
    Particularly helpful for command line options with pathlib paths
    """
    return ' '.join(str(arg) for arg in arguments)


class Xorriso:
    """
    Wrapper for xorriso
    """

    def __init__(self, xorriso_path: Path | None = None):
        self.xorriso = get_command('xorriso', xorriso_path)

    def run(self, *args: str | Path) -> subprocess.CompletedProcess:
        """
        Run xorriso

        All arguments are passed to xorriso
        """

        command = (self.xorriso, *args)

        LOGGER.debug('Running subprocess command: %s', join_args(command))

        process = subprocess.run(command, capture_output=True, check=False, env={'LANG': 'C'})
        if process.returncode != 0:
            raise ImogenXorrisoError(
                f'{join_args(command)} exited with status {process.returncode}: {process.stderr.decode('utf-8')}'
            )

        return process

    def get_iso_details(self, path: Path | str) -> tuple[str, list[str]]:
        """
        Gets volume ID and files from an ISO
        """

        process = self.run('-indev', path, '-pkt_output', 'on', '-find')

        for line in process.stderr.decode('utf-8').splitlines():
            if line.startswith('Volume id'):
                volume_id = shlex.split(line)[-1]
                break
        else:
            raise ImogenXorrisoError(f'Unable to determine volume ID for ISO at {path}')

        files = []
        for line in process.stdout.decode('utf-8').splitlines():
            if line.startswith('R:1:'):
                path = os.path.normpath(shlex.split(line)[-1])
                if path != '.':
                    files.append(path)

        return volume_id, files
