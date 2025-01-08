# -*- coding: UTF-8 -*-
"""
File-based stream synchronization
=================================
@ Sync-stream

Author
------
Yuchen Jin
- cainmagi@gmail.com
- yjin4@uh.edu

Description
-----------
This module is based on the file-lock package (fasteners). It uses rotating files to
record the message items.
"""

import os
import sys
import glob
import contextlib
import types

from typing import Union, Optional
from typing import TextIO

try:
    from typing import List, Tuple, Type, Sequence
except ImportError:
    from builtins import list as List, tuple as Tuple, type as Type
    from collections.abc import Sequence

from typing_extensions import Literal, Never

import fasteners

from .base import GroupedMessage
from .base import is_end_line_break


__all__ = ("LineFileBuffer",)


class LineFileBuffer(contextlib.AbstractContextManager):
    """The file-locked line-based buffer handle.

    This buffer provides a rotating item stroage for the text-based stream. The text is
    stored not by length, but by lines. The maximal line number of the storage is
    limited.

    The file-locked handle could be shared by different processes, but we do not
    recommend to do that. A better way to use this handle is to initialize it in each
    sub-processes (if needed).

    Note that this handle is process-safe, not thread-safe. In other words, each
    process should only maintain one INDEPENDENT LineFileBuffer. The `LineFileBuffer`
    should not be shared by either different threads or different processes.
    """

    def __init__(
        self, file_path: Union[str, os.PathLike], maxlen: int = 20, tmp_id: str = "tmp"
    ) -> None:
        """Initialization.

        Arguments
        ---------
        file_path: `str | os.PathLike`
            The path of the record files. The file suffix would be automatically set
            as `.log`.

        maxlen: `int`
            The maximal number of records. Each record would be saved as one file.

        tmp_id: `str`
            The identifier for the temporary file. Each process should holds one
            unique id. A conflict id may cause the written flows from different
            processes to interrupt each other.
        """
        if not isinstance(maxlen, int) or maxlen < 1:
            raise TypeError(
                'syncstream: The argument "maxlen" should be a positive integer.'
            )
        file_path = str(file_path).strip()
        if not file_path:
            raise TypeError(
                'syncstream: The argument "file_path" should be a non-empty str.'
            )
        tmp_id = str(tmp_id)
        if not isinstance(tmp_id, str) or tmp_id == "":
            raise TypeError(
                'syncstream: The argument "tmp_id" should be a non-empty str.'
            )
        self.__file_path = os.path.splitext(file_path)[0]
        file_dir, file_name = os.path.split(self.__file_path)
        if file_name == "":
            raise TypeError(
                'syncstream: The argument "file_path" should contain a non-empty file '
                "name."
            )
        self.__file_dir = "." if file_dir == "" else file_dir
        self.__file_name = file_name
        self.__tmp_id = tmp_id
        self.__maxlen = maxlen
        self.__file_lock = fasteners.InterProcessReaderWriterLock(
            self.__file_path + ".lock"
        )
        self.__file_tmp_lock = fasteners.InterProcessReaderWriterLock(
            self.__file_path + "-{0}.lock".format(self.__tmp_id)
        )

        # Is closed
        self.__closed: bool = False

        # stdout/stderr configs
        self.__stdout: Optional[TextIO] = None
        self.__stderr: Optional[TextIO] = None

    def __enter__(self):
        """Enter the context, where stdout/stderr will be redirected to this object."""
        self.__stdout = sys.stdout
        self.__stderr = sys.stderr
        sys.stdout = self
        sys.stderr = self
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        exc_traceback: Optional[types.TracebackType],
    ) -> None:
        """Exit the context, where stdout/stderr will be retrieved."""
        sys.stdout = self.__stdout
        sys.stderr = self.__stderr
        self.__stdout = None
        self.__stderr = None
        if exc_value is None:
            self.new_line()
        else:
            self.send_exc(exc_value)
        return None

    @property
    def __tmp_file_path(self) -> str:
        """Get the temporary file path of this buffer.

        This property is private and should not be exposed to users.
        """
        return "{0}-{1}.tmp".format(self.__file_path, self.__tmp_id)

    @property
    def maxlen(self) -> int:
        """The maximal length (number of lines) of the buffer."""
        return self.__maxlen

    def __len__(self) -> int:
        """Number of lines/items in the buffer."""
        max_len = self.__maxlen
        val_n_lines = 0  # Current number of log files.
        with self.__file_lock.read_lock():
            log_files = os.listdir(self.__file_dir)
            for n in range(self.maxlen):
                if "{0}-{1:d}.log".format(self.__file_name, n) in log_files:
                    val_n_lines += 1
                else:
                    break
        if self.__get_last_line():
            val_n_lines += 1
        return min(max_len, val_n_lines) if max_len else val_n_lines

    @property
    def closed(self) -> bool:
        """Check whether the buffer has been closed."""
        return self.__closed

    def close(self, exc: Optional[BaseException] = None) -> None:
        """Close the IO. This method only takes effects once. The second call will
        do nothing.

        Arguments
        ---------
        exc: `BaseException | None`
            If `exc` is not None, will call `new_line()` before closing the buffer.
            Otherwise, call `send_exc()`.
        """
        if exc is None:
            self.new_line()
        else:
            self.send_exc(exc)
        self.__closed = True

    def fileno(self) -> Never:
        """Return the file ID.

        This buffer will not use file ID, so this method will raise an `OSError`.
        """
        raise OSError(
            "syncstream: {0} does not use fileno.".format(self.__class__.__name__)
        )

    def isatty(self) -> Literal[False]:
        """Whether the stream is connected to terminal/TTY. Return `False`"""
        return False

    def readable(self) -> bool:
        """Whether the stream is readable. The stream is readable as long as the buffer
        is not closed.

        If the stream is not readable, calling `read()` will raise an `OSError`.
        """
        with self.__file_tmp_lock.read_lock(), self.__file_lock.read_lock():
            return not self.__closed

    def writable(self) -> bool:
        """Whether the stream is writable. The stream is writable as long as the buffer
        is not closed.

        If the stream is not writable, calling `write()` will raise an `OSError`.
        """
        with self.__file_tmp_lock.write_lock(), self.__file_lock.write_lock():
            return not self.__closed

    def seekable(self) -> Literal[False]:
        """Whether the stream support random access. This buffer does not."""
        return False

    def seek(self) -> Never:
        """Will raise an `OSError` since this buffer does not support random access."""
        raise OSError(
            "syncstream: {0} does not support random "
            "access.".format(self.__class__.__name__)
        )

    def send_exc(self, exc: BaseException) -> None:
        """Send an exception/warning object to the records.

        The object will be written as a long string with its traceback. Even if the
        long string contains line break, this item will be still viewed as one record.
        """
        if self.__closed:
            return
        self.__update_records((str(GroupedMessage(exc)),))

    def new_line(self) -> None:
        R"""Manually trigger a new line to the buffer. If the current stream is already
        a new line, do nothing.

        This method is equivalent to
        ```python
        if (last line is not empty):
            write('\n')
        ```
        """
        if self.__closed:
            return

        if self.__get_last_line() != "":
            self.__write("\n")

    def clear(self) -> None:
        """Clear all log files.

        This method would search and remove all log files, including the temporary file.
        However, the lock files would not be removed. A typical usage of this method is
        to clear files only in the main process.
        """
        with self.__file_lock.write_lock():
            for fpath_remove in glob.iglob(
                "{0}-*.log".format(self.__file_path), recursive=False
            ):
                os.remove(fpath_remove)
        with self.__file_tmp_lock.write_lock():
            tmp_path = self.__tmp_file_path
            if os.path.isfile(tmp_path):
                os.remove(tmp_path)

    def flush(self) -> None:
        """Flush the current written line stream."""
        pass  # pylint: disable=unnecessary-pass

    def __update_records(self, lines: Sequence[str]) -> None:
        """Update the log files.

        The log files would be updated by this method. Each line would be saved in one
        log file.

        This method is private and should not be exposed to users.

        Arguments
        ---------
        lines: `[str]`
            The new lines to be written in the log files.
        """
        # Lock the log files in writer mode.
        with self.__file_lock.write_lock():
            # Check the number of lines, and truncate the lines.
            n_lines = len(lines)
            if n_lines <= 0:
                return
            if n_lines >= self.maxlen:
                lines = lines[-self.maxlen :]
                n_lines = self.maxlen
            # Check the number of log files.
            log_files = os.listdir(self.__file_dir)
            n_current = 0  # Current number of log files.
            for n in range(self.maxlen):
                if "{0}-{1:d}.log".format(self.__file_name, n) in log_files:
                    n_current += 1
                else:
                    break
            # Move the existing files.
            n_remain = min(n_current, self.maxlen - n_lines)
            for n in range(n_remain - 1, -1, -1):
                file_old = "{0}-{1:d}.log".format(self.__file_path, n)
                file_new = "{0}-{1:d}.log".format(self.__file_path, n + n_lines)
                if os.path.isfile(file_new):
                    os.remove(file_new)
                os.rename(file_old, file_new)
            # Write new log files in the reversed order.
            for n in range(n_lines):
                with open(
                    "{0}-{1:d}.log".format(self.__file_path, n_lines - 1 - n), "w"
                ) as fobj:
                    fobj.write(lines[n])

    def __get_last_line(self) -> str:
        """Get the last line from the log files.

        The last line should be saved in the newest log file (with a number of 0).

        This method is private and should not be exposed to users.
        """
        file_name = self.__tmp_file_path
        with self.__file_tmp_lock.read_lock():
            if os.path.isfile(file_name):
                with open(file_name, "r") as fobj:
                    last_line = fobj.read()
            else:
                last_line = ""
        return last_line

    def __clean_last_line(self) -> None:
        """Clean the last line file.

        This method is used for optimizing the clearning operation for a single line.

        This method is private and should not be exposed to users.
        """
        # Lock the log files in writer mode.
        with self.__file_tmp_lock.write_lock():
            with open(self.__tmp_file_path, "w"):
                pass

    def __write_last_line(self, line: str) -> int:
        """Append message to the last line in the log file.

        This method is used for optimizing the writting operation for a single line.

        This method is private and should not be exposed to users.
        """
        # Lock the log files in writer mode.
        with self.__file_tmp_lock.write_lock():
            with open(self.__tmp_file_path, "a") as fobj:
                return fobj.write(line)

    def parse_lines(self, lines: Sequence[str]) -> None:
        """Parse the lines.

        This method would be triggered when the new lines are written by `write()`
        method.

        The default behavior is writting the lines to the log files.

        Users could inherit this method and override it with their customized parsing
        method, like regular expression searching.

        Arguments
        ---------
        lines: `[str]`
            The new lines to be written in the log files.
        """
        self.__update_records(lines)

    def read(self, size: Optional[int] = None) -> Tuple[str, ...]:
        """Read the records.

        Fetch the stored record items from the buffer. Using the `read()` method is
        process-safe and would not influence the cursor of `write()` method.

        If the current written line is not blank, the `read()` method would regard it
        as the last record item.

        Arguments
        ---------
        size: `int | None`
            The number of record items to be returned.

        Returns:
        -------
        #1: `[str]`
            If size is `None`, would return the whole storage.

            If `size` is an `int` value, would return the last `size` items.
        """
        if not self.readable():
            raise OSError("syncstream: The stream cannot be read now.")

        if isinstance(size, int) and size <= 0:
            return tuple()
        # Get the last line.
        last_line = self.__get_last_line()
        with self.__file_lock.read_lock():
            # Check the number of log files.
            log_files = os.listdir(self.__file_dir)
            n_current = 0  # Current number of log files.
            for n in range(self.maxlen - 1 if last_line else self.maxlen):
                if "{0}-{1:d}.log".format(self.__file_name, n) in log_files:
                    n_current += 1
                else:
                    break
            # Get the number of reading lines.
            if size is None:
                n_read = n_current
            elif last_line:
                n_read = min(size - 1, n_current)
            else:
                n_read = min(size, n_current)
            # Read the log files.
            res: List[str] = list()
            for n in range(n_read - 1, -1, -1):
                with open("{0}-{1:d}.log".format(self.__file_path, n), "r") as fobj:
                    res.append(fobj.read())
            if last_line:
                res.append(last_line)
        return tuple(res)

    def __write(self, data: str) -> int:
        """The `write()` method without lock.

        This method is private and should not be used by users.
        """
        message_lines = data.splitlines()
        n_lines = len(message_lines)
        if n_lines == 1 and message_lines[0] == "":
            self.parse_lines((self.__get_last_line(),))
            self.__clean_last_line()
            return 1
        elif is_end_line_break(data):
            message_lines.append("")
            n_lines += 1
        if n_lines > 1:
            message_lines[0] = self.__get_last_line() + message_lines[0]
            last_line = message_lines.pop()
            self.parse_lines(message_lines)
            self.__clean_last_line()
            return self.__write_last_line(last_line)
        elif n_lines == 1:
            return self.__write_last_line(message_lines[0])
        else:
            return 0

    def write(self, data: str) -> int:
        """Write the records.

        The source data is the same as that of a text-based IO. Each time when `data`
        contains a line break, a new record item would be pushed in the storage. The
        `write()` method is process-safe.

        Arguments
        ---------
        data: `str`
            The data that would be written in the stream.

        Returns
        -------
        #1: `int`
            Number of lines (i.e. the record items) that are written to the storage.
        """
        if not self.writable():
            raise OSError("syncstream: The stream cannot be write now.")

        return self.__write(data)
