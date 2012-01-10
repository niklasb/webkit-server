# Overview

A standalone version of the Webkit server included in [capybara-webkit][1].
It includes a slim Python wrapper and the following improvements over the
original version from thoughtbot:

* `Wait` command to wait for the current page to load
* `SetAttribute` command to [configure certain `QWebkit` settings][2]
* `SetHtml` command to [load custom HTML][3] into the browser (e.g. to
  execute scripts on web pages scraped by a static scraper)
* `submit()` and `path()` methods for DOM nodes to [submit forms and get
  an XPath of the node][4], respectively
* `SetViewportSize` command to set the viewport size of the in-memory browser

# Building and Installing

* If you only want to build the server, you can use the provided shell script
  `build.sh`.
* If you want to install the Python binding, you can use `sudo python
  setup.py install` (this also builds the server and places it into Python's
  `site-packages` directory).
* If you want to use the Webkit server for web scraping, please take a look at
  [pyscrape][5].

# License

This software is based on [capybara-webkit][1].
capybara-webkit is Copyright (c) 2011 thoughtbot, inc. It is free software, and
may be redistributed under the terms specified in the LICENSE file.

 [1]: https://github.com/thoughtbot/capybara-webkit
 [2]: https://github.com/thoughtbot/capybara-webkit/pull/171
 [3]: https://github.com/thoughtbot/capybara-webkit/pull/170
 [4]: https://github.com/thoughtbot/capybara-webkit/pull/173
 [5]: https://github.com/niklasb/pyscrape
