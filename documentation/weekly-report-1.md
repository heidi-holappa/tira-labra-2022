# Weekly Report #1

## Quick recap on progress

* Initial requirements specification created, including
  * topic for the project (lossless compression)
  * initial proposal for algorithms to be used (Huffman coding & LZ77)
  * programming language to be used (Python)
  * language to be used in documentation and code (English)
  * Initial sources
* Project and remote repository created
* Signed into labtool, added link to Github repository
* Weekly report #1 written


## What have I done this week?
I made a conscious choice to prioritize last courses of period IV this week (last course has a deadline tomorrow on Sunday). I give my word to make up for any missing hours next week. With that said, I personally am satisfied with what I have accomplished this week.

Choosing the topic was the most difficult thing on this first week. There were so many exciting possibilities and I spent a long time on thinking about pros and cons of different decisions. At the moment I have a feeling that for example path finding algorithms could prove very useful later on in my future professional career. Should I focus on them to get as much experience on something that could perhaps be useful later on? Or should I use this opportunity to study something that interests me academically, even if I am uncertain of what future use I'd have for that knowledge?

I opted to focus on data compression algorithms. It is a topic that has long fascinated me and I wanted to take this opportunity to understand the basics on how lossless data compression works. My reasoning is that I am already highly motivated on investing time on studying path finding algorithms and I will find opportunities to study that. I might, however, miss out on learning about data compression if I didn't use one of the available opportunities to put time and effort on a fascinating topic that may or may not prove useful later on. 

This week I have studied about data compression and scraped the surface on the fascinating topic. I have decided to propose a project that focuses on lossless data compression. In the course material a comparison of Huffman vs. Lempel-Ziv was given as an example of a good scope for this project and I decided to start by looking into these two algorithms.

During this first week I have created a project and a remote repository to GitHub. I have also initialized Poetry and added Pylint, Pytest, Invoke and Coverage for future purposes. I have to best of my knowledge and understanding fulfilled all tasks given for week one.  

## How has the application progressed?
This week the core content application has not yet progressed. I did however create an initial template for the GUI, which can already be tested by downloading the project. I used my previous work from the OhTe-course to setup the main layout, menu structure and theme configuration that I personally created this spring. I considered that reusing my own work in this way is acceptable, as the GUI is merely a tool to make focusing on the purpose of this course more convenient. 

I have made an initial proposal for the application package structure, which can be found in the [architecture](architecture.md) documentation. 

## What did I learn during this week / today?
I scraped the surface on lossless compression and learned a little on the history of the Huffman coding and LZ77. I also got a basic understanding on how these two algorithms / approaches work, and that they are rarely used on their own, but rather as 'tools' to tackle a part of a more complex task. I learned a little bit about DEFLATE that combines the two before mentions algorithms. If there is time, it'd be fantastic to implement that as well into this project! 

## What remained unclear or caused difficulties? 

At the moment I have three main areas on which I would like to get guidance. I would very much like to have an online meeting to go through these. 

### Is this a good starting point for the project? 
I am at this time uncertain on whether I chose a good starting point for this project. Data compression is a topic I am not familiar with and I would like to learn the basics of lossless data compression. For this reason I wanted to focus on these two well known algorithms. It was relatively easy to find pseudocode examples of the two algorithms I propose focusing on (Huffman coding, LZ77), but I do not yet understand the functionalities of these algorithms well enough to fully understand, whether the pseudocode examples I first found are optimal or not. I still need to do more research. 

### Time and space complexities
At the moment I am struggling with understanding the time and space complexities of these algorithms. I have detailed my current understanding in the 'requirements specification' document and would very much appreciate feedback on the content. Also I would like to hear feedback on whether the scope of my project is good for this course, taking in to consideration that my goal is the get a good grade (preferrably a 5). 

### Compression ratio
Based on initial reading the compression ratio of Huffman coding is approximately 1,5:1. For the project a compression ratio greater than 1.67:1 is preferrable. I am unclear on how I should approach this objective if my project focuses on comparing Huffman coding and LZ77. Should I search for ways to optimize the algorithms? 


**To sum up**
* I would like to setup an online meeting to get guidance
* I am uncertain on the time and space complexities 
* is the scope and objectives good for this project
* if my objective is to compare two historical compression algorithms, should the compression ratio still be 40-60 percent (greater than 1.67:1)
* tips on good and well regarded sources would be very welcome

## Next steps
During next week after receiving feedback on my project proposal I will either start building the application and first versions of the algorithms selected for this project or to work on a refined project proposal. The initial idea is to have first working versions of the chosen algorithms ready for use and GUI-features that enable trying out the implementation of the algorithms. I will also begin writing automated tests. 

I propose that I exclude GUI-classes from the automated tests as was done in the OhTe-course.  

| Date (dd/mm/yyyy) |Task | Hours |
| ---- | ---- | ---- |
| 9.5.2022 | Course introduction lecture | 2 |
| 9.5.2022 | Thinking about all the exciting topics while unable to fall asleep.  | 0,5|
| 10.5.2022 | Choosing a topic. Reading about data compression | 2 |
| 11.5.2022 | Reading about Huffman coding and LZ77 | 1 |
| 12.5.2022 | Creating project, Github repository, signup to Labtool | 2 |
| 12.5.2022 | Studying algorithms, writing documentation | 1,5 |
| 14.5.2022 | Studying algorithms, writing documentation | 3 |
| 14.5.2022 | Writing documentation, reading source material | 2 |
| ---- | ---- | ---- |
| **total**| ---- | **14** |
