#include "Command.h"

class WebPage;

class Wait : public Command {
  Q_OBJECT

  public:
    Wait(WebPage *page, QObject *parent = 0);
    virtual void start(QStringList &arguments);

  private slots:
    void loadFinished(bool success);
};

