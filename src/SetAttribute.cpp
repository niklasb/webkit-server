#include "SetAttribute.h"
#include "WebPage.h"
#include <QWebSettings>

static QMap<QString, QWebSettings::WebAttribute> getAttributesByName()
{
  QMap<QString, QWebSettings::WebAttribute> map;
  map.insert("AutoLoadImages",
             QWebSettings::AutoLoadImages);
  // disable setting JavascriptEnabled to false,
  // as our Javascript helpers won't work then
  //map.insert("JavascriptEnabled",
  //           QWebSettings::JavascriptEnabled);
  map.insert("DnsPrefetchEnabled",
             QWebSettings::DnsPrefetchEnabled);
  map.insert("PluginsEnabled",
             QWebSettings::PluginsEnabled);
  map.insert("PrivateBrowsingEnabled",
             QWebSettings::PrivateBrowsingEnabled);
  map.insert("JavascriptCanOpenWindows",
             QWebSettings::JavascriptCanOpenWindows);
  map.insert("JavascriptCanAccessClipboard",
             QWebSettings::JavascriptCanAccessClipboard);
  map.insert("OfflineStorageDatabaseEnabled",
             QWebSettings::OfflineStorageDatabaseEnabled);
  map.insert("OfflineWebApplicationCacheEnabled",
             QWebSettings::OfflineWebApplicationCacheEnabled);
  map.insert("LocalStorageEnabled",
             QWebSettings::LocalStorageEnabled);
  map.insert("LocalStorageDatabaseEnabled",
             QWebSettings::LocalStorageDatabaseEnabled);
  map.insert("LocalContentCanAccessRemoteUrls",
             QWebSettings::LocalContentCanAccessRemoteUrls);
  map.insert("LocalContentCanAccessFileUrls",
             QWebSettings::LocalContentCanAccessFileUrls);
  map.insert("AcceleratedCompositingEnabled",
             QWebSettings::AcceleratedCompositingEnabled);
  map.insert("SiteSpecificQuirksEnabled",
             QWebSettings::SiteSpecificQuirksEnabled);
  return map;
}

const QMap<QString, QWebSettings::WebAttribute> attributes_by_name =
  getAttributesByName();

SetAttribute::SetAttribute(WebPageManager *manager, QStringList &arguments, QObject *parent) : SocketCommand(manager, arguments, parent) {
}

void SetAttribute::start() {
  if (!attributes_by_name.contains(arguments()[0])) {
    // not found
    finish(false, QString("No such attribute: ") +
                  arguments()[0]);
    return;
  }

  if (!page()->isLoading()) {
    disconnect(page(), SIGNAL(pageFinished(bool)), this, SLOT(loadFinished(bool)));
    finish(true);
  }

  QWebSettings::WebAttribute attr =
    attributes_by_name[arguments()[0]];

  if (arguments()[1] != "reset")
    page()->settings()->setAttribute(attr, arguments()[1] != "false");
  else
    page()->settings()->resetAttribute(attr);

  finish(true);
}
