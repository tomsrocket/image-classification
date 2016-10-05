Image Classification with SVM
=============================

Train a classiefier based on two directories with images. Based on http://www.ippatsuman.com/2014/08/13/day-and-night-an-image-classifier-with-scikit-learn/

Sourcecode can be found at https://github.com/tomsrocket/image-classification


Download example logo files
---------------------------

This is an example set of bash commands that can be used to download logos from the homepage of Brandon Gaille:  

1. Download the index file, e.g.

        wget http://brandongaille.com/category/logos/

2. Extract urls of the good pages

        grep -oP 'http[^"]*logo[^/"]*/' index.html | uniq | sort > filelist.txt

3. Download the logo files

       wget -P logos-incoming/ -r -l 1 -w 0.1 -nd -A Company-Logo.jpg -i filelist.txt

4. Get more logos from Logopedia http://logos.wikia.com/wiki/Logopedia

        This is your homework. :-)

Or check out the really cool scraper that was written by
* Simon Schrader
* https://twitter.com/der_simon
* http://simon-schraeder.de/


Download "other" images
-----------------------

Download mid resolution images from gratisography.com:

1. Download index file:

        wget http://gratisography.com/

2. Download all images that match the filename pattern "pictures*.jpg":

        grep -oP 'pictures[^"]+jpg' index.html | xargs -i wget http://gratisography.com/{}


Download images from pixabay

1. wget --header="Accept: text/html" --user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0" 'https://pixabay.com/de/photos/?image_type=photo&cat=&min_width=&min_height=&q=kaffee&order='

2. grep -oP '\/static\/uploads[^.]+_340.jpg' index.html | xargs -i wget --header="Accept: text/html" --user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0" https://pixabay.com{}

Install Jupyter
---------------

1. Install Anaconda https://www.continuum.io/downloads
2. Change to the directory with the image classification presentation and run the jupyer notebook aplication:  

        cd jupyter-notebook
        jupyter notebook

# How to build a Jupyter notebook

## Useful information & links

* Magic commands for code cells https://ipython.org/ipython-doc/3/interactive/magics.html
        %load filename.py => copy file content into current cell
        %run filename.py => run file in background, declared methods can be used in scope of notebook

* If you want to commit your ipynb files, choose "clear data and restart kernel" inside jupyter,
  so that the outputs will be cleared from the notebook files.

* Doing a presentation? Keep an eye on the time: http://www.timer-tab.com/


## iPython example code snippets

* display images from a directory by using html output:

```
from IPython.core.display import display, HTML
from os import listdir
from os.path import isfile, join

mypath = "logos/"
images = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]
string = '<h1>' + str(len(images)) + " Logos in directory</h1>";

for image in images:
    string += '<img style="float:left;width:100px;height:70px;oveflow:hidden" src="' +  image + '"</h1>';
display(HTML(string))
```

Run the image classifier
------------------------

Change to the directory "hackathon/", then run the following command. It will show usage information.

    python image_classification.py
