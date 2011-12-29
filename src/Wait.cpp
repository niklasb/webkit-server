#include "Wait.h"
#include "Command.h"
#include "WebPage.h"

Wait::Wait(WebPage *page, QObject *parent)
  : Command(page, parent)
{ }

void Wait::start(QStringList &arguments) {
  Q_UNUSED(arguments);
  connect(page(), SIGNAL(pageFinished(bool)), this, SLOT(loadFinished(bool)));

  if (!page()->isLoading()) {
    disconnect(page(), SIGNAL(pageFinished(bool)), this, SLOT(loadFinished(bool)));
    emit finished(new Response(true));
  }
}

void Wait::loadFinished(bool success) {
  QString message;
  if (!success)
    message = page()->failureString();

  disconnect(page(), SIGNAL(pageFinished(bool)), this, SLOT(loadFinished(bool)));
  emit finished(new Response(success, message));
}
