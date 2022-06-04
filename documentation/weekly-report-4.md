# Weekly Report #4

## Quick recap on progress
- Data compressed with both algorithms is now stored as bytes. 
- Lempel-Ziv 77 compression is now more efficient. Recursive window search replaced with an iterative solution. Still needs extensive optimization. 
- Learned that algorithms only work correctly on printable ASCII characters. Current understanding is that this is due to data manipulation when writing data to files. Perhaps considering the scope of this project restricting scope to printable ASCII-characters is justifiable? 
- New tests now test alogirthms on larger files
- Optimization issues remain. Compressing a file with million characters on LZ77 takes 50 minutes on my personal laptop at the moment.  
- Testing documentation updated
- How-to-guide updated


## What have I done this week?
At this time data can be compressed and uncompressed with both algorithms. Compressed data is written as bytes into a compressed file. Logging has been improved and now both compression and uncompression produce log information. Logging also includes assessment on time required for different stages of compression/uncompression. 

I have expanded testing and started building a view for more extensive testing. The idea is that the user can create test data with certain parameters and then run tests.

I am unsatisfied with the code quality at this time. Adding the initial version of extensive tests produced complications to the code and there is now redundancy and confusing design choices. I will do my best to refactor these before the end of the course. 


## How has the application progressed?
- Data now stored as bytes
- Automated tests expanded
- Initial manually operated extended tests created. 
- Logging improved

## What did I learn during this week / today?
I have gotten a better understanding on the restrictions of my project. I learned that my application only works properly on printable ASCII-characters: 
```
'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
```

currently I am considering whether it would be justifiable to limit the scope of this project to handling compression on files containing only these characters. My initial thoughts are that these characters provide enough variety to analyze the algorithms in a versatile way. 

From my counseling session with the course assistant I got more clarity on how to progress the project in the upcoming weeks and on what to focus on with the rest of my time with the course. 

## What remained unclear or caused difficulties? 
- Can I limit the scope to include just printable ASCII-characters?
- Suggestions on how to optimize especially the LZ77 algorithm (while still respecting the original design of the algorithm) would be very welcome. 
- Compression ratio with random ASCII-data is quite terrible, often over 100 percent (meaning that the compressed file takes more space than the original). This is understandable as for example in the LZ77 compression if no match is found, offset, match length and the next character are all stored in the data. Together they take 3 bytes. So for every non-matched one byte character three bytes are taken. And for every match of length one character two bytes of data are taken (offset and match length). So in a random ASCII data these scenarios are more frequent and compression is inefficient. 

## Initial analysis on time complexity
I will need to analyze how well my implementations match the original algorithms to get a better understanding of the time complexity. Below are initial observations. 

### Lempel-Ziv 77 
The Lempel Ziv compression algorithm goes through the whole content once. At each index a search is executed, where string content for the length of the window is looked through. Each index in the window is compared to the first index of the lookahead buffer. If they are a match, then the lookahead buffer is iteratively looked through for the length of the match. In the worst scenario the who content consists of one character (i.e. "AAA...A"). In such a case in each step the window and the lookahead buffer are all looked through, thus the time complexity being (content * window * lookahead buffer). 

In uncompression content is added to the end of the string iteratively. If a match exists, it is looked for in the existing string. Otherwise the next character is available in the stored data. In the worst case a match of the length of the buffer is found at every index > buffer size. In this scenario for each step a buffer lenght of sting data is copied and added to the end of the string. 

### Huffman coding
The huffman coding consists of different steps that have different time complexities. 
- Calculating frequencies (iterative loop with constant time calculations)
- Building of minimum heap
- Creating storable Huffman tree with a recursive function
- In the uncompression phase the Huffman tree is traversed. The tree is not balanced, but the path lengths are based on probabilities (frequencies) of characters. I will need to investigate the time complexity of this operation. 

## Pylint and Pytest - status update
Some Pylint issues remain open. These will be addressed before the end of the course. 

## Next steps
- Optimize algorithms
- Add features to extensive tests
- Refactor code
- Write documentation

## Study hours for week #4

| Date (dd/mm/yyyy) |Task | Hours |
| ---- | ---- | ---- |
| 29.5.2022 | Fix issue with Huffman tree decoding | 2 |
| 29.5.2022 | Write new tests | 1 |
| 31.5.2022 | Huffman coding now stores data as bytes | 1 |
| 31.5.2022 | Refactor LZ77, create iterative loop for window | 1 |
| 31.5.2022 | Create a new service package object to handle log/analysis data | 0,5 |
| 1.6.2022 | Guidance consultation with the course assistant | 1 |
| 2.6.2022 | Improve logging, create new tests | 1,5 |
| 2.6.2022 | Learn that text-files downloaded from internet cause issues, investigate | 1,5 |
| 2.6.2022 | Write more tests while investigating | 1 |
| 3.6.2022 | Clean code, address some pylint issues | 1 |
| 3.6.2022 | Improve logging and analysis data | 1 |
| 3.6.2022 | Create initial version of manually operated extensive tests | 2 |
| 3.6.2022 | Create new GUI - functionalities | 0,5 |
| 3.6.2022 | Write documentation | 1 |
| **total**| ---- | **16** |
