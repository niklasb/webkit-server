#include "Server.h"
#include "WebPage.h"
#include "Connection.h"

#include <QTcpServer>

Server::Server(QObject *parent, bool ignoreSslErrors) : QObject(parent) {
  m_tcp_server = new QTcpServer(this);
}

bool Server::start() {
  connect(m_tcp_server, SIGNAL(newConnection()), this, SLOT(handleConnection()));
  return m_tcp_server->listen(QHostAddress::Any, 0);
}

quint16 Server::server_port() const {
  return m_tcp_server->serverPort();
}

void Server::handleConnection() {
  QTcpSocket *socket = m_tcp_server->nextPendingConnection();
  WebPage *m_page = new WebPage(this);
  m_page->setIgnoreSslErrors(true);
  new Connection(socket, new WebPage(this), this);
}
