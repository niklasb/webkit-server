#include "SocketCommand.h"

class Wait : public SocketCommand {
  Q_OBJECT

  public:
    Wait(WebPageManager *manager, QStringList &arguments, QObject *parent = 0);
    virtual void start();

  private slots:
    void loadFinished(bool success);
};
