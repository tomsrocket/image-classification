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

        grep -oR 'http[^"]*logo[^/"]*/' index.html | uniq | sort > filelist.txt

3. Download the logo files

       wget -P logos-incoming/ -r -l 1 -w 0.1 -nd -A Company-Logo.jpg -i filelist.txt

Or check out the really cool scraper that was written by
* Simon Schrader
* https://twitter.com/der_simon
* http://simon-schraeder.de/


Download example other images
-----------------------------

Download mid resolution images from gratisography.com:

1. Download index file:

        wget http://gratisography.com/

2. Download all images that match the filename pattern "pictures*.jpg":

        grep -oP 'pictures[^"]+jpg' index.html | xargs -i wget http://gratisography.com/{}


Install Jupyter
---------------

1. Install Anaconda https://www.continuum.io/downloads
2. In your favorite directory run:  

        jupyter notebook

# Build a Jupyter notebook

## Useful links:

* Magic commands for code cells https://ipython.org/ipython-doc/3/interactive/magics.html


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
