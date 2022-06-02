# Weekly Report #4

## Quick recap on progress
- Data compressed with both algorithms is now stored as bytes. 
- Lempel-Ziv 77 compression is now more efficient. Recursive window search replaced with an iterative solution.


## What have I done this week?


## How has the application progressed?

## What did I learn during this week / today?

## What remained unclear or caused difficulties? 

## Initial analysis on time complexity

### Lempel-Ziv 77 
The Lempel Ziv compression algorithm goes through the whole content once. At each index a search is executed, where string content for the length of the window is looked through. Each index in the window is compared to the first index of the lookahead buffer. If they are a match, then the lookahead buffer is iteratively looked through for the length of the match. In the worst scenario the who content consists of one character (i.e. "AAA...A"). In such a case in each step the window and the lookahead buffer all all looked through, thus the time complexity being (content * window * lookahead buffer). 

### Huffman coding
The huffman coding consists of different steps that have different time complexities. 
- Calculating frequencies (iterative loop with constant time calculations)
- Building of minimum heap
- Creating storable Huffman tree with a recursive function
- 

## Pylint and Pytest - status update

## Next steps

## Study hours for week #4

| Date (dd/mm/yyyy) |Task | Hours |
| ---- | ---- | ---- |
| 29.5.2022 | Fix issue with Huffman tree decoding | 2 |
| 29.5.2022 | Write new tests | 1 |
| 31.5.2022 | Huffman coding now stores data as bytes | 1 |
| 31.5.2022 | Refactor LZ77, create iterative loop for window | 1 |
| 31.5.2022 | Create a new service package object to handle log/analysis data | 0,5 |
| 2.6.2022 | Improve logging, create new tests | 1,5 |
| 2.6.2022 | Learn that text-files downloaded from internet cause issues, investigate | 1,5 |
| 2.6.2022 | Write more tests while investigating | 1 |
| **total**| ---- | **9,5 ** |

