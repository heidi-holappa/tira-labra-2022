# General Structure
The general structure of the application can be overviewed in the [how-to-guide](how-to-guide.md).

# Accomplished Time and Space Complexities 
It is still needed to analyze how well my implementations match the original algorithms to get a better understanding of the time complexity. Below are initial observations. 

### Lempel-Ziv 77 
The Lempel Ziv compression algorithm goes through the whole content once. At each index a search is executed, where string content for the length of the window is looked through. Matches for the length between 3 to buffer size are looked for iteratively with Python's built-in str.find() method. The process is repeated for each index of the content n that is being compressed, so the time complexity is n * search time. 

Based on Python's documentation this method uses Boyer-Moore, Sunday and Horspool - algorithms, and has the worst case time complexity of O(n*m), average time complexity of O(n) and lower case time complexity of O(n / m), in which n equals the size of the string from where a match is looked for ([source 1](http://web.archive.org/web/20151113000216/effbot.org/zone/stringlib.htm), [source 2](https://hg.python.org/cpython/file/5444c2e22ff8/Objects/stringobject.c#l1742)). 

From this an estimate of the total time complexity can be created. A rough worst case time complexity would be O(k * m * n * n) = O(k * m * n^2), in which
- k = characters in content that is compressed
- m = characters in sliding window
- n = characters in lookahead buffer

In uncompression content is added to the end of the string iteratively. If a match exists, it is looked for in the existing string. Otherwise the next character is available in the stored data. In the worst case a match of the length of the buffer is found at every index > buffer size. In this scenario for each step a buffer lenght of sting data is copied and added to the end of the string. This takes O(n) of time, where n is the number of characters in the uncompressed content. 


### Huffman coding
The huffman coding consists of different steps that have different time complexities. 
- Calculating frequencies (iterative loop with constant time calculations)
- Building of minimum heap
- Creating storable Huffman tree with a recursive function
- In the uncompression phase the Huffman tree is traversed. The tree is not balanced, but the path lengths are based on probabilities (frequencies) of characters. I will need to investigate the time complexity of this operation. 

# Performance and O-analysis comparison
As written above, this is still under investigation.

# Known Quality Issues and Suggestions for Improvement
- Data manipulation to byte form is quite naive due to lack of experience. The efficiency issues are most clearly visible in the LZ77 uncompression phase. Also the compression ratio is affected by this. 
- More extensive tests need to be written. Preferably also graphical representations of results.
- Currently only printable ASCII-charcters can be handled:
```
'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
```
In addition following characters can be handled:
- (32) # whitespace
- (10) # line-break
- (228) # ä
- (196) # Ä
- (197) # Å
- (229) # å
- (246) # ö
- (214) # Ö

# Sources

**Huffman coding:**  
[1] Geeks for Geeks' [article](https://www.geeksforgeeks.org/huffman-coding-greedy-algo-3/) on Huffman coding  
[2] Microsoft Documentation: [2.1.4.2 Huffman Code Construction Phase](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-xca/35a83e96-981d-48ed-a4eb-0b9cc6b51440)  
[3] Wikipedia: [Huffman coding](https://en.wikipedia.org/wiki/Huffman_coding)  
[4] John Morris: [Huffman encoding](https://www.cs.auckland.ac.nz/software/AlgAnim/huffman.html) 
[5] Stack Overflow: [Storing Huffman tree](https://stackoverflow.com/questions/759707/efficient-way-of-storing-huffman-tree)
  
**LZ77**  
[6] Towards Data Science: [How data compression works: Exploring LZ77](https://towardsdatascience.com/how-data-compression-works-exploring-lz77-3a2c2e06c097)  
[7] Microsoft Documentation: [2.1.1.1.1 LZ77 Compression Algorithm](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-wusp/fb98aa28-5cd7-407f-8869-a6cef1ff1ccb)  
[8] Wikipedia: [LZ77 and LZ78](https://en.wikipedia.org/wiki/LZ77_and_LZ78)  
[9] PADS: [Practical Algorithms and Data structures on Strings](https://www.cs.helsinki.fi/group/pads/)  
[10] Kempa, Dominik, and Dmitry Kosolobov. “LZ-End Parsing in Linear Time.” (2017): n. pag. Print.  
[11] Kosolobov, Dmitry. “Relations Between Greedy and Bit-Optimal LZ77 Encodings.” (2018): n. pag. Print.  
[12] Professor Blelloch, Guy. Lecture slides from course "Algorithms in the 'Real World'": https://www.cs.cmu.edu/~guyb/realworld/slidesF08/suffixcompress.pdf  
  
**General**  
[13] Cormen, Thomas H. Introduction to Algorithms. 3rd ed. Cambridge, Mass: MIT Press, 2009.  
[14] Salomon, D. (David). A Concise Introduction to Data Compression. London: Springer, 2008. Print.  
[15] Sayood, Khalid. Introduction to Data Compression. 3rd ed. Amsterdam ;: Elsevier, 2006. Print.  
[16] Salomon, Daṿid, and Giovanni Motta. Handbook of Data Compression. 5th ed. 2010. London: Springer London, 2010. Web.  

**Video-sources**  
[17] Computerphile: [Elegant compression in Text (the LZ 77 method)](https://youtu.be/goOa3DGezUA)  
[18] Google Developers: [The LZ77 Compression Family](https://youtu.be/Jqc418tQDkg)  
[19] Tom Scott: [How Computers Compress Text: Huffman coding and Huffman Trees](https://youtu.be/JsTptu56GM8)  
[20] Computerphile: [How Huffman Trees Work](https://youtu.be/umTbivyJoiI)
[21] Google Developers: [Compressor Head - series](https://youtu.be/Eb7rzMxHyOk)

**Python-specific**
[22] [Source code for object str](https://hg.python.org/cpython/file/5444c2e22ff8/Objects/stringobject.c#l1742)
[23] [An archived blog post by Frederik Lundh](http://web.archive.org/web/20151113000216/effbot.org/zone/stringlib.htm) 