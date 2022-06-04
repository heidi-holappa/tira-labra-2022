# General Structure
The general structure of the application can be overviewed in the [how-to-guide](how-to-guide.md).

# Accomplished Time and Space Complexities 
It is still needed to analyze how well my implementations match the original algorithms to get a better understanding of the time complexity. Below are initial observations. 

### Lempel-Ziv 77 
The Lempel Ziv compression algorithm goes through the whole content once. At each index a search is executed, where string content for the length of the window is looked through. Each index in the window is compared to the first index of the lookahead buffer. If they are a match, then the lookahead buffer is iteratively looked through for the length of the match. In the worst scenario the who content consists of one character (i.e. "AAA...A"). In such a case in each step the window and the lookahead buffer are all looked through, thus the time complexity being (content * window * lookahead buffer). 

In uncompression content is added to the end of the string iteratively. If a match exists, it is looked for in the existing string. Otherwise the next character is available in the stored data. In the worst case a match of the length of the buffer is found at every index > buffer size. In this scenario for each step a buffer lenght of sting data is copied and added to the end of the string. 

### Huffman coding
The huffman coding consists of different steps that have different time complexities. 
- Calculating frequencies (iterative loop with constant time calculations)
- Building of minimum heap
- Creating storable Huffman tree with a recursive function
- In the uncompression phase the Huffman tree is traversed. The tree is not balanced, but the path lengths are based on probabilities (frequencies) of characters. I will need to investigate the time complexity of this operation. 

# Performance and O-analysis comparison
As written above, this is still under investigation.

# Known Quality Issues and Suggestions for Improvement
- Especially Lempel-Ziv 77 needs optimization. Have to investigate how to optimize it within the specifications of original LZ77 structure. 
- Data manipulation to byte form is quite naive due to lack of experience. The efficiency issues are most clearly visible in the LZ77 uncompression phase.
- Code needs refactoring and cleaning up. Repetitive code, confusing design choices.
- GUI needs more work
- More extensive tests need to be written. Preferably also graphical representations of results.
- Currently only printable ASCII-charcters can be handled:
```
'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
```



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