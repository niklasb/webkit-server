#include "Source.h"
#include "NetworkAccessManager.h"
#include "WebPageManager.h"
#include "WebPage.h"

Source::Source(WebPageManager *manager, QStringList &arguments,
               QObject *parent)
  : SocketCommand(manager, arguments, parent) {
}

void Source::start() {
  NetworkAccessManager* accessManager = manager()->networkAccessManager();
  QNetworkRequest request(page()->currentFrame()->url());
  reply = accessManager->get(request);

  connect(reply, SIGNAL(finished()), this, SLOT(sourceLoaded()));
}

void Source::sourceLoaded() {
  finish(true, reply->readAll());
}
