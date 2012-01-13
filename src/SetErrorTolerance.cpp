#include "SetErrorTolerance.h"
#include "WebPage.h"

SetErrorTolerance::SetErrorTolerance(WebPage *page, QObject *parent)
  : Command(page, parent)
{ }

void SetErrorTolerance::start(QStringList &arguments)
{
  page()->setErrorTolerant(arguments.takeFirst() != "false");
  emit finished(new Response(true));
}
