#Copyright Jon Berg , turtlemeat.com
import subprocess
import re
import urllib
import string,cgi,time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
#import pri
import os
import sys

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if ( self.path.endswith(".css") or self.path.endswith(".jpg") ):
                f = open(curdir + sep + self.path) #self.path has /test.html
                self.send_response(200)
                self.send_header('Content-type',  'text/html' if self.path.endswith(".css") else "image/jpg" )
                self.end_headers()
                self.wfile.write( f.read() )
                f.close()

            else: 

                self.send_response(200)
                self.send_header('Content-type',    'text/html')
                self.end_headers()

                self.wfile.write( "<link href=\"styles.css\" rel=\"stylesheet\" type=\"text/css\">" )

                if self.path.endswith("test"):
                    for root, _, files in os.walk("/data/git/image-classification/testdata"):
                        for file_name in files:
                            file_path = os.path.join(root, file_name)
                            response = subprocess.check_output("python image_classification.py image \""+ file_path +"\"", shell=True)
                            m = re.search('\[(.)\].*image:\s(.*)$', response)
                            print( response )
                            img_url = m.group(2)
                            is_logo = m.group(1)


                            self.wfile.write( "<div class=\"res result"+is_logo+"\"><img src=\"testdata/" +  file_path[40:] + "\" /></div>" )
                            sys.stdout.flush()

                    return


                else: 
                    parse_domain = self.path[1:]
                    if parse_domain != "":
                        return self.html_download( parse_domain )
                    self.wfile.write("This is your company logo download service<br /><br />try <a href=\"/test\">/test</a> to show results of image classification with SVM. (it will show testresults for all images in the subdirectory 'testdata/' and its subdirs)" )
                    self.wfile.write("<br />try <a href=\"/www.lego.com\">/www.lego.com</a> any domain to extract the logo of that domain. Check the A.I. response to see what the SVM thinks of it: [1] = it is a logo, [0] = it is not a logo." )
            return
                
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)




    def run_tests( self ):


        return



    def html_download( self, url ):
        url = "http://" + url 
        self.wfile.write("<br />fetching url: " + url )
        fp = urllib.urlopen(url)
        try:
            html_data = fp.read()
        finally:
            fp.close()

        img_url = ""
        #m = re.search('<[^>]*logo[^>]*>', html_data)
        for m in re.finditer('<[^>]*logo[^>]*>', html_data):
            img_tag = m.group()
            self.wfile.write( "<br />potential image: " + img_tag[1:]  )
            m2 = re.search( '(http:\/\/\S+(?:jpg|gif|png)\S*?)["\)]', img_tag )
            if m2:
                img_url = m2.group(1)
                break
            else: 
                m2 = re.search( 'src="([^"]+)"', img_tag )
                if m2:
                    img_url = m2.group(1)
                    break

        if img_url: 

            if img_url[0:1] == "/":
                m2 = re.search( '(https?:\/\/[^\/]+)\/?', url )
                if m2:
                    hostname = m2.group(1)
                    img_url = hostname + img_url

            self.wfile.write( "<br /><br />found image url: " + img_url )
            self.wfile.write( "<br /><br /><img src=\"" + img_url+"\" />" )
            self.wfile.write( "<br /><br />Asking A.I..." )

            response = subprocess.check_output("python image_classification.py url \""+ img_url +"\"", shell=True)
            self.wfile.write("<pre>" + response )

        else: 
            self.wfile.write("<br /><br />nothing found")
        return 
     

def main():
    try:
        server = HTTPServer(('', 8000), MyHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()
