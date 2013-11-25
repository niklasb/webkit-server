#include "SocketCommand.h"

class SetHtml : public SocketCommand {
  Q_OBJECT

  public:
    SetHtml(WebPageManager *manager, QStringList &arguments, QObject *parent = 0);
    virtual void start();
};
