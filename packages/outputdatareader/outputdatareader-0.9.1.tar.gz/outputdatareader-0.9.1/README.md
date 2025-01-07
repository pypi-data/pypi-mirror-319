# outputdatareader

This outputdatareader reads the necessary data from a text file output as a result of program execution.

There are many programs that output the results of an execution to a text file, but the output is not always in a consistent format.
If the output consists of multiple sections, each of which is formatted differently, it can be difficult for a single analyzer to provide the entire output.
Also, there are cases where only some sections are wanted.

With outputodatareader, you do not necessarily need to read the entire output, only the parts you want.

## Install

outputdatareader can be installed with pip:

    $ pip install outputdatareader

Or add it to your project using the package manager:

    $ poetry add outputdatareader

## Usage

### How it works

outputdatareader consists of two stages

1. the scanner breaks the text file into appropriate segments (e.g., one line)
2. the reader repeatedly retrieves segments from the scanner one by one and reads them.

The reader processes the segments retrieved from the scanner one at a time, but can select and read only the ones it really needs. Unnecessary segments can be discarded.

The reader can also delegate part of the processing to another reader. When the processing comes back, it continues from there.

### Reader

Define a subclass that extends the `outputdatareader.readers.Base` class and create an instance for use.
This class provides the framework for the read loop, so the subclass can concentrate on parsing and reading segments retrieved from the scanner.
The subclass implements the following methods:

- `setup`
- `loop`
- `teardown`

Only `loop` is required. This method is the essential part of reading.
`setup` and `teardown` pre-process and post-process the read, respectively.

Several private methods are available during the read loop.

- `_next_loop` jumps to “next loop”.
- `_exit_loop` exits the reading loop. `teardown` is executed before returning to the caller.
- `_exit_read` skips `teardown` and finishes reading.
- `_unshift` returns one segment to the scanner.

`_unshift` is needed when the segment received from the scanner is the beginning of the “next section” to be read by another reader.
If you return one segment to the scanner and then stop reading, another reader that reads the “next section” can start reading from there.

### Scanner

The scanner breaks the text file into appropriate segments and provides them to the reader.
The scanner is an iterable object.

To create your own scanner, extend `outputdatareader.scanners.Base` class and implement the method `_scan`. `_scan` is responsible for breaking it down into appropriate segments.

`outputdatareader.scanners` module provides `LineScanner` to scan one line at a time, and `CsvScanner` to scan a CSV file one record at a time.

## Example

```python
from outputdatareader.scanners import LineScanner
from outputdatareader.readers import Base


class MainReader(Base):
    def loop(self, line):
        if line.statswith('Section 2'):
            self._unshift()
            reader = Section2Reader(self.scanner, {})
            self.holder['section_2'] = reader.read()
        elif line.statswith('Section 5'):
            self._unshift()
            reader = Section5Reader(self.scanner, {})
            self.holder['section_5'] = reader.read()
        else:
            # ignore other sections
            pass


class Section2Reader(Base):
    def loop(self, line):
        if line.startswith('Section 3'):
            self._exit_read()
        else:
            # implement here


class Section5Reader(Base):
    def loop(self, line):
        # implement here


def main():
    scanner = LineScanner('some_output.txt', encoding='utf-8')
    result_holder = {}
    reader = MainReader(scanner, result_holder)
    result = reader.read()
    print(result)


main()
```

## License

MIT License.
