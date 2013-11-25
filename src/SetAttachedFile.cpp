#include "SetAttachedFile.h"
#include "WebPage.h"
#include "WebPageManager.h"
#include "InvocationResult.h"

SetAttachedFile::SetAttachedFile(WebPageManager *manager, QStringList &arguments, QObject *parent) : JavascriptCommand(manager, arguments, parent) {
}

void SetAttachedFile::start() {
  InvocationResult result = page()->invokeCapybaraFunction("setAttachedFile", arguments());
  finish(&result);
}
