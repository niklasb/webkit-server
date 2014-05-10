#include "SocketCommand.h"

class SetHtml : public SocketCommand {
  Q_OBJECT;

  public:
    SetHtml(WebPageManager*, QStringList&, QObject *parent = 0);
    virtual void start();
};
