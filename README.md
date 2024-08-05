# Bookerize

Bookerize is a simple tool to convert a A4 PDF file into a booklet format. It transform a PDF file in a way that when printed and folded, it will create a booklet.
At the moment, the tool only converts into a A5 booklet, but in the future, it will be possible to choose the desired format.

## Installation

To install the required dependencies, run the following command:

```bash
pip install pyPDF3
```

## Usage

To use the tool, run the following command:

```bash
python bookerize.py <path> [output_name]
```

Where `<path>` is the path to the PDF file you want to convert.
The output file will be saved in the same directory as the input file, with the name `<output_name>.pdf`. If no output name is provided, the output file will have the same name as the input file with `_bookerized` appended.

## Example

To convert the file `example.pdf` into a booklet format, run the following command:

```bash
python bookerize.py example.pdf
```

This will create a file called `example_bookerized.pdf` in the same directory as the input file.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
