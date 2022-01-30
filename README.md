# SA:MP Wiki Scraper

### Caution

All the data behind old SA:MP Wiki might be protected work. I'm not a lawyer - use it on your own risk!
This script accesses the page every three seconds to avoid accessing it too often - your access might otherwise be identified as an attack. As already said: use it (and speed it up) on your own risk!
  
Check https://team.sa-mp.com/robots.txt before using the script! You may not have the permission to use the script on some sites.  
Respect others boundaries!

### Installation

The following packages are needed in order to make your own dump:

- bs4 (BeautifulSoup)
- requests
- colorama

I recommend using the newest Python version. Use whatever version you want, as long as it assists all features used in the packages.  
Python versions below 3 won't work.

```
pip install -r requirements.txt
```
  
That's it.

### Usage

This tool was originally designed to collect all possible links from the SA:MP Wiki. There is no need to recollect all the links, you can use my list linked down below.  
In order to collect all links by your own (this may take up to 3-4 hours!), run `python3 samp_wiki_scraper.py` and choose option number 1.
  
In order to skip this process, check out my gist: https://gist.github.com/Andosius/eaca6480be330e9c6432b3ebaf1aa5e9
Put this file into the projects main directory and run `python3 samp_wiki_scraper.py` with option number 2. This should create the whole directory structure for you.
Afterwards you can start downloading the contents by running `python3 samp_wiki_scraper.py` and choosing option number 3.
  
  
All the files will be within the `dump/` directory. Have fun.