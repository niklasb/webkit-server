# Overview

**Author:** Niklas Baumstark

A standalone version of the Webkit server included in [capybara-webkit][1].
It includes a slim Python wrapper and the following improvements over the
original version from thoughtbot:

* `Wait` command to wait for the current page to load
* `SetAttribute` command to [configure certain `QWebkit` settings][2]
* `SetHtml` command to [load custom HTML][3] into the browser (e.g. to
  execute scripts on web pages scraped by a static scraper)
* `SetViewportSize` command to set the viewport size of the in-memory browser

If you are interested in web scraping using this server, have a look at [dryscrape][4].

# Building and Installing

To install the Python binding (this also builds the server and places it into
Python's `site-package` directory):

    sudo python setup.py install

If you don't need the Python bindings, you can also use the supplied `build.sh`
shellscript to build the server only.

### A word about Qt 5.6

The 5.6 version of Qt removes the Qt WebKit module in favor of the new module Qt WebEngine. So far webkit-server has not been ported to WebEngine (and likely won't be in the near future), so Qt <= 5.5 is a requirement.

# Contact, Bugs, Contributions

If you have any problems with this software, don't hesitate to open an 
issue on [Github](https://github.com/niklasb/webkit-server) or open a pull 
request or write a mail to **niklas 
baumstark at Gmail**.

# License

This software is based on [capybara-webkit][1].
capybara-webkit is Copyright (c) 2011 thoughtbot, inc. It is free software, and
may be redistributed under the terms specified in the LICENSE file.

 [1]: https://github.com/thoughtbot/capybara-webkit
 [2]: https://github.com/thoughtbot/capybara-webkit/pull/171
 [3]: https://github.com/thoughtbot/capybara-webkit/pull/170
 [4]: https://github.com/niklasb/dryscrape
