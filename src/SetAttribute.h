#include "SocketCommand.h"

class SetAttribute : public SocketCommand {
  Q_OBJECT;

  public:
    SetAttribute(WebPageManager*, QStringList&, QObject* parent = 0);
    virtual void start();
};
