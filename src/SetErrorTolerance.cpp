#include "SetErrorTolerance.h"
#include "WebPage.h"

SetErrorTolerance::SetErrorTolerance(WebPage *page, QObject *parent)
  : Command(page, parent)
{ }

void SetErrorTolerance::start(QStringList &arguments)
{
  int tolerance = arguments.takeFirst().toInt();
  if (tolerance < 0)
    emit finished(new Response(false, "Expected integer argument >= 0"));
  page()->setErrorTolerance(tolerance);
  emit finished(new Response(true));
}
