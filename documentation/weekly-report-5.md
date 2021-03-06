# Weekly Report #5

## Quick recap on progress
- Read a lot and had piffanies
- LZ77 optimized, great improvement in compression time! 
- Created more diverse test material
- Cleaned code based on pylint feedback
- Multiple questions for the course assistant below in section "What remained unclear or caused difficulties"
- Made small updates to [Execution document](execution-documentation.md) and [Testing document](testing-documentation.md)

## What have I done this week?
The first days of the week I had to commit to preparing to the exam of Data Structures and Algorithms II, so unfortunately I had no time to work on this project. From the rest of the study hours for the week I had to spend multiple hours on research this time, but I think it was beneficial! I was able to optimize the compression time of LZ77 significantly. 

I also cleaned the code based on pylint feedback and created and downloaded new test material for even more diverse testing. 

## How has the application progressed?
- New test material created
- LZ77 optimized
- Code refactored and most pylint issues fixed

## What did I learn during this week / today?

### There is no spoon
From reading material I first and foremost learned that LZ77 isn't a compression algorithm, but a model for efficient compression method. The effect is that there is no 'canonical' LZ77 algorithm and instead there is a family of LZ77 adaptations with very different implementations and thus very different time and space complexities. This was the biggest piffany for me as I understood that I've been looking at some questions from a wrong perspective. 

### LZ77 optimization breakthrough - now using built in find()-method
Based on my discussion with the course assistant I refactored LZ77 to use pointers instead of copies from the string containing the content to be compressed. This had a two fold impact on the compression time of larger files. For some natural language files the compression rate was improved, but for files with more random content the effect was opposite.  

This lead me into thinking that perhaps using Python's built in find()-method would be a good idea. I then created a new version that uses find() and it had a tremendous impact. For instance the compression time for the book 'Seitsem??n veljest??" that has over 600,000 characters dropped from 70 seconds to 1.5 seconds! Another plus side is that based on documentation the find()-method uses known algorithms, such as Boyer-Moore and Horspool, which have a widely agreed upon time complexity, which helps me give a more precise estimation on the time complexity of my LZ77 implementation. 

As a down side, at least temproarily, I removed the concept of the into-buffer-sliding window from the execution, as it would require moving the index in the case when the match continues into the lookahead buffer. If there is time, I will try to include this within the new implementation. Removing this feature will have an effect on compression ratio, though the compression time efficiency was greatly increased. Perhaps it is a compromise that needs to be done. 


## What remained unclear or caused difficulties? 
This week I have multiple issues I hope to get feedback on:


### Algoritms ineffective with random ASCII-characters

Both algorithms are very uneffective with random ASCII - characters. Often compression ratio ends up being over 100 percent. My thoughts:
- **Huffman coding:** With randomly created character-content the frequencies are close to each other which makes all branches of the Huffman tree long and compression ratio thus poor
- **LZ77:** With randomly created character-content multiple character matches are rarer and compressed content takes more space. 

For LZ77 I think I could optimize the compression by rethinking how the content is stored. I read upon a solution where:
- First bit indicates whether a match was found (1= true, 0= false). 
- If false, then only the next character is stored (one byte), if true the offset and match length are stored. 
- Also some sources suggest limiting the requirement for minimum match length to three characters for better compression time and ratio efficiency (I implemented this in my new sliding window method)

Does this sound like a good approach for LZ77 compression optimization? 

As for Huffman coding I have no ideas at the moment. I have read a bit on 'canonical Huffman tree', but I do not yet understand the concept well enough to know, whether it'd provide any benefits in this particular issue. Any suggestions or hints would be very welcome! 

I tried what compression ratio the pre-installed compressor on Fuxi-laptop gives for the file test-data/random-printable-ascii-100-paragraphs.txt. The original size is 74.7 kB and compressed size is 62.3 kB, so the compression ratio is 0.83 (I have included the compressed zip-file for easier verification). This makes me consider that perhaps I can not meet to desired 40-60 percent compressed size for all files as professionally built applications do not achieve that. I would very much like to hear thoughts on this! 

### Algorithms ineffective with random word content
Both algorithms are sub-optimal with randomly generated words of natural language. I assume the issues are connected to the same reasons as the ones mentioned above, perhaps as randomly created string of natural language words lacks the same structure (and repetitiveness) as coherent textual content. At the moment I am unsure whether this is a limitation of these two method, or is it something I could perhaps optimize. I would very much appreciate any feedback or tips on how to proceed with this. 

### Time and Space complexity for LZ77
I created a new version of the 'sliding window' match search by using Python's built in find()-method. Based on documentation this method uses Boyer-Moore, Sunday and Horspool - algorithms, and has the worst case time complexity of O(n*m), average time complexity of O(n) and lower case time complexity of O(n / m), in which n equals the size of the string from where a match is looked for ([source 1: Fredrik Lundh's archived blog](http://web.archive.org/web/20151113000216/effbot.org/zone/stringlib.htm), [source 2: stringobject source code](https://hg.python.org/cpython/file/5444c2e22ff8/Objects/stringobject.c#l1742)). 

From this I can create an estimate of the total time complexity as in each index of the content-string this search if concluded. Thus a rough worst case time complexity would be O(k * m * n * n) = O(k * m * n^2), in which
- k = characters in content that is compressed
- m = characters in sliding window
- n = characters in lookahead buffer

The power of two for the n comes from the lookahead buffer being looked through iteratively until the longest match is found. On average only a few iterations are gone through, but in a worst case scenario n iterations are performed. I estimate that in an average case the time complexity is more closer to O(k * m)

As for the space complexity of LZ77 I currently have very flimsy understanding. It is my understanding after looking at Python's str source code that in my implementation find creates a window and buffer sized copies of the string with each iteration, in which case O(k * m + k * n) strings are created. On top of that a tuple for the compressed content and later a binary version of the content are created. 

I would greatly appreciate any feedback on how to proceed with these time and space complexity estimations. 

### Pylint and ignore
I propose adding two things to Pylint's ignore list:
- R0902: Too many instance attributes (11/8) (too-many-instance-attributes)
  - In the entities classes I have 11 instance attributes and I propose that refactoring them perhaps isn't that crucial considering the objectives of this course. Can I ignore theses issues? 
- W0703: Catching too general exception Exception (broad-except)
  - The manual extensive tests have a broad except to catch some information in the events that the compression fails for any given reason. I propose that given the scope of this project this is useful, as the compression works with limited character set and tests can easily fail in different ways due to a file containing unsupported characters. Or should I try to diagnose the most common errors and create more specific exceptions? 

## Pylint and Pytest - status update
Most Pylint issues have been addressed and at the time of writing this Pylint-score is 9.89. Five open issues exists. In the previous section I had a question regarding couple of these issues. At the moment of writing the branch coverage is at 86 percent. Especially the service classes need more extensive tests. Now that the algorithms are more optimized, I can next week write tests for even larger files. 

![Coverage-report](images/coverage-report-week-5.png)

## Next steps
- Improve tests
- Refactor code 
- Fix open Pylint issues
- Try to improve compression ratio for both algorithms. 

## Study hours for week #4

| Date (dd/mm/yyyy) |Task | Hours |
| ---- | ---- | ---- |
| 8.6.2022 | Re-read the original article on LZ77 | 2 |
| 9.6.2022 | Peer-review | 3,5 |
| 10.6.2022 | Read multiple articles on LZ77 to find solutions for optimation | 2,5 |
| 11.6.2022 | Create more test material for more extensive testing | 1 |
| 10.6.2022 | Optimize LZ77 by creating strings in a more sensible way | 0,5 |
| 11.6.2022 | Optimize LZ77 string match search | 2 |
| 11.6.2022 | Study time complexity of LZ77 | 1 |
| 11.6.2022 | Write documentation | 0,5 |
| 11.6.2022 | Fix Pylint issues | 1,5 |
| 11.6.2022 | Test that everything works after refactoring on local and university VM | 0,5 |
| 11.6.2022 | Update testing and execution documentations | 0,5 |
| **total**| ---- | **15,5** |
