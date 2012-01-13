#include "Command.h"

class WebPage;

class SetErrorTolerance : public Command {
  Q_OBJECT;

 public:
  SetErrorTolerance(WebPage *page, QObject *parent = 0);
  virtual void start(QStringList &arguments);
};
