# Introduction
This project is being built as a university course project during Summer 2022 for the laboratory class of Data Structures and Algorithms. I propose doing my project on lossless data compression.

The initial proposal is to do a comparison on two well known algorithms, Huffman coding and LZ77. For more detailed proposal please see 'Requirements specification.' For detailed report on the projects first week see 'Weekly Report #1.'


## Project documentation

* [Execution documentation](/documentation/execution-documentation.md)
* [Requirements specification](/documentation/requirements-specification.md)
* [Testing documentation](/documentation/testing-documentation.md)
* [How-to-Guide](/documentation/how-to-guide.md)
* [Weekly report #1](/documentation/weekly-report-1.md)
* [Weekly report #2](documentation/weekly-report-2.md)
* [Weekly report #3](documentation/weekly-report-3.md)
* [Weekly report #4](documentation/weekly-report-4.md)
* [Weekly report #5](documentation/weekly-report-5.md)
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