# Introduction
This project was built as a university course project during Summer 2022 for the laboratory class of Data Structures and Algorithms. The subject of the project was lossless data compression.

Two well known algorithms, Huffman coding and Lempel-Ziv 77, were implemented. Please see the project documentation for additional information.


## Project documentation

* [Implementation documentation](/documentation/execution-documentation.md)
* [Requirements specification](/documentation/requirements-specification.md)
* [Testing documentation](/documentation/testing-documentation.md)
* [How-to-Guide](/documentation/how-to-guide.md)
* Weekly reports:
  * [Weekly report #1](/documentation/weekly-report-1.md)
  * [Weekly report #2](documentation/weekly-report-2.md)
  * [Weekly report #3](documentation/weekly-report-3.md)
  * [Weekly report #4](documentation/weekly-report-4.md)
  * [Weekly report #5](documentation/weekly-report-5.md)
  * [Weekly report #6](documentation/weekly-report-6.md)
Extra-documents
  * [Project architecture (extra document)](/documentation/architecture.md)

## Installation

To install the project run the following command in the project folder:
```
poetry install
```

To run the application type the following command:
```
poetry run invoke start
```

## Other useful commands

To run quick tests from terminal use the command
```
poetry run invoke test
```

To run tests on larger files (> 1 MB) use the command
```
poetry run invoke extended-test
```

To generate a coverage report use the command
```
poetry run invoke coverage-report
```