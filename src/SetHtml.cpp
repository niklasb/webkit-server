#include "SetHtml.h"
#include "WebPage.h"
#include <QUrl>

SetHtml::SetHtml(WebPageManager *manager, QStringList &arguments, QObject *parent)
  : SocketCommand(manager, arguments, parent)
{ }

void SetHtml::start() {
  if (arguments().size() > 1)
    page()->currentFrame()->setHtml(arguments()[0], QUrl(arguments()[1]));
  else
    page()->currentFrame()->setHtml(arguments()[0]);
  finish(true);
}
