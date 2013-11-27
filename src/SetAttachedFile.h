#include "JavascriptCommand.h"

class SetAttachedFile : public JavascriptCommand {
  Q_OBJECT

  public:
    SetAttachedFile(WebPageManager *, QStringList &arguments, QObject *parent = 0);
    virtual void start();
};
