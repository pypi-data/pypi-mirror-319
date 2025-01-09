from io import UnsupportedOperation
import builtins, sqlite3

_unmodified_open = builtins.open

class SqlDir :
    def __init__(self, name, mode, db_connection):
        self.name = name
        self.mode = mode
        self.db_connection = db_connection
        self._closed = False

        self._buffer = b""

        if "r" in self.mode or "a" in self.mode or "+" in self.mode:
            row = self.db_connection.execute(
                "select content from files where name = ?", (self.name,)
            )
            if row is not None: self._buffer = row[0]
            else: self._buffer = b""

        self._pos = len(self._buffer) if "a" in mode else 0

    def write(self, data):
        if "w" not in self.mode and "a" not in self.mode and "+" not in self.mode:
            raise UnsupportedOperation("sqldir:: file not open for writing")

        if isinstance(data, str): data = data.encode("utf-8")

        self._buffer = self._buffer[:self._pos] + data + self._buffer[self._pos + len(data):]
        self._pos += len(data)

        return len(data)

    def read(self, size=-1):
        if "r" not in self.mode and "+" not in self.mode:
            raise UnsupportedOperation("File not open for reading")

        if size < 0:
            data = self._buffer[self._pos:]
            self._pos = len(self._buffer)
        else:
            data = self._buffer[self._pos:self._pos+size]
            self._pos += len(data)

        return data

    def seek(self, offset, whence=0):
        match whence:
            case 0: self._pos = offset
            case 1: self._pos += offset
            case 2: self._pos = len(self._buffer) + offset
            case _: pass
        return self._pos

    def tell(self):
        return self._pos

    def close(self):
        if not self._closed:
            self._closed = True
            if any(m in self.mode for m in ["w", "a", "+"]):
                self.db_connection.execute(
                    """
                    INSERT OR REPLACE INTO files (name, content)
                    VALUES (?, ?)
                    """,
                    (self.name, self._buffer)
                )
                self.db_connection.commit()

    def flush(self): pass
    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): self.close()

# = = =

def open(
    name, 
    mode="r",
    buffering=-1,
    encoding=None,
    errors=None,
    newline=None,
    closefd=True,
    opener=None,
    use_sqldir=True,
):
    db_modes = {"w", "r", "a", "r+", "w+", "a+"}
    
    if not any(m in mode for m in db_modes) or not use_sqldir:
        return _unmodified_open(
                name, mode, 
                buffering, encoding, errors, 
                newline, closefd, opener
        )

    return SqlDir(name, mode, _sqldir_connection)

def install_patch(path="sqldir.db"):
    global _sqldir_connection
    _sqldir_connection = sqlite3.connect(path)
    _sqldir_connection.execute(
        """
        CREATE TABLE IF NOT EXISTS files (
            name TEXT PRIMARY KEY,
            content BLOB
        );
        """
    )
    builtins.open = open

def remove_patch():
    builtins.open = _unmodified_open
