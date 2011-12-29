#include "SetViewportSize.h"
#include "WebPage.h"

SetViewportSize::SetViewportSize(WebPage *page, QObject *parent)
  : Command(page, parent)
{ }

void SetViewportSize::start(QStringList &arguments)
{
  int width  = arguments[0].toInt();
  int height = arguments[1].toInt();

  QSize size(width, height);
  page()->setViewportSize(size);

  emit finished(new Response(true));
}
