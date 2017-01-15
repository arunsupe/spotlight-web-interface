# spotlight-web-interface
Expose spotlight via a web interface in the LAN

In my home, I have an iMac desktop that acts as the fileserver. I save all my family's digital 
belongings in it. I use OSX's spotlight to index the files for search. As a convenience, I wrote a small 
python script to expose this machine's spotlight to the LAN via a web interface. This way, I can 
search my fileserver using spotlight from anywhere in the LAN using any web browser.

I am an amature at programming and with python. The code does not do any error checking. It 
blocks with each request. It runs in a terminal window (not demonized). I use it purely as a convenience. 
The entire family can now find files named "2015 tax return" or whatever from their laptops. I am putting 
it out there so that anyone who finds it useful may use it. Any help improving it, demonizing it, non-blocking it, 
improving the UI or porting it to other platforms' native fulltext search functions (Windows, linux, android?!, iOS ;-) etc) 
is very appreciated and welcome.

It would be cool to have a similar search interface running on every computer/device in the LAN as some 
type of service, and a client that can search each machine and display results. There has to be a 
discovery mechanism for machines coming on to the LAN too. Pipe dreams...

Dependencies:
  - flask (pip install flask)
  - spotlight (has to be enabled in the Mac)
  - OSX (Obviously; only runs in OS X - needs spotlight)

To run:
  - clone repository
  - cd to the spotlight-web-interface directory
  - python ./spotlight-web-interface.py
  
  OR
  - download spotlight-web-interface.py to any directory 
  - download the jquery.min.js file from js/ to js/ directory

Then:
  - go to http://thiscomputerip:5000/ (where thiscomputerip is the ip address of the computer 
  running the script)
  
A blank search bar will appear. Type the query in and hit enter. Results will appear. Click to 
read or download per borwser and mimetype setting.

  
