# Testing documentation
The application has automated unittests and a functionalities that allow user to create test material and run an extended test-set on selected materials. 

## Automated tests
The automated tests are also divided into two categories. Lighter tests are ran every time the application is launched. These test that the basic functionalities of the application run correctly. If any of the tests fail, the application won't start. These tests include (but are not limited to):

| Package | Class | Test | Notes |
| -------- | -------- | -------- | -------- |
| Services | FileManagement | File creation works | |
| Services | FileManagement | Only valid files are compressed / uncompressed | |
| Services | FileManagement | If no log file is found a default message is returned. | |
| Services | CompressionManagement | Test file extension validation works | |
| Services | ExtensiveTestHandler | All supported characters are included | |
| Services | ExtensiveTestHandler | Randomly created content only includes supported charcters | |
| Services | ExtensiveTestHandler | Content validation works as intended | Multiple tests |
| Services | ExtensiveTestHandler | HTML-report and graphs are created | |
| Entities | HuffmanCoding | frequencies are calculated correctly | |
| Entities | HuffmanCoding | Huffman tree is built correctly | |
| Entities | HuffmanCoding | uncompressed file content matches the original file content with different types of content. ||
| Entities | HuffmanCoding | Huffman tree is correctly re-created in uncompression-phase ||
| Entities | HuffmanCoding | Huffman tree is correctly re-created in uncompression-phase | Multiple different tests |
| Entities | HuffmanNode | node comparison works. | class HuffmanNode is in the file huffman.py |
| Entities | Lempel-Ziv 77 | Uncompressed content matches original content | |
| Entities | Lempel-Ziv 77 | Various content-types are compressed and uncompressed correctly | |
| Entities | Lempel-Ziv 77 | Offsets, lengths and characters are correctly formed for "AABCABCDABCDABCD"  | |

 User can additionally manually launch more extensive tests from the terminal. The more extensive automated tests include testing algorithms on larger files and can take multiple minutes to run through. Tests include validation and user is notified if validations fail. Currently validation includes:

 - Test files have content
 - Original and uncompressed contents match

## Running tests in terminal

A lighter test-set is run every time the application start. To run this lighter test-set in the terminal, use the command
```
poetry run invoke test
```

User can also activate a test set containing more extensive tests. Please note, that running these tests can take some time. With the University provided Fuxi-laptop the tests take approximately 90 seconds. 

```
poetry run invoke extended-test
```

## Extensive tests view in GUI
In the extensive tests -view user can create new test material or run tests on files of selected size. When the tests are run, all files in the configured directory (default = test-data) that match the size user defined are included and tested. The directory can be configured in the .env -file. User can also add data to the folder for testing purposes.  

Before running the tests user is asked to specify minimum and maximum character count for files to be included. If user for instance sets the values to `100000` and `2500000` files with a character count from 100,000 to 2,500,000 will be included in the tests.  

User can view the test result of the extensive tests in the desktop application, or from a generated HTML-file. The HTML-file includes two tables and four graphs to make reviewing the test analysis easier and more enjoyable. 

## Coverage Report for Unittests
The coverage report can be run by typing the command `poetry run invoke coverage-report` in the terminal. The branch coverage of the final release is 99 percent.

![Coverage report - final release](images/coverage-report-final-release.png)

The following directories and files have been omitted from the branch coverage report:
- GUI -package
- test -package
- launch.py

## Input Used for Testing
At the moment the testing material for user operated extensive tests includes:
- Files with Python-random ASCII - content. 
- Files with randomly generated natural language content. 
- Public Domain content from Project Gutenberg and the Finnish classic 'Seitsemän Veljestä'
- First 100,000 decimals of pi

For the automated tests mostly predefined inputs are used, but few tests use randomly created material. 


## Redoing Tests
A user can run the automated tests by typing `poetry run invoke test` in the terminal. To create a coverage report user can use the command `poetry run invoke coverage-report`

## Visual Presentation of coverage branch test Results
See coverage report above. 


## Tests to be added (to-do-list):
* Expand tests on service classes
* Research if there are ways to test space efficiency
* Consider testing service packages FileManagement, LogManagement, GraphManagement
* Lempel-Ziv 77 has a lighter selection of tests than Huffman Coding. Is this alright as is? 
