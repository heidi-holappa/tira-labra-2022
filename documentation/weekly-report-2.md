# Weekly Report #2

## Quick recap on progress

## What have I done this week?
I was unfortunate to catch a flu previous weekend and was on a sick leave from work for the whole week. I did my best to put energy into the project and am once again satisfied with what I have done under the circumstances. Looking forwarded next week, hopefully without a flu and with time and energy to fully commit to this project. The biggest thing for me this week has been the growing excitement while learning more on data compression. So far this has been the favorite course I have taken. I feels great to have such passionate feelings on a subject one is studying! 

On a more conrete level I read more on the Huffman coding and built a first version of the algorithm. I did struggle quite a bit with understanding the algorithm fully, but I think I have a good understanding of the basic functionalities now. I also created first functionalities in the GUI. I had to learn on how to use filedialog (file explorer) in Tkinter and it was a great new thing to learn! A user can now compress / uncompress files from the GUI. 

To make testing easier, files can also be compressed/uncompressed directly from huffman.py file.


## How has the application progressed?
* Initial version of Huffman coding algorithm is implemented
* txt-files with ASCII (256) coded content can be compressed and uncompressed
* compressed files have ".huf" as an extension
* An initial simple analysis file is created on compression results. 
* The GUI has first working functionalities
* The application has extensive docstring
* The application now uses dotenv for easier configuration

## What did I learn during this week / today?
I learned a lot more on Huffman coding and know now how to proceed with that part of this project. I also learned a new useful skill for GUI - creation (how to open file explorer to read files). 

## What remained unclear or caused difficulties? 
I still need to improve the Huffman algorithm in multiple ways. Currently it only handles .txt-files with ASCII 256 content. I would like to look into how to make the algorithm a bit more universal. 

The other big issue to solve is storing the huffman tree. I had trouble finding good material, most likely because I did not fully understand what search terms to use. I asked for sources on good tutorials on the subject at the Telegram channel and got a very good tip. The tutorial had a lot of good vocabulary so I am confident that finding more tutorials on the topic will be easier! 

## Next steps
* Build initial version of Lempel-Ziv 77 algorithm
* Improve Huffman coding
* Integrate compression analysis into the GUI. 


## Study hours for week #2

| Date (dd/mm/yyyy) |Task | Hours |
| ---- | ---- | ---- |
| 17.5.2022 | Reading up on Huffman coding  | 2 |
| 18.5.2022 | Start building first version of Huffman code  | 2 |
| 19.5.2022 | Finish first working version of Huffman code | 3 |
| 20.5.2022 | Create GUI functionalities, learn to use filedialog | 2 |
| 20.5.2022 | Create initial service class for compression, refactor entities class | 1 |
| 20.5.2022 | Write initial how-to-guide, test application on university virtual machine. | 0,5 |
| **total**| ---- | **10,5** |
