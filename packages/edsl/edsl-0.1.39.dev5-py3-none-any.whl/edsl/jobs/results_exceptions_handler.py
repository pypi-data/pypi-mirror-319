from typing import Optional, TYPE_CHECKING, Protocol
import sys
from edsl.scenarios.FileStore import HTMLFileStore
from edsl.config import CONFIG
from edsl.coop.coop import Coop


class ResultsProtocol(Protocol):
    """Protocol defining the required interface for Results objects."""

    @property
    def has_unfixed_exceptions(self) -> bool: ...

    @property
    def task_history(self) -> "TaskHistoryProtocol": ...


class TaskHistoryProtocol(Protocol):
    """Protocol defining the required interface for TaskHistory objects."""

    @property
    def indices(self) -> list: ...

    def html(self, cta: str, open_in_browser: bool, return_link: bool) -> str: ...


class RunParametersProtocol(Protocol):
    """Protocol defining the required interface for RunParameters objects."""

    @property
    def print_exceptions(self) -> bool: ...


class ResultsExceptionsHandler:
    """Handles exception reporting and display functionality."""

    def __init__(
        self, results: ResultsProtocol, parameters: RunParametersProtocol
    ) -> None:
        self.results = results
        self.parameters = parameters

        self.open_in_browser = self._get_browser_setting()
        self.remote_logging = self._get_remote_logging_setting()

    def _get_browser_setting(self) -> bool:
        """Determine if exceptions should be opened in browser based on config."""
        setting = CONFIG.get("EDSL_OPEN_EXCEPTION_REPORT_URL")
        if setting == "True":
            return True
        elif setting == "False":
            return False
        else:
            raise Exception(
                "EDSL_OPEN_EXCEPTION_REPORT_URL must be either True or False"
            )

    def _get_remote_logging_setting(self) -> bool:
        """Get remote logging setting from coop."""
        try:
            coop = Coop()
            return coop.edsl_settings["remote_logging"]
        except Exception as e:
            # print(e)
            return False

    def _generate_error_message(self, indices) -> str:
        """Generate appropriate error message based on number of exceptions."""
        msg = f"Exceptions were raised in {len(indices)} interviews.\n"
        if len(indices) > 5:
            msg += f"Exceptions were raised in the following interviews: {indices}.\n"
        return msg

    def handle_exceptions(self) -> None:
        """Handle exceptions by printing messages and generating reports as needed."""
        if not (
            self.results.has_unfixed_exceptions and self.parameters.print_exceptions
        ):
            return

        # Print error message
        error_msg = self._generate_error_message(self.results.task_history.indices)
        print(error_msg, file=sys.stderr)

        # Generate HTML report
        filepath = self.results.task_history.html(
            cta="Open report to see details.",
            open_in_browser=self.open_in_browser,
            return_link=True,
        )

        # Handle remote logging if enabled
        if self.remote_logging:
            filestore = HTMLFileStore(filepath)
            coop_details = filestore.push(description="Error report")
            print(coop_details)

        print("Also see: https://docs.expectedparrot.com/en/latest/exceptions.html")
