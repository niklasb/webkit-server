#include <QtWebKitWidgets>

class WebPage : public QWebPage {
  Q_OBJECT

  public:
    WebPage(QObject *parent = 0);
    QVariant invokeCapybaraFunction(const char *name, QStringList &arguments);
    QVariant invokeCapybaraFunction(QString &name, QStringList &arguments);
    QString failureString();
    QString userAgentForUrl(const QUrl &url ) const;
    void setUserAgent(QString userAgent);
    int getLastStatus();
    void resetResponseHeaders();
    void setCustomNetworkAccessManager();
    bool render(const QString &fileName);
    virtual bool extension (Extension extension, const ExtensionOption *option=0, ExtensionReturn *output=0);
    void setIgnoreSslErrors(bool ignore);
    bool ignoreSslErrors();
    QString consoleMessages();
    void resetConsoleMessages();

  public slots:
    bool shouldInterruptJavaScript();
    void injectJavascriptHelpers();
    void loadStarted();
    void loadFinished(bool);
    bool isLoading() const;
    QString pageHeaders();
    void frameCreated(QWebFrame *);
    void replyFinished(QNetworkReply *reply);
    void ignoreSslErrors(QNetworkReply *reply, const QList<QSslError> &);
    void handleUnsupportedContent(QNetworkReply *reply);
    void resetSettings();
    void setErrorTolerant(bool errorTolerant);

  signals:
    void pageFinished(bool);

  protected:
    virtual void javaScriptConsoleMessage(const QString &message, int lineNumber, const QString &sourceID);
    virtual void javaScriptAlert(QWebFrame *frame, const QString &message);
    virtual bool javaScriptConfirm(QWebFrame *frame, const QString &message);
    virtual bool javaScriptPrompt(QWebFrame *frame, const QString &message, const QString &defaultValue, QString *result);
    virtual QString chooseFile(QWebFrame * parentFrame, const QString &suggestedFile);

  private:
    bool m_errorTolerant;
    QString m_error;
    QString m_capybaraJavascript;
    QString m_userAgent;
    bool m_loading;
    QString getLastAttachedFileName();
    void loadJavascript();
    void setUserStylesheet();
    int m_lastStatus;
    QString m_pageHeaders;
    bool m_ignoreSslErrors;
    QStringList m_consoleMessages;
};

