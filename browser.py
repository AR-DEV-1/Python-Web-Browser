import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QTabWidget, QHBoxLayout, QAction,
    QMenuBar, QToolBar, QFileDialog, QMessageBox, QPushButton, QLabel, QStatusBar, QSplitter
)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QIcon

class BrowserTab(QWidget):
    def __init__(self):
        super().__init__()

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.browser)

        self.setLayout(layout)

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Python Web Browser")
        self.setGeometry(100, 100, 1280, 800)

        self.url_bar = QLineEdit()
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.update_url_bar)
        self.setCentralWidget(self.tabs)

        self.bookmarks = []
        self.history = []
        self.downloads = []

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.create_new_tab(QUrl("https://www.google.com"), "New Tab")

        self.create_toolbar()
        self.create_menu_bar()

    def create_toolbar(self):
        toolbar = QToolBar("Navigation")
        self.addToolBar(toolbar)

        back_button = QAction(QIcon("icons/1.png"), "Back", self)
        back_button.triggered.connect(self.navigate_back)
        toolbar.addAction(back_button)

        forward_button = QAction(QIcon("icons/2.png"), "Forward", self)
        forward_button.triggered.connect(self.navigate_forward)
        toolbar.addAction(forward_button)

        reload_button = QAction(QIcon("icons/3.png"), "Reload", self)
        reload_button.triggered.connect(self.reload_page)
        toolbar.addAction(reload_button)

        new_tab_button = QAction(QIcon("icons/4.png"), "New Tab", self)
        new_tab_button.triggered.connect(self.open_new_tab)
        toolbar.addAction(new_tab_button)

        home_button = QAction(QIcon("icons/5.png"), "Home", self)
        home_button.triggered.connect(self.navigate_home)
        toolbar.addAction(home_button)

        bookmark_button = QAction(QIcon("icons/6.png"), "Bookmark", self)
        bookmark_button.triggered.connect(self.add_bookmark)
        toolbar.addAction(bookmark_button)

        show_history_button = QAction(QIcon("icons/7.png"), "History", self)
        show_history_button.triggered.connect(self.show_history)
        toolbar.addAction(show_history_button)

        downloads_button = QAction(QIcon("icons/8.png"), "Downloads", self)
        downloads_button.triggered.connect(self.show_downloads)
        toolbar.addAction(downloads_button)

        toggle_dark_mode = QAction(QIcon("icons/9.png"), "Toggle Dark Mode", self)
        toggle_dark_mode.triggered.connect(self.toggle_dark_mode)
        toolbar.addAction(toggle_dark_mode)

        split_view_button = QAction(QIcon("icons/10.png"), "Split View", self)
        split_view_button.triggered.connect(self.split_view)
        toolbar.addAction(split_view_button)

        self.url_bar.returnPressed.connect(self.navigate_to_url)
        toolbar.addWidget(self.url_bar)

        toolbar.setStyleSheet("background-color: #f0f0f0; padding: 5px;")

    def create_menu_bar(self):
        menu_bar = QMenuBar(self)

        file_menu = menu_bar.addMenu("File")
        new_tab_action = QAction("New Tab", self)
        new_tab_action.triggered.connect(self.open_new_tab)
        file_menu.addAction(new_tab_action)

        save_page_action = QAction("Save Page As", self)
        save_page_action.triggered.connect(self.save_page)
        file_menu.addAction(save_page_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        bookmarks_menu = menu_bar.addMenu("Bookmarks")
        show_bookmarks_action = QAction("Show Bookmarks", self)
        show_bookmarks_action.triggered.connect(self.show_bookmarks)
        bookmarks_menu.addAction(show_bookmarks_action)

        tools_menu = menu_bar.addMenu("Tools")
        clear_history_action = QAction("Clear History", self)
        clear_history_action.triggered.connect(self.clear_history)
        tools_menu.addAction(clear_history_action)

        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.show_settings)
        tools_menu.addAction(settings_action)

        self.setMenuBar(menu_bar)

    def create_new_tab(self, qurl=QUrl("https://www.google.com"), label="New Tab"):
        browser_tab = BrowserTab()
        browser_tab.browser.setUrl(qurl)
        index = self.tabs.addTab(browser_tab, label)
        self.tabs.setCurrentIndex(index)
        browser_tab.browser.urlChanged.connect(self.update_url_bar_from_browser)

        self.history.append(qurl.toString())

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        self.current_browser().setUrl(QUrl(url))

        self.history.append(url)
        self.status_bar.showMessage(f"Navigating to {url}")

    def update_url_bar_from_browser(self, qurl):
        self.url_bar.setText(qurl.toString())
        self.status_bar.showMessage(f"Current URL: {qurl.toString()}")

    def update_url_bar(self, index):
        current_tab = self.tabs.widget(index)
        if current_tab:
            current_browser = current_tab.browser
            self.url_bar.setText(current_browser.url().toString())

    def navigate_back(self):
        self.current_browser().back()
        self.status_bar.showMessage("Navigating back")

    def navigate_forward(self):
        self.current_browser().forward()
        self.status_bar.showMessage("Navigating forward")

    def reload_page(self):
        self.current_browser().reload()
        self.status_bar.showMessage("Reloading page")

    def open_new_tab(self):
        self.create_new_tab()

    def navigate_home(self):
        self.current_browser().setUrl(QUrl("https://www.google.com"))
        self.status_bar.showMessage("Navigating to home")

    def add_bookmark(self):
        url = self.current_browser().url().toString()
        if url not in self.bookmarks:
            self.bookmarks.append(url)
            QMessageBox.information(self, "Bookmark Added", f"{url} has been added to bookmarks.")
        else:
            QMessageBox.information(self, "Bookmark", f"{url} is already bookmarked.")

    def show_bookmarks(self):
        if not self.bookmarks:
            QMessageBox.information(self, "Bookmarks", "No bookmarks available.")
            return

        bookmarks_str = "\n".join(self.bookmarks)
        QMessageBox.information(self, "Bookmarks", bookmarks_str)

    def show_history(self):
        if not self.history:
            QMessageBox.information(self, "History", "No browsing history available.")
            return

        history_str = "\n".join(self.history)
        QMessageBox.information(self, "History", history_str)

    def clear_history(self):
        self.history.clear()
        QMessageBox.information(self, "History", "Browsing history cleared.")

    def toggle_dark_mode(self):
        if self.styleSheet():
            self.setStyleSheet("")
        else:
            self.setStyleSheet("background-color: #2E2E2E; color: #FFFFFF;")

    def show_downloads(self):
        downloads_str = "\n".join(self.downloads) if self.downloads else "No downloads available."
        QMessageBox.information(self, "Downloads", downloads_str)

    def split_view(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            splitter = QSplitter(Qt.Horizontal)
            left_browser = QWebEngineView()
            right_browser = QWebEngineView()

            left_browser.setUrl(current_tab.browser.url())
            right_browser.setUrl(QUrl("https://www.google.com"))

            splitter.addWidget(left_browser)
            splitter.addWidget(right_browser)

            layout = QVBoxLayout()
            layout.addWidget(splitter)

            new_widget = QWidget()
            new_widget.setLayout(layout)

            self.tabs.addTab(new_widget, "Split View")

    def save_page(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Page As", "", "HTML Files (*.html);;All Files (*)")
            if file_path:
                current_tab.browser.page().toHtml(lambda html: self.write_to_file(file_path, html))

    def write_to_file(self, file_path, content):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        QMessageBox.information(self, "Save Page", f"Page saved to {file_path}.")

    def show_settings(self):
        QMessageBox.information(self, "Settings", "Settings feature under development.")

    def current_browser(self):
        return self.tabs.currentWidget().browser

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())