import pathlib
import platform
from ctypes import CDLL, POINTER, byref, c_char_p, c_int, c_size_t
from typing import Any

from ._data_structs import Bucket, Bucket_FFI, EngineSignalSet, EngineSignalSet_FFI


class SquiidEngine:
    """Class used to access the Squiid engine."""

    def __init__(self, library_path: str | None = None):
        """Construct a new Squiid engine class.

        Args:
            library_path (str | None): path to `libsquiid_engine.so`
        """
        # compute library path
        if library_path is None:
            file_directory = pathlib.Path(__file__).parent.resolve()

            prefix = "lib"
            extension = ".so"
            if platform.system() == "Windows":
                prefix = ""
                extension = ".dll"
            elif platform.system() == "Darwin":
                extension = ".dylib"

            library_path = str(
                (file_directory / f"{prefix}squiid_engine{extension}").resolve()
            )

        # load library with given path
        self._lib: CDLL = CDLL(library_path)

        # define function argument and result types
        self._lib.execute_multiple_rpn_exposed.argtypes = [
            POINTER(c_char_p),
            c_size_t,
        ]
        self._lib.execute_multiple_rpn_exposed.restype = EngineSignalSet_FFI

        self._lib.get_stack_exposed.argtypes = [POINTER(c_int)]
        self._lib.get_stack_exposed.restype = POINTER(POINTER(Bucket_FFI))

        self._lib.get_commands_exposed.argtypes = [POINTER(c_int)]
        self._lib.get_commands_exposed.restype = POINTER(c_char_p)

        self._lib.get_previous_answer_exposed.argtypes = []
        self._lib.get_previous_answer_exposed.restype = POINTER(Bucket_FFI)

        self._lib.update_previous_answer_exposed.argtypes = []
        self._lib.update_previous_answer_exposed.restype = EngineSignalSet_FFI

        # Add cleanup functions
        self._lib.free_engine_signal_set.argtypes = [EngineSignalSet_FFI]
        self._lib.free_engine_signal_set.restype = None

        self._lib.free_bucket_array.argtypes = [
            POINTER(POINTER(Bucket_FFI)),  # array pointer
            c_int,  # length
        ]
        self._lib.free_bucket_array.restype = None

        self._lib.free_bucket.argtypes = [POINTER(Bucket_FFI)]
        self._lib.free_bucket.restype = None

    def execute_multiple_rpn(self, data: list[str]) -> EngineSignalSet:
        """Execute multiple RPN commands in the engine at once.

        Args:
            data (list[str]): list of RPN commands as strings. Example: ["3", "3", "add"]

        Returns:
            EngineSignalSet: Which Engine Signals were triggered from the commands
        """
        encoded_data = [item.encode("utf-8") for item in data]

        # get pointer to data
        data_ptr = (c_char_p * len(encoded_data))(*encoded_data)

        # submit data to engine
        result: EngineSignalSet_FFI = self._lib.execute_multiple_rpn_exposed(
            data_ptr, len(encoded_data)
        )

        messages = EngineSignalSet.from_ffi(result)

        self._lib.free_engine_signal_set(result)

        return messages

    def execute_single_rpn(self, data: str) -> EngineSignalSet:
        """Execute a single RPN statement.

        Args:
            data (str): the single command to execute

        Returns:
            EngineSignalSet: Which Engine Signals were triggered from the commands
        """
        return self.execute_multiple_rpn([data])

    def get_stack(self) -> list[Bucket]:
        """Get the current stack from the engine.

        Returns:
            list[Bucket]: The stack
        """
        # define variable to store stack length
        out_len = c_int(0)

        # get stack from engine
        stack: list[Any] = self._lib.get_stack_exposed(byref(out_len))  # pyright: ignore[reportExplicitAny]

        try:
            stack_items: list[Bucket] = []
            # iterate over the given array and convert the Bucket_FFI elements to Bucket
            for i in range(out_len.value):
                if stack[i]:
                    curr_value: Bucket_FFI = stack[i].contents  # pyright: ignore[reportAny]
                    stack_items.append(Bucket.from_ffi(curr_value))

            return stack_items

        finally:
            # cleanup in case of error
            self._lib.free_bucket_array(stack, out_len)

    def get_commands(self) -> list[str]:
        """Get a list of valid commands that the engine accepts.

        Returns:
            list[str]: list of commands from the engine

        Raises:
            RuntimeError: While this shouldn't happen, if no commands are returned, a RuntimeError will be raised.
        """
        # define variable to store stack length
        out_len = c_int(0)

        result_ptr = None

        try:
            # try to get the commands
            result_ptr: list[bytes] | None = self._lib.get_commands_exposed(
                byref(out_len)
            )

            # return none on failure
            if not result_ptr or out_len.value == 0:
                raise RuntimeError("no commands were returned from the engine")

            command_list: list[str] = []
            # iterate over the array of results
            for i in range(out_len.value):
                # get the current result value
                curr_value = c_char_p(result_ptr[i]).value

                if curr_value is not None:
                    # append it to the result list if not None
                    command_list.append(curr_value.decode("utf-8"))

            return command_list

        finally:
            # free the unneeded bytes once finished
            if result_ptr and out_len.value > 0:
                self._lib.free_string_array(result_ptr, out_len)

    def get_previous_answer(self) -> Bucket:
        """Get the current previous answer variable from the engine.

        Returns:
            Bucket: Bucket containing the value of the previous answer
        """
        bucket_ffi_ptr = self._lib.get_previous_answer_exposed()  # pyright: ignore[reportAny]

        try:
            bucket = Bucket.from_ffi(bucket_ffi_ptr.contents)  # pyright: ignore[reportAny]

            return bucket
        finally:
            # cleanup in case of error
            self._lib.free_bucket(bucket_ffi_ptr)

    def update_previous_answer(self) -> EngineSignalSet:
        """Update the previous answer variable in the engine.

        This should be called after a full algebraic statement in algebraic mode,
        or after each RPN command if in RPN mode.

        Returns:
            EngineSignalSet: If an error is encountered while updating the previous answer, it will be here
        """
        signals_ffi: EngineSignalSet_FFI = self._lib.update_previous_answer_exposed()

        try:
            signals = EngineSignalSet.from_ffi(signals_ffi)

            return signals
        finally:
            # free signals in case of error
            self._lib.free_engine_signal_set(signals_ffi)
