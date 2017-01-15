from __future__ import unicode_literals

from flask import Flask, request, send_file, send_from_directory, stream_with_context, Response
import unicodedata
import subprocess
import os
import re
import urllib
from socket import gethostname

def decode(text, encoding='utf-8', normalization='NFC'):
    """Return ``text`` as normalised unicode.
    :param text: string
    :type text: encoded or Unicode string. If ``text`` is already a
        Unicode string, it will only be normalised.
    :param encoding: The text encoding to use to decode ``text`` to
        Unicode.
    :type encoding: ``unicode`` or ``None``
    :param normalization: The nomalisation form to apply to ``text``.
    :type normalization: ``unicode`` or ``None``
    :returns: decoded and normalised ``unicode``
    """
    # convert string to Unicode
    if isinstance(text, basestring):
        if not isinstance(text, unicode):
            text = unicode(text, encoding)
    # decode Cocoa/CoreFoundation Unicode to Python Unicode
    if re.search(r'\\U\d{3,}', text):
        text = text.replace('\\U', '\\u').decode('unicode-escape')
    return unicodedata.normalize(normalization, text)

def run(query=''):
    '''Takes a query string, searches using mdfind
    normalizes returned vaule to unicode
    returns the list
    '''
    cmd = ['mdfind', query]
    # open pipes
    proc = subprocess.Popen(cmd,
                            shell=False,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    os.environ['LANG'] = 'en_US.UTF-8'
    stdout, stderr = proc.communicate()
    output = filter(None, [s.strip()
                           for s in decode(stdout).split('\n')])
    return htmlize(output)

def shrink(text):
    ''' thisislongtext.pdf ==> thisis...'''
    if len(text) < 60:
        return text
    else:
        return text[:57] + '...'

def htmlize(output=[]):
    '''Takes a list of file paths, returns a html page with the list values as links
    '''
    page = '''<style>
        .center { margin: auto;}
        #list4 { width:720px; font-family:Georgia, Times, serif; font-size:15px; }
        #list4 ul { list-style: none; }
        #list4 ul li { }
        #list4 ul li a { display:block; text-decoration:none; color:#000000; background-color:#FFFFFF; line-height:30px;
  border-bottom-style:solid; border-bottom-width:1px; border-bottom-color:#CCCCCC; padding-left:10px; cursor:pointer; }
        #list4 ul li a:hover { color:#FFFFFF; background-color:#1c73ed; background-repeat:repeat-x; }
        #list4 ul li a strong { margin-right:10px; }
    </style></head>
    <body><div id="list4" class='center'>
   <ul><li><a href=/download?filename=><h1><strong>Results</strong></h1></a></li>'''
    page += ''.join(['<li><a href=/download?filename=' + urllib.quote_plus(i.encode('utf8')) + ' title="' + os.path.basename(i) + '">' + shrink(os.path.basename(i)) + "</a></li>" \
                     for i in output])
    page += "</ul></div>"
    return page

app = Flask(__name__)

@app.route('/')
def searchBarPage():
    page = '''
<html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="/js/jquery.min.js"></script>
    <style>
        .elements {
           float: center;
        }
    </style>
    </head>
    <body>
    <form class="elements" id="searchbar" action="search" method="get">
        <input placeholder=''' + gethostname() + ''' type="text" name="q" size="100%" style="font-size:25px" >
        <input type="submit" style="visibility: hidden;" />
    </form>
    <div class="elements" id=results></div>
    <script>
    $('#searchbar').submit(function() { // catch the form's submit event
        $.ajax({ // create an AJAX call...
            data: $(this).serialize(), // get the form data
            type: $(this).attr('method'), // GET or POST
            url: $(this).attr('action'), // the file to call
            success: function(response) { // on success..
                $('#results').html(response); // update the DIV
            }
        });
        return false; // cancel original event to prevent form submitting
    });
    </script>
    </body></html>
    '''
    return page


@app.route('/search')
def search():
    q = request.args.get('q')
    return run(query=q)

@app.route('/download')
def getFile():
    filename = request.args.get('filename')
    filename = urllib.unquote_plus(filename)
    filename = filename.decode('utf8')
    if os.path.isfile(filename):
        return send_file(filename)
    elif os.path.isdir(filename):
        return "You clicked on a directory. Cannot render directories"
    else:
        return "File not found"

@app.route('/js/<path:path>')
def send_js(path):
    '''locally cache jquery'''
    return send_from_directory('js', path)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
