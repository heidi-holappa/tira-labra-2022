# Installation

Begin by downloading the project from GitHub. During the project stable releases will be published. Before the first release the project can be cloned. 

Install dependencies with the following command:
```
poetry install
```

Run the application with the following command:
```
poetry run invoke start
```

# How to Use the Application

Run the application with the command `poetry run invoke start`. The application start with a main screen

## Main view

![Main view](images/how-to-guide-main-view.png)

From the menu a user can 
* exit the application
* access help - documentation
* view app infomartion

From the button `compress / uncompress data` user can access compression view. 

## Data compression view
At the moment data can be compressed and uncompressed with an initial Huffman coding algorithm.  

![Compression view](images/how-to-guide-compression-view.png)

Start by selecting either an uncompressed txt-file or compressed huf-file. Two example txt-files are included for more convenient testing experience.  

A compressed file is created into the same directory. At the moment the Huffman tree is unefficiently stored as integer-values (and a character separator ';'). This will change as the project progresses. 

![An example of compressed file](images/how-to-guide-huffman-compressed.png)

Additionally a log-file containing initial information on the compression is created. 

![Log-file](images/how-to-guide-huffman-analysis.png)

## Configuration
The application uses dotenv for configuration. User can change the default folder used in File Explorer. 


# How To Run Tests

Miten ohjelma suoritetaan, miten eri toiminnallisuuksia käytetään
Minkä muotoisia syötteitä ohjelma hyväksyy
Missä hakemistossa on jar ja ajamiseen tarvittavat testitiedostot.