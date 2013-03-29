#include "Wait.h"
#include "Command.h"
#include "WebPage.h"
#include <iostream>

Wait::Wait(WebPage *page, QObject *parent)
  : Command(page, parent)
{ }

void Wait::start(QStringList &arguments) {
  Q_UNUSED(arguments);
  connect(page(), SIGNAL(pageFinished(bool)), this, SLOT(loadFinished(bool)));

  std::cerr << "WAIT connected pageFinished slot" << std::endl;
  std::cerr << "WAIT page isLoading: " << page()->isLoading() << std::endl;
  if (!page()->isLoading()) {
    std::cerr << "WAIT disconnecting" << std::endl;
    disconnect(page(), SIGNAL(pageFinished(bool)), this, SLOT(loadFinished(bool)));
    emit finished(new Response(true));
  }
}

void Wait::loadFinished(bool success) {
  std::cerr << "WAIT loadFinished" << std::endl;
  QString message;
  if (!success)
    message = page()->failureString();

  std::cerr << "WAIT loadFinished disconnecting (2)" << std::endl;
  disconnect(page(), SIGNAL(pageFinished(bool)), this, SLOT(loadFinished(bool)));
  emit finished(new Response(success, message));
}
