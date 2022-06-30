# Project architecture
This document was not required in the course tasks and it is mainly meant for personal learning and documentation. 

## Package structure
The application follows the concept of the layered architecture framework. 

* The project will have a GUI-package for constructing and managing graphical user interfaces.
  - GUI: Constructs GUI and handles the GUI-logic
  - MainView: The first view shown to user
  - CompressionView: View in which user can compress/uncompress data
  - TestingView: View from which user can operate the extensive testing
  - SetTheme: Configures visual the theme for the application
  - Menu: Constructs the menubar for the application
* Service package handles the application logic.
  - FileManagement: Handles accessing and writing content from/to files
  - CompressionManagement: Handles logic related to compression/uncompression
  - ExtensiveTestHandler: Handles user operated extensive tests
  - LogHandler: Handles logic involved in creating log-entries
  - GraphManagement: Creates graphs (this could also be an entity, but for design reasons was included here)
* Entities package contains the algorithms to be included (Huffman coding and LZ77) and log entries. 
  - HuffmanCoding: compress/uncompress data with an algorithm based on Huffman coding
  - LempelZiv77: compress/uncompress data with an algorithm based on Lempel-Ziv 77
  - LogEntry: create a new log entry
  - SupportedCharacters: creates an object instance containing the supported characters.


```mermaid
    stateDiagram
    state Service {
        application_logic
    }
    state GUI {
        GUI_classes
    }
    state Entities {
        data_instances
    }

    GUI --> Service
    Service --> Entities
```

## Main functionalities
In this section the reader can review some core fuctionalities of the application logic as detailed sequence diagrams.

### Compressing a file with Huffman coding
The following sequence diagram details the process of compressing a file with the Huffman coding. The application logic for compression with both Huffman coding and LZ77 is similar. 

```mermaid
sequenceDiagram
actor user
participant GUI
participant CompressionManagement
participant HuffmanCoding
participant LogEntry
participant LogHandler
user ->> GUI: selects a file to be compressed
user ->> GUI: selects Huffman coding as compression method
user ->> GUI: pressess button 'compress'
GUI ->> GUI: validates file extension
GUI ->> CompressionManagement: activate_huffman_compression(filepath)
CompressionManagement ->> CompressionManagement: initialize filename for compressed file
CompressionManagement ->> LogEntry: LogEntry()
CompressionManagement ->> HuffmanCoding: HuffmanCoding(filename, compressed_filename, logentry)
CompressionManagement ->> HuffmanCoding: execute_compression()
CompressionManagement ->> HuffmanCoding: analyze_compression()
CompressionManagement ->> LogHandler: write_csv_entry_to_file(logentry.get_data_as_csv_row)
CompressionManagement ->> CompressionManagement: create_compression_logentry(logentry)
CompressionManagement ->> LogHandler: create_compression_entry(logentry.logdata)
GUI ->> GUI: _update_log()
GUI ->> GUI: clear_frame()
GUI ->> GUI: _construct_log_frame()
GUI ->> user: _compression_status_notification()
```

### Running extensive tests
Running extensive tests is the most complex set of operations in this given application. For easier readability most steps of the logic related to object instances from the Entities package and other instances from service package have been omitted from the sequence diagram. This process involves instances from all objects from the Entities package and multiple object instances from the service package (LogHandler, GraphManagement) that are now left out from the diagram.

```mermaid
sequenceDiagram
actor user
participant GUI
participant ExtensiveTestHandler
participant CompressionManagement
participant SupportedCharacters
user ->> GUI: presses button 'Run extensive tests'
user ->> GUI: enters minimum character count
user ->> GUI: enters maximum character count
GUI ->> GUI: validates min and max values
GUI ->> ExtensiveTestHandler: activate_extensive_tests(min_characters, max_characters)
ExtensiveTestHandler ->> ExtensiveTestHandler: init_html_file()
ExtensiveTestHandler ->> ExtensiveTestHandler: init_csv_file()
ExtensiveTestHandler ->> ExtensiveTestHandler: validate_test_files()
ExtensiveTestHandler ->> GUI: returns error if unsupported content and aborts
ExtensiveTestHandler ->> SupportedCharacters: get characters in dictionary
ExtensiveTestHandler ->> ExtensiveTestHandler: for each file within min and max character count
ExtensiveTestHandler ->> ExtensiveTestHandler: run_tests_on_file(filename, content)
ExtensiveTestHandler ->> ExtensiveTestHandler: test_huffman_compression(filename, content)
ExtensiveTestHandler ->> CompressionManagement: activate_huffman_compression(filename)
ExtensiveTestHandler ->> CompressionManagement: activate_huffman_uncompression(filename)
ExtensiveTestHandler ->> ExtensiveTestHandler: validate_content_matches(content, compressed_content)
ExtensiveTestHandler ->> ExtensiveTestHandler: if file handling or validation fails, log errors
ExtensiveTestHandler ->> ExtensiveTestHandler: test_lempelziv_compression(filename, content)
ExtensiveTestHandler ->> CompressionManagement: activate_lempelziv_compression(filename)
ExtensiveTestHandler ->> CompressionManagement: activate_lempelziv_uncompression(filename)
ExtensiveTestHandler ->> ExtensiveTestHandler: validate_content_matches(content, compressed_content)
ExtensiveTestHandler ->> ExtensiveTestHandler: if file handling or validation fails, log errors
ExtensiveTestHandler ->> ExtensiveTestHandler: remove_extensive_test_files()
ExtensiveTestHandler ->> ExtensiveTestHandler: log_end(success, fail, total)
ExtensiveTestHandler ->> ExtensiveTestHandler: html_log_end(success, fail, total)
GUI ->> user: _show_success_message()
```