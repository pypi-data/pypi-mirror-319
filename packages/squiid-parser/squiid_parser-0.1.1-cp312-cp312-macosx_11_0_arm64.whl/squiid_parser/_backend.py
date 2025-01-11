import ctypes
import pathlib
import platform


class SquiidParser:
    """Class used to access the Squiid parsing engine."""

    def __init__(self, library_path: str | None = None):
        """Construct a new Squiid parser class.

        Args:
            library_path (str | None): path to `libsquiid_parser.so`
        """
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
                (file_directory / f"{prefix}squiid_parser{extension}").resolve()
            )

        self._lib: ctypes.CDLL = ctypes.CDLL(library_path)

        # define arg types for functions
        self._lib.parse_exposed.argtypes = [
            ctypes.c_char_p,  # input string
            ctypes.POINTER(ctypes.c_int),  # output length pointer
        ]
        self._lib.parse_exposed.restype = ctypes.POINTER(ctypes.c_char_p)

        self._lib.free_string_array.argtypes = [
            ctypes.POINTER(ctypes.c_char_p),  # array pointer
            ctypes.c_int,  # length
        ]

        self._lib.free_string_array.restype = None

    def parse(self, input_string: str) -> list[str] | None:
        """Parse an algebraic notation string into an RPN notation list of strings.

        Args:
            input_string (str): The algebraic string to parse.

        Returns:
            list[str] | None: The list of operation strings in RPN notation.
        """
        # encode the input as bytes
        input_bytes = input_string.encode("utf-8")

        out_len = ctypes.c_int(0)

        result_ptr = None

        try:
            # try to parse the current string
            result_ptr: list[bytes] | None = self._lib.parse_exposed(
                ctypes.c_char_p(input_bytes), ctypes.byref(out_len)
            )

            # return none on failure
            if not result_ptr or out_len.value == 0:
                return None

            parsed_results: list[str] = []
            # iterate over the array of results
            for i in range(out_len.value):
                # get the current result value
                curr_value = ctypes.c_char_p(result_ptr[i]).value

                if curr_value is not None:
                    # append it to the result list if not None
                    parsed_results.append(curr_value.decode("utf-8"))

            return parsed_results
        finally:
            # free the unneeded bytes once finished
            if result_ptr and out_len.value > 0:
                self._lib.free_string_array(result_ptr, out_len)
