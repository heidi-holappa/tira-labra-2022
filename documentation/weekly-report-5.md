# Weekly Report #5

## Quick recap on progress
- Read a lot and had piffanies
- Created more diverse test material
- Multiple questions for the course assistant below in section "What remained unclear or caused difficulties"


## What have I done this week?
The first days of the week I had to commit to preparing to the exam of Data Structures and Algorithms II, so unfortunately I had no time to work on this project. From the rest of the week I had to spend multiple hours on research this week, but I think it was beneficial! 

## How has the application progressed?
- New test material created

## What did I learn during this week / today?
From reading material I first and foremost learned that LZ77 isn't a compression algorithm, but a model for efficient compression method. The effect is that there is no 'canonical' LZ77 algorithm and instead there is a family of LZ77 adaptations with very different implementations and thus very different time and space complexities. This was the biggest piffany for me as I understood that I've been looking at some questions from a wrong perspective. 

## What remained unclear or caused difficulties? 
This week I have multiple issues I hope to get feedback on:


### Algoritms ineffective with random ASCII-characters

Both algorithms are very uneffective with random ASCII - characters. Often compression ratio ends up being over 100 percent. My thoughts:
- **Huffman coding:** With randomly created character-content the frequencies are close to each other which makes all branches of the Huffman tree long and compression ratio thus poor
- **LZ77:** With randomly created character-content multiple character matches are rarer and compressed content takes more space. 

For LZ77 I think I could optimize the compression by rethinking how the content is stored. I read upon a solution where:
- First bit indicates whether a match was found (1= true, 0= false). 
- If false, then only the next character is stored (one byte), if true the offset and match length are stored. 
- Also some sources suggest limiting the requirement for minimum match length to three characters for better compression time and ratio efficiency

Does this sound like a good approach for LZ77 compression optimization? 

As for Huffman coding I have no ideas at the moment. I have read a bit on 'canonical Huffman tree', but I do not yet understand the concept well enough to know, whether it'd provide any benefits in this particular issue. Any suggestions or hints would be very welcome! 

### Algorithms ineffective with random word content
Both algorithms are sub-optimal with randomly generated words of natural language. I assume the issues are connected to the same reasons as the ones mentioned above. At the moment I am unsure whether this is a limitation of these two method, or is it something I could perhaps optimize. I would very much appreciate any feedback or tips on how to proceed with this. 

### Time and Space complexity for LZ77
As my biggest piffany for this week was that there is no spoon, to quote the famous movie Matrix, meaning that there is no one LZ77 algorithm. This means that I need to now rethink how to argue anything about the time and space complexities of my adaptation.  

One thought that came to my mind is that perhaps I could implement some well known string matching algorithm to my LZ77 compressor. For instance [the Karp-Rabin](http://www-igm.univ-mlv.fr/~lecroq/string/node5.html#SECTION0050) algorithm seems like something I might be able to implement to my solution and it has a defined time complexity.  

Would this be a good approach? 


## Pylint and Pytest - status update

## Next steps

## Study hours for week #4

| Date (dd/mm/yyyy) |Task | Hours |
| ---- | ---- | ---- |
| 8.6.2022 | Re-read the original article on LZ77 | 2 |
| 9.6.2022 | Peer-review | 3,5 |
| 10.6.2022 | Read multiple articles on LZ77 to find solutions for optimation | 2,5 |
| 11.6.2022 | Create more test material for more extensive testing | 1 |
| 10.6.2022 | Optimize LZ77 by creating strings in a more sensible way | 0,5 |
| 11.6.2022 | Optimize LZ77 by keeping pointers instead of making copies of string | 0 |
| **total**| ---- | **9,5** |
