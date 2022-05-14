# Weekly Report #1

## Quick recap on progress

* Initial requirements specification created, including
  * topic for the project
  * initial proposal for algorithms to be used
  * programming language to be used  
* Project and remote repository created
* Signed into labtool, added link to Github


## What have I done this week?
I made a conscious choice to prioritize last courses of period IV this week (last course has a deadline on Sunday). I give my word to make up for any missing hours next week. With that said, I personally am satisfied with what I have accomplished this week. 

Choosing the topic was the most difficult thing on this first week. There were so many exciting possibilities and I spent a long time on thinking about pros and cons of different decisions. At the moment I have a feeling that for example path finding algorithms could prove very useful later on in my future professional career. Should I focus on them to get as much experience on something that could perhaps be useful later on? On the other hand music has always been a part of my life. Should I use this opportunity to create something that could provide value to my dear hobby? Or should I use this opportunity to study something that interests me academically, even if I am uncertain of what future use I'd have for that knowledge? 

I opted to choose the last one and focus on data compression algorithms. It is a topic that has long fascinated me and I wanted to take this opportunity to understand a bit more about how they work. At the moment I am uncertain, whether this knowledge will be professionally useful in the future, but I try to keep my mind open right now and to pursue topics that fascinate and motivate me. My reasoning is that I am already highly motivated on investing time on studying path finding algorithms and I will find opportunities to study that. I might, however, miss out on learning about data compression if I didn't use one of the available opportunities to put time and effort on a fascinating topic that may or may not prove useful later on. 

This week I have studied about data compression and scraped the surface on the fascinating topic. I have decided that my project will focus on lossless data compression. In the course material a comparison of Huffman vs. Lempel-Ziv was given as an example of a good scope for this project and I decided to start by looking into these two algorithms.

During this first week I have created a project and a remote repository to GitHub. I have to best of my knowledge and understanding fulfilled included everything that was asked to the  requirements specification documentation. 

I have also initialized Poetry and added Pylint, Pytest, Invoke and Coverage for future purposes. 

## How has the application progressed?
This week the core content application has not yet progressed. I did however create an initial template for the GUI, which can already be tested by downloading the project. I used my previous work from the OhTe-course to setup the main layout, menu structure and theme configuration that I personally created this spring. I considered that reusing my own work in this way is acceptable, as the GUI is merely a tool to make focusing on the purpose of this course more convenient. 

I have made an initial proposal for the application structure, which can be found in the [architecture](architecture.md) documentation. 

## What did I learn during this week / today?
I scraped the surface on lossless compression and learned a little on the history of the Huffman coding and LZ77. I also got a basic understanding on how these two algorithms / approaches work, and that they are rarely used on their own, but rather as 'tools' to tackle a part of a more complex task. I learned a little bit about DEFLATE that combines the two before mentions algorithms. If there is time, it'd be fantastic to implement that as well into this project! 

## What remained unclear or caused difficulties? 
I am at this time uncertain on whether I chose a good starting point for this project. It was relatively easy to find pseudocode examples of the two algorithms I propose focusing on (Huffman coding, LZ77), but I do not yet understand the functionalities of these algorithms well enough to fully understand, whether the pseudocode examples I first found are optimal or not. I still need to do a lot of research. 

At the moment I am struggling with understanding the time and space complexities of these algorithms. I have detailed my current understanding in the 'requirements specification' document and would very much appreciate feedback on the content. Also I would like to hear feedback on whether the scope of my project is good for this course, taking in to consideration that my goal is the get a good grade (preferrably a 5). 

To sum up
* I would like to setup an online meeting to get guidance
* I am uncertain on the time and space complexities 
* is the scope good for this project? 
* tips on good and well regarded sources would be very welcome

## Next steps
During next week I will start building the application and first versions of the algorithms selected for this project. The initial idea is to have first working versions of the algorithms ready for use and GUI-features that enable trying out the implementation of the algorithms. 


| Date (dd/mm/yyyy) |Task | Hours |
| ---- | ---- | ---- |
| 9.5.2022 | Course introduction lecture | 2 |
| 9.5.2022 | Thinking about all the exciting topics while unable to fall asleep.  | 0,5|
| 10.5.2022 | Choosing a topic. Reading about data compression | 2 |
| 11.5.2022 | Reading about Huffman coding and LZ77 | 1 |
| 12.5.2022 | Creating project, Github repository, signup to Labtool | 2 |
| 12.5.2022 | Studying algorithms, writing documentation | 1,5 |
| 14.5.2022 | Studying algorithms, writing documentaiton | 3 |
| ---- | ---- | ---- |
| **total**| ---- | **12** |
