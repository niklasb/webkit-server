#include "SetAttribute.h"
#include "WebPage.h"
#include <QWebSettings>

static QMap<QString, QWebSettings::WebAttribute> getAttributesByName()
{
  QMap<QString, QWebSettings::WebAttribute> map;
#define ADD_ATTR(attr) map.insert(#attr, QWebSettings::attr)
  ADD_ATTR(AutoLoadImages);
  ADD_ATTR(DnsPrefetchEnabled);
  ADD_ATTR(PluginsEnabled);
  ADD_ATTR(PrivateBrowsingEnabled);
  ADD_ATTR(JavascriptCanOpenWindows);
  ADD_ATTR(JavascriptCanAccessClipboard);
  ADD_ATTR(OfflineStorageDatabaseEnabled);
  ADD_ATTR(OfflineWebApplicationCacheEnabled);
  ADD_ATTR(LocalStorageEnabled);
  ADD_ATTR(LocalStorageDatabaseEnabled);
  ADD_ATTR(LocalContentCanAccessFileUrls);
  ADD_ATTR(LocalContentCanAccessRemoteUrls);
  ADD_ATTR(AcceleratedCompositingEnabled);
  ADD_ATTR(SiteSpecificQuirksEnabled);
  // disable setting JavascriptEnabled to false,
  // as our Javascript helpers won't work then
  //ADD_ATTR("JavascriptEnabled");
  //map.insert("JavascriptEnabled",
  //           QWebSettings::JavascriptEnabled);
#undef ADD_ATTR
  return map;
}

const QMap<QString, QWebSettings::WebAttribute> attributes_by_name =
  getAttributesByName();

SetAttribute::SetAttribute(WebPageManager* manager, QStringList& args, QObject* parent)
  : SocketCommand(manager, args, parent)
{ }

void SetAttribute::start()
{
  QString name = arguments()[0], val = arguments()[1];
  if (!attributes_by_name.contains(name)) {
    // not found
    finish(false, QString("No such attribute: ") + name);
    return;
  }

  QWebSettings::WebAttribute attr = attributes_by_name[name];
  if (val != "reset")
    page()->settings()->setAttribute(attr, val != "false");
  else
    page()->settings()->resetAttribute(attr);

  finish(true);
}
