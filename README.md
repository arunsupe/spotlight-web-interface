# spotlight-web-interface
Expose spotlight via a web interface in the LAN

In my home, I have an iMac desktop that acts as the fileserver. I save all my family's digital 
belongings in it. I use OSX's spotlight to index the files for search. As a convenience, I wrote a small 
python script to expose this machine's spotlight to the LAN via a web interface. This way, I can 
search my fileserver using spotlight from anywhere in the LAN using any web browser.

I am an amature at programming and with python. The code does not do any error checking. It 
blocks with each request. I use it purely as a convenience. The entire family can now find  
files named "2015 tax return" or whatever from their laptops. I am putting it out there so that
anyone who finds it useful may use it. Any help improving it, or adding other search options using
the platform's native search functions (Windows 10, linux etc) is very appreciated and welcome.

It would be cool to have a similar search interface running on every computer/device in the LAN as some 
type of service, and a client that can search each machine and display results. There has to be a 
discovery mechanism for machines coming on to the LAN too. Pipe dreams...