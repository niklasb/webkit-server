#include "SocketCommand.h"
#include <QMap>
#include <QString>
#include <QWebSettings>

extern const QMap<QString, QWebSettings::WebAttribute> attributes_by_name;

class WebPage;

class SetAttribute : public SocketCommand {
  Q_OBJECT

  public:
    SetAttribute(WebPageManager *manager, QStringList &arguments, QObject *parent = 0);
    virtual void start();
};
