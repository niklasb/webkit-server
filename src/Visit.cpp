#include "Visit.h"
#include "Command.h"
#include "WebPage.h"
#include <iostream>

Visit::Visit(WebPage *page, QObject *parent) : Command(page, parent) {
  connect(page, SIGNAL(pageFinished(bool)), this, SLOT(loadFinished(bool)));
}

void Visit::start(QStringList &arguments) {
  QUrl requestedUrl = QUrl(arguments[0]);
  std::cerr << "VISIT requesting load" << std::endl;
  page()->currentFrame()->load(QUrl(requestedUrl));
}

void Visit::loadFinished(bool success) {
  std::cerr << "VISIT load finished" << std::endl;
  QString message;
  if (!success)
    message = page()->failureString();

  disconnect(page(), SIGNAL(pageFinished(bool)), this, SLOT(loadFinished(bool)));
  emit finished(new Response(success, message));
}
