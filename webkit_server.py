"""
Python bindings for the `webkit-server <https://github.com/niklasb/webkit-server/>`_
"""

import sys, os
import subprocess
import re
import socket
import atexit
import json

# path to the `webkit_server` executable
SERVER_EXEC = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                           'webkit_server'))


class SelectionMixin(object):
  """ Implements a generic XPath selection for a class providing
  ``_get_xpath_ids``, ``_get_css_ids`` and ``get_node_factory`` methods. """

  def xpath(self, xpath):
    """ Finds another node by XPath originating at the current node. """
    return [self.get_node_factory().create(node_id)
            for node_id in self._get_xpath_ids(xpath).split(",")
            if node_id]

  def css(self, css):
    """ Finds another node by a CSS selector relative to the current node. """
    return [self.get_node_factory().create(node_id)
            for node_id in self._get_css_ids(css).split(",")
            if node_id]


class NodeFactory(object):
  """ Implements the default node factory.

  `client` is the associated client instance. """

  def __init__(self, client):
    self.client = client

  def create(self, node_id):
    return Node(self.client, node_id)


class NodeError(Exception):
  """ A problem occured within a ``Node`` instance method. """
  pass

class Node(SelectionMixin):
  """ Represents a DOM node in our Webkit session.

  `client` is the associated client instance.

  `node_id` is the internal ID that is used to identify the node when communicating
  with the server. """

  def __init__(self, client, node_id):
    super(Node, self).__init__()
    self.client = client
    self.node_id = node_id

  def text(self):
    """ Returns the inner text (*not* HTML). """
    return self._invoke("text")

  def get_bool_attr(self, name):
    """ Returns the value of a boolean HTML attribute like `checked` or `disabled`
    """
    val = self.get_attr(name)
    return val is not None and val.lower() in ("true", name)

  def get_attr(self, name):
    """ Returns the value of an attribute. """
    return self._invoke("attribute", name)

  def set_attr(self, name, value):
    """ Sets the value of an attribute. """
    self.exec_script("node.setAttribute(%s, %s)" % (repr(name), repr(value)))

  def value(self):
    """ Returns the node's value. """
    if self.is_multi_select():
      return [opt.value()
              for opt in self.xpath(".//option")
              if opt["selected"]]
    else:
      return self._invoke("value")

  def set(self, value):
    """ Sets the node content to the given value (e.g. for input fields). """
    self._invoke("set", value)

  def path(self):
    """ Returns an XPath expression that uniquely identifies the current node. """
    return self._invoke("path")

  def submit(self):
    """ Submits a form node, then waits for the page to completely load. """
    self.eval_script("node.submit()")

  def eval_script(self, js):
    """ Evaluate arbitrary Javascript with the ``node`` variable bound to the
    current node. """
    return self.client.eval_script(self._build_script(js))

  def exec_script(self, js):
    """ Execute arbitrary Javascript with the ``node`` variable bound to
    the current node. """
    self.client.exec_script(self._build_script(js))

  def _build_script(self, js):
    return "var node = Capybara.nodes[%s]; %s;" % (self.node_id, js)

  def select_option(self):
    """ Selects an option node. """
    self._invoke("selectOption")

  def unselect_options(self):
    """ Unselects an option node (only possible within a multi-select). """
    if self.xpath("ancestor::select")[0].is_multi_select():
      self._invoke("unselectOption")
    else:
      raise NodeError, "Unselect not allowed."

  def click(self):
    """ Alias for ``left_click``. """
    self.left_click()

  def left_click(self):
    """ Left clicks the current node, then waits for the page
    to fully load. """
    self._invoke("leftClick")

  def right_click(self):
    """ Right clicks the current node, then waits for the page
    to fully load. """
    self._invoke("rightClick")

  def double_click(self):
    """ Double clicks the current node, then waits for the page
    to fully load. """
    self._invoke("doubleClick")

  def hover(self):
    """ Hovers over the current node, then waits for the page
    to fully load. """
    self._invoke("hover")

  def focus(self):
    """ Puts the focus onto the current node, then waits for the page
    to fully load. """
    self._invoke("focus")

  def drag_to(self, element):
    """ Drag the node to another one. """
    self._invoke("dragTo", element.node_id)

  def tag_name(self):
    """ Returns the tag name of the current node. """
    return self._invoke("tagName")

  def is_visible(self):
    """ Checks whether the current node is visible. """
    return self._invoke("visible") == "true"

  def is_attached(self):
    """ Checks whether the current node is actually existing on the currently
    active web page. """
    return self._invoke("isAttached") == "true"

  def is_selected(self):
    """ is the ``selected`` attribute set for this node? """
    return self.get_bool_attr("selected")

  def is_checked(self):
    """ is the ``checked`` attribute set for this node? """
    return self.get_bool_attr("checked")

  def is_disabled(self):
    """ is the ``disabled`` attribute set for this node? """
    return self.get_bool_attr("disabled")

  def is_multi_select(self):
    """ is this node a multi-select? """
    return self.tag_name() == "select" and self.get_bool_attr("multiple")

  def _get_xpath_ids(self, xpath):
    """ Implements a mechanism to get a list of node IDs for an relative XPath
    query. """
    return self._invoke("findXpathWithin", xpath)

  def _get_css_ids(self, css):
    """ Implements a mechanism to get a list of node IDs for an relative CSS
    query. """
    return self._invoke("findCssWithin", css)

  def get_node_factory(self):
    """ Returns the associated node factory. """
    return self.client.get_node_factory()

  def __repr__(self):
    return "<Node #%s>" % self.path()

  def _invoke(self, cmd, *args):
    return self.client.issue_node_cmd(cmd, "false", self.node_id, *args)


class Client(SelectionMixin):
  """ Wrappers for the webkit_server commands.

  If `connection` is not specified, a new instance of ``ServerConnection`` is
  created.

  `node_factory_class` can be set to a value different from the default, in which
  case a new instance of the given class will be used to create nodes. The given
  class must accept a client instance through its constructor and support a
  ``create`` method that takes a node ID as an argument and returns a node object.
  """

  def __init__(self,
               connection = None,
               node_factory_class = NodeFactory):
    super(Client, self).__init__()
    self.conn = connection or ServerConnection()
    self._node_factory = node_factory_class(self)

  def visit(self, url):
    """ Goes to a given URL. """
    self.conn.issue_command("Visit", url)

  def body(self):
    """ Returns the current DOM as HTML. """
    return self.conn.issue_command("Body")

  def source(self):
    """ Returns the source of the page as it was originally
    served by the web server. """
    return self.conn.issue_command("Source")

  def url(self):
    """ Returns the current location. """
    return self.conn.issue_command("CurrentUrl")

  def set_header(self, key, value):
    """ Sets a HTTP header for future requests. """
    self.conn.issue_command("Header", key, value)

  def reset(self):
    """ Resets the current web session. """
    self.conn.issue_command("Reset")

  def status_code(self):
    """ Returns the numeric HTTP status of the last response. """
    return int(self.conn.issue_command("Status"))

  def headers(self):
    """ Returns a list of the last HTTP response headers. """
    headers = self.conn.issue_command("Headers")
    res = []
    for header in headers.split("\r"):
      key, value = header.split(": ", 1)
      for line in value.split("\n"):
        res.append((key, line))
    return res

  def eval_script(self, expr):
    """ Evaluates a piece of Javascript in the context of the current page and
    returns its value. """
    ret = self.conn.issue_command("Evaluate", expr)
    return json.loads("[%s]" % ret)[0]

  def exec_script(self, script):
    """ Executes a piece of Javascript in the context of the current page. """
    self.conn.issue_command("Execute", script)

  def render(self, path, width = 1024, height = 1024):
    """ Renders the current page to a PNG file (viewport size in pixels). """
    self.conn.issue_command("Render", path, width, height)

  def set_viewport_size(self, width, height):
    """ Sets the viewport size. """
    self.conn.issue_command("ResizeWindow", width, height)

  def set_cookie(self, cookie):
    """ Sets a cookie for future requests (must be in correct cookie string
    format). """
    self.conn.issue_command("SetCookie", cookie)

  def clear_cookies(self):
    """ Deletes all cookies. """
    self.conn.issue_command("ClearCookies")

  def cookies(self):
    """ Returns a list of all cookies in cookie string format. """
    return [line.strip()
            for line in self.conn.issue_command("GetCookies").split("\n")
            if line.strip()]

  def set_error_tolerant(self, tolerant=True):
    """ DEPRECATED! This function is a no-op now.

    Used to set or unset the error tolerance flag in the server. If this flag
    as set, dropped requests or erroneous responses would not lead to an error. """
    return

  def set_attribute(self, attr, value = True):
    """ Sets a custom attribute for our Webkit instance. Possible attributes are:

      * ``auto_load_images``
      * ``dns_prefetch_enabled``
      * ``plugins_enabled``
      * ``private_browsing_enabled``
      * ``javascript_can_open_windows``
      * ``javascript_can_access_clipboard``
      * ``offline_storage_database_enabled``
      * ``offline_web_application_cache_enabled``
      * ``local_storage_enabled``
      * ``local_storage_database_enabled``
      * ``local_content_can_access_remote_urls``
      * ``local_content_can_access_file_urls``
      * ``accelerated_compositing_enabled``
      * ``site_specific_quirks_enabled``

    For all those options, ``value`` must be a boolean. You can find more
    information about these options `in the QT docs
    <http://developer.qt.nokia.com/doc/qt-4.8/qwebsettings.html#WebAttribute-enum>`_.
    """
    value = "true" if value else "false"
    self.conn.issue_command("SetAttribute",
                            self._normalize_attr(attr),
                            value)

  def reset_attribute(self, attr):
    """ Resets a custom attribute. """
    self.conn.issue_command("SetAttribute",
                            self._normalize_attr(attr),
                            "reset")

  def set_html(self, html, url = None):
    """ Sets custom HTML in our Webkit session and allows to specify a fake URL.
    Scripts and CSS is dynamically fetched as if the HTML had been loaded from
    the given URL. """
    if url:
      self.conn.issue_command('SetHtml', html, url)
    else:
      self.conn.issue_command('SetHtml', html)

  def set_proxy(self, host     = "localhost",
                      port     = 0,
                      user     = "",
                      password = ""):
    """ Sets a custom HTTP proxy to use for future requests. """
    self.conn.issue_command("SetProxy", host, port, user, password)

  def clear_proxy(self):
    """ Resets custom HTTP proxy (use none in future requests). """
    self.conn.issue_command("ClearProxy")

  def issue_node_cmd(self, *args):
    """ Issues a node-specific command. """
    return self.conn.issue_command("Node", *args)

  def get_node_factory(self):
    """ Returns the associated node factory. """
    return self._node_factory

  def _get_xpath_ids(self, xpath):
    """ Implements a mechanism to get a list of node IDs for an absolute XPath
    query. """
    return self.conn.issue_command("FindXpath", xpath)

  def _get_css_ids(self, css):
    """ Implements a mechanism to get a list of node IDs for an absolute CSS query
    query. """
    return self.conn.issue_command("FindCss", css)

  def _normalize_attr(self, attr):
    """ Transforms a name like ``auto_load_images`` into ``AutoLoadImages``
    (allows Webkit option names to blend in with Python naming). """
    return ''.join(x.capitalize() for x in attr.split("_"))


class NoX11Error(Exception):
  """ Raised when the Webkit server cannot connect to X. """

class Server(object):
  """ Manages a Webkit server process. If `binary` is given, the specified
  ``webkit_server`` binary is used instead of the included one. """

  def __init__(self, binary = None):
    binary = binary or SERVER_EXEC
    self._server = subprocess.Popen([binary],
                                    stdin  = subprocess.PIPE,
                                    stdout = subprocess.PIPE,
                                    stderr = subprocess.PIPE)
    output = self._server.stdout.readline()
    try:
      self._port = int(re.search("port: (\d+)", output).group(1))
    except AttributeError:
      raise NoX11Error, "Cannot connect to X. You can try running with xvfb-run."

    # on program termination, kill the server instance
    atexit.register(self.kill)

  def kill(self):
    """ Kill the process. """
    self._server.kill()
    self._server.wait()

  def connect(self):
    """ Returns a new socket connection to this server. """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", self._port))
    return sock

default_server = None
def get_default_server():
  """ Returns a singleton Server instance (possibly after creating it, if it
  doesn't exist yet). """
  global default_server
  if not default_server:
    default_server = Server()
  return default_server


class NoResponseError(Exception):
  """ Raised when the Webkit server does not respond. """

class InvalidResponseError(Exception):
  """ Raised when the Webkit server signaled an error. """

class EndOfStreamError(Exception):
  """ Raised when the Webkit server closed the connection unexpectedly. """

class ServerConnection(object):
  """ A connection to a Webkit server.

  `server` is a server instance or `None` if a singleton server should be connected
  to (will be started if necessary). """

  def __init__(self, server = None):
    super(ServerConnection, self).__init__()
    self._sock = (server or get_default_server()).connect()
    self.issue_command("IgnoreSslErrors");

  def issue_command(self, cmd, *args):
    """ Sends and receives a message to/from the server """
    self._writeline(cmd)
    self._writeline(str(len(args)))
    for arg in args:
      arg = str(arg)
      self._writeline(str(len(arg)))
      self._sock.send(arg)

    return self._read_response()

  def _read_response(self):
    """ Reads a complete response packet from the server """
    result = self._readline()
    if not result:
      raise NoResponseError, "No response received from server."

    if result != "ok":
      raise InvalidResponseError, self._read_message()

    return self._read_message()

  def _read_message(self):
    """ Reads a single size-annotated message from the server """
    size = int(self._readline())
    if size == 0:
      return ""
    else:
      return self._recvall(size)

  def _recvall(self, size):
    """ Receive until the given number of bytes is fetched or until EOF (in which
    case ``EndOfStreamError`` is raised). """
    result = []
    while size > 0:
      data = self._sock.recv(min(8192, size))
      if not data:
        raise EndOfStreamError, "Unexpected end of stream."
      result.append(data)
      size -= len(data)
    return ''.join(result)

  def _readline(self):
    """ Cheap implementation of a readline function that operates on our underlying
    socket. """
    res = []
    while True:
      c = self._sock.recv(1)
      if c == "\n":
        return "".join(res)
      res.append(c)

  def _writeline(self, line):
    """ Writes a line to the underlying socket. """
    self._sock.send(line + "\n")
