# Requirements specification

## Purpose of the application
This application was build as a university computer science laboratory project to study the operation of lossless data compression. 

## Programming language used
The application is built with Python. Poetry is used for dependency management and packaging. 

## Study program (degree education)
Bachelor's Programme in Computer Science and Master's Programme (3 years + 2 years) 

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

## The time and space complexities

The time complexity of Huffman coding is $O(n \log n)$ according to the Wikipedia article and the Geeks for Geeks article (links below). I do however want to verify this from a more trusted source during the project. 

Based on initial study it seems that several different time and space complexities can be achieved for LZ77, depending on the execution. Based on the sources it is possible to achieve $O(n)$ and to best of my understanding $O(n \log n)$ could be achievable with a simpler design as well. 




### Additional sources

Huffman coding:
* Geeks for Geeks' [article](https://www.geeksforgeeks.org/huffman-coding-greedy-algo-3/) on Huffman coding
* Microsoft Documentation: [2.1.4.2 Huffman Code Construction Phase](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-xca/35a83e96-981d-48ed-a4eb-0b9cc6b51440)
* Wikipedia: [Huffman coding](https://en.wikipedia.org/wiki/Huffman_coding)
* John Morris: [Huffman encoding](https://www.cs.auckland.ac.nz/software/AlgAnim/huffman.html)


LZ77
* Towards Data Science: [How data compression works: Exploring LZ77](https://towardsdatascience.com/how-data-compression-works-exploring-lz77-3a2c2e06c097)
* Microsoft Documentation: [2.1.1.1.1 LZ77 Compression Algorithm](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-wusp/fb98aa28-5cd7-407f-8869-a6cef1ff1ccb)
* Wikipedia: [LZ77 and LZ78](https://en.wikipedia.org/wiki/LZ77_and_LZ78)
* PADS: [Practical Algorithms and Data structures on Strings](https://www.cs.helsinki.fi/group/pads/)