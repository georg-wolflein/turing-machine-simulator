class ExecutionError(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message


class TuringMachineError(ExecutionError):
    def __init__(self, message: str):
        super().__init__(message)


class SyntaxError(ExecutionError):
    def __init__(self, message: str):
        super().__init__(message)


def assert_property(cond: bool, message: str):
    if not cond:
        raise TuringMachineError(message)
