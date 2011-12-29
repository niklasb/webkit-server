#include "Command.h"

class WebPage;

class SetViewportSize : public Command {
  Q_OBJECT;

 public:
  SetViewportSize(WebPage *page, QObject *parent = 0);
  virtual void start(QStringList &arguments);
};
