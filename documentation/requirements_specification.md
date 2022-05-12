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
