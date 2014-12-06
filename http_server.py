#Copyright Jon Berg , turtlemeat.com
import subprocess
import re
import urllib
import string,cgi,time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
#import pri

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            #if self.path.endswith(".html"):

            self.send_response(200)
            self.send_header('Content-type',    'text/html')
            self.end_headers()
            parse_domain = self.path[1:]
            if parse_domain != "":
                return self.html_download( parse_domain )
            self.wfile.write("hey, today is the" + str(time.localtime()[7]))
            self.wfile.write(" day in the year " + str(time.localtime()[0]))
            return
                
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)


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
