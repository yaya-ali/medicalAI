from threading import Thread
from typing import Any, Callable, Optional, Union
import threading
import queue


class FunctionRunnerThread(Thread):
    """A Thread subclass that runs a function in a separate thread."""

    def __init__(
        self,
        func: Callable[..., Any],
        *args: Any,
        callback: Optional[Callable[[Any], None]] = None,
    ):
        """Initialize the thread.

        Args:
            func: The function to run.
            *args: The arguments to pass to the function.
            callback: An optional callback function that will be called with the result.
        """
        super().__init__()
        self.func = func
        self.args = args
        self.callback = callback
        self.q: Any = queue.Queue()
        self.current_thread = threading.current_thread()

    def run(self) -> None:
        """Run the function with the given arguments in a separate thread.

        The result of the function is put on a queue and the callback is called with the result, if provided.
        """
        try:
            result = self.func(self.current_thread, *self.args)
        except Exception as e:
            self.q.put(e)
        else:
            self.q.put(result)
            if self.callback:
                self.callback(result)

    def result(self) -> Union[Any, None]:
        """Get the result of the function.

        This method should be called after the thread has finished.
        If the function raised an exception, this method will re-raise it.

        Returns:
            The result of the function, or None if the function has not yet
            finished or the result that has already been retrieved.
        """
        if not self.q.empty():
            result = self.q.get()
            if isinstance(result, Exception):
                raise result
            return result
        return None
