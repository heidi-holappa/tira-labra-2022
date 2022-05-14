# Requirements specification

## Purpose of the application
This application is to be built as a university computer science laboratory project to study the operation of lossless data compression. The initial proposal is to do a comparative study on two well known methods for lossless data compression, Huffman coding and LZ77 (also known as LZ1).

## Language
I will use English language for constructing and documenting this project. Finnish is favored for Labtool correspondence and online guidance sessions. For peer demo sessions either language is good. 

## Programming language used
The application will be built with Python. Poetry is used for dependency management and packaging. 

I have taken the programming courses OhPe and OhJa with Java, so I have the basic knowledge for understanding applications built with Java language. 

## Study program (degree education)
Bachelor's Programme in Computer Science and Master's Programme (3 years + 2 years). Currently I am working on my bSc. 

## Algorithms used
The application provides data compression with two well know algorithms: 
* Dr. Huffman's [Huffman coding](https://en.wikipedia.org/wiki/Huffman_coding) and 
* Professor Lempel's and Professor Ziv's [LZ77](https://en.wikipedia.org/wiki/LZ77_and_LZ78).

### LZ77
A pseudo code for LZ77 can be found in the [Wikipedia article](https://en.wikipedia.org/wiki/LZ77_and_LZ78):

```
while input is not empty do
    match := longest repeated occurrence of input that begins in window
    
    if match exists then
        d := distance to start of match
        l := length of match
        c := char following match in input
    else
        d := 0
        l := 0
        c := first char of input
    end if
    
    output (d, l, c)
    
    discard l + 1 chars from front of window
    s := pop l + 1 chars from front of input
    append s to back of window
repeat
```

### Huffman coding
A pseudocode example for Huffman coding can be found in Professor Alvarez' [notes](http://cs.bc.edu/~alvarez/Algorithms/Notes/huffman.pdf):
```
Input: Array f[1...n] of numerical frequencies or probabilities.
Output: Binary coding tree with n leaves that has minimum expected code length
for f.
huffman(f[1...n])
(1) T = empty binary tree
(2) Q = priority queue of pairs (i, f[i]), i = 1...n, with f as comparison key
(3) foreach k = 1...n − 1
(4) i = extractMin(Q)
(5) j = extractMin(Q)
(6) f[n + k] = f[i] + f[j]
(7) insertNode(T, n + k) with children i, j
(8) insertRear(Q,(n + k, f[n + k]))
(9) return T
```

## The problem to be solved
This project is not set out to solve any unsolved problem, but rather to study two well known lossless compression algorithms. The initial plan is to create an application that provides tools for

* compressing string data with both algorithms
* evaluating run-time and effectiveness of compression

The application will include tools for creating random test material. Application user can also add their own material to test the performance of the algorithms in different scenarios. The objective is to create versatile test material. The 'strenghts and weaknesses' of both algorithms are well documented and the objective is to take these into account while creating test data. 

## The time and space complexities
My initial understanding is that text compression can be done in time complexity $O(n \log n)$ with both Huffman coding and LZ77. I am currently researching the selected algorithms and will possibly update these complexities in the first weeks of the course. 

According to articles on Geeks for Geeks [1] Wikipedia [3] the time complexity of Huffman coding is $O(n \log n)$. Based on initial research there is much more complexity and uncertainty to the time and space complexities of Huffman coding [12,13,14]. According to professor David Solomon [12,14], the average space complexity for Huffman coding is 2.2 bits/symbol, but the best and worst cases have significant variation. 

Based on initial study it seems that variations of LZ77 achieve different time complexities [8,9]. Based on the sources a time complexity of, when certain conditions apply, $O(n)$ is possible to achieve. My current understading is, that the time complexity of the original LZ77 is harded to estimate. The best and worst cases depend i.e. on the size of the buffer window and given data. To best of my current understanding a time complexity of $O(n \log n)$ could be achievable with a relatively simple design as well. I am at the moment uncertain on the big O space complexity of LZ77. 


## Sources (will be later moved to Execution document)

**Huffman coding:**  
[1] Geeks for Geeks' [article](https://www.geeksforgeeks.org/huffman-coding-greedy-algo-3/) on Huffman coding  
[2] Microsoft Documentation: [2.1.4.2 Huffman Code Construction Phase](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-xca/35a83e96-981d-48ed-a4eb-0b9cc6b51440)  
[3] Wikipedia: [Huffman coding](https://en.wikipedia.org/wiki/Huffman_coding)  
[4] John Morris: [Huffman encoding](https://www.cs.auckland.ac.nz/software/AlgAnim/huffman.html)  
  
**LZ77**  
[5] Towards Data Science: [How data compression works: Exploring LZ77](https://towardsdatascience.com/how-data-compression-works-exploring-lz77-3a2c2e06c097)  
[6] Microsoft Documentation: [2.1.1.1.1 LZ77 Compression Algorithm](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-wusp/fb98aa28-5cd7-407f-8869-a6cef1ff1ccb)  
[7] Wikipedia: [LZ77 and LZ78](https://en.wikipedia.org/wiki/LZ77_and_LZ78)  
[8] PADS: [Practical Algorithms and Data structures on Strings](https://www.cs.helsinki.fi/group/pads/)  
[9] Kempa, Dominik, and Dmitry Kosolobov. “LZ-End Parsing in Linear Time.” (2017): n. pag. Print.  
[10] Kosolobov, Dmitry. “Relations Between Greedy and Bit-Optimal LZ77 Encodings.” (2018): n. pag. Print.  
[11] Professor Blelloch, Guy. Lecture slides from course "Algorithms in the 'Real World'": https://www.cs.cmu.edu/~guyb/realworld/slidesF08/suffixcompress.pdf  
  
**General**  
[12] Salomon, D. (David). A Concise Introduction to Data Compression. London: Springer, 2008. Print.  
[13] Sayood, Khalid. Introduction to Data Compression. 3rd ed. Amsterdam ;: Elsevier, 2006. Print.  
[14] Salomon, Daṿid, and Giovanni Motta. Handbook of Data Compression. 5th ed. 2010. London: Springer London, 2010. Web.  

**Video-sources**  
[15] Computerphile: [Elegant compression in Text (the LZ 77 method)](https://youtu.be/goOa3DGezUA)  
[16] Google Developers: [The LZ77 Compression Family](https://youtu.be/Jqc418tQDkg)  
[17] Tom Scott: [How Computers Compress Text: Huffman coding and Huffman Trees](https://youtu.be/JsTptu56GM8)  
[18] Computerphile: [How Huffman Trees Work](https://youtu.be/umTbivyJoiI)