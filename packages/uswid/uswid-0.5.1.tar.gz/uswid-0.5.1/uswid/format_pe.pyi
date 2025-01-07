from .container import uSwidContainer as uSwidContainer
from .errors import NotSupportedError as NotSupportedError
from .format import uSwidFormatBase as uSwidFormatBase
from .format_coswid import uSwidFormatCoswid as uSwidFormatCoswid
from _typeshed import Incomplete

class uSwidFormatPe(uSwidFormatBase):
    objcopy: Incomplete
    cc: Incomplete
    cflags: Incomplete
    filepath: Incomplete
    def __init__(self, filepath: str | None = None) -> None: ...
    def load(self, blob: bytes, path: str | None = None) -> uSwidContainer: ...
    def save(self, container: uSwidContainer) -> bytes: ...
