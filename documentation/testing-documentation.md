# Testing documentation

## Tests to be added (to-do-list):
* Add time efficiency tests to the extended testing
* Expand tests on service classes
* Research if there are ways to test space efficiency
* Consider testing service package FileManagement

## Coverage Report for Unittests
The coverage report can be run by typing the command `poetry run invoke coverage-report` in the terminal. Currently the branch coverage is 81 percent. Especially the service package classes need more extensive tests at this point.  

![Coverage report - week 4](images/coverage-report-week-4-image.png)


## What Has Been Tested and How?
At the moment automated tests are used to test most of the functionalities in entities packages. New classes in service packages still need tests to be written. Tests also include integrated testing in which instances of objects from both service and entities packages are tested simultaneously. 

User can now also manually operate extensive tests. Currently user can create random data either in natural English lanaguage or as random printable ASCII-characters. User can then run extensive tests that go through all the files in the default test directory defined in the .env file. When launching the tests user is asked to define what is the maximum character length for the files to be included in testing. For instance, if user inputs 50000 (fifty thousand), files with 50,000 or less characters will be included in the tests. 

![Extensive test view week 4](images/extensive-test-view-week-4.png)


## Input Used for Testing
At the moment tests use both predefined inputs and randomized input. Based on research it seems that tests with randomized input are not recommended. In the future focus will shift more to predefined inputs so that failed tests can be more easily replicated. 


## Redoing Tests
A user can run the automated tests by typing `poetry run invoke test` in the terminal. To create a coverage report user can use the command `poetry run invoke coverage-report`

## Visual Presentation of Test Results
See coverage report above at the beginning of the file. 


