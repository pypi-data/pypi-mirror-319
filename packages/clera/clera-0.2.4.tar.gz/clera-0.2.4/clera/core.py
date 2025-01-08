from PySide6.QtCore import QSize, QPoint, QEvent
from PySide6.QtGui import QIcon, QMouseEvent, QScreen, QSyntaxHighlighter, QShortcut
from PySide6.QtWidgets import QMainWindow, QToolBar, QStatusBar, QGroupBox, QButtonGroup
from PySide6.QtWidgets import QWidget,  QHBoxLayout, QVBoxLayout,  QGridLayout, QTabWidget, QMenu
from PySide6.QtWidgets import QDialog, QFileDialog, QStyleFactory, QStackedWidget
################################
################################
from .utils import *
from .widgets import *
from .database import *
# from .scripts import *


__all__ = [
    'Window', 'Box', 'Grid', 'fieldset', 'Column', 'column', 'Group', 'group', 'Toolbar', 'toolbar',
    'Menubar', 'menubar', 'Statusbar', 'statusbar', 'GET', 'get', 'Button', 'button', 'Input',
    'input', 'Text', 'text', 'Image', 'image', 'CheckBox', 'checkbox', 'RadioButton', 'radiobutton',
    'Textarea', 'textarea', 'item', 'empty', 'separator', 'Exit', 'exit', 'Copy', 'copy', 'Cut', 'cut',
    'Paste', 'paste', 'Undo', 'undo', 'Redo', 'redo', 'link', 'ListWidget', 'listwidget', 'ListItem',
    'tab', 'TabWidget', 'tabwidget', 'Select', 'select', 'option', 'ProgressBar', 'progressbar',
    'Slider', 'slider', 'Dial', 'dial', 'Popup', 'popup', 'call', 'Titlebar', 'titlebar', 'File', 'file',
    'Folder', 'folder', 'ScrollArea', 'scrollarea', 'minimize', 'maximize', 'close', 'title', 'Highlight',
    'r', 'Stack', 'stack', 'expand', 'fixed', 'vertical', 'horizontal', 'top', 'bottom', 'left', 'right', 'center',
    'vcenter', 'hcenter', 'justify', 'static', 'normal', 'standard', 'password', 'noecho', 'extended',
    'noselection', 'multi', 'single', 'windows', 'windows11', 'fusion', 'curve', 'breeze', 'oxygen','circle', 'square',
    'encode', 'decode', 'colorpicker', 'ColorPicker', 'Database', 'database', 'null', 'blob',
    'thread', 'screen', 'screenshot', 'shortcut', 'Table', 'td'
]


app = start()

DEFAULT_WINDOW_LAYOUT = QWidget()


def init_window_css(css_string):
    custom, builtins = console_css(css_string)
    for items in custom:
        name, property = items
        widget = WIDGET_ID_SAFE[name]

        if name in WIDGET_ID_SAFE:
            for value in compr:
                value = value.split('::')
                _type = value[1]

                if _type in str(type(widget)):
                    break
                else:
                    remaining_type = value[0]
                    if remaining_type in str(type(widget)).lower():
                        break

            property = property.replace(TYPE_MARKER, _type)
            widget.setStyleSheet(property)
                    

            

    app.setStyleSheet(builtins)


def link(href: None = None):
    if href != None and href.strip().endswith('.cx'):
        LINK_ITEMS_INCLUDED.append(href)


def init_linked_files():
    for LINK_ITEM in LINK_ITEMS_INCLUDED:
        file_path = path.abspath(LINK_ITEM)

        is_file = path.isfile(file_path)
        is_valid_path = path.exists(file_path)

        if is_file != False and is_valid_path != False:
            with open(file_path, 'r') as file:
                file_content = file.read()

            init_window_css(file_content)




class MainWindow(QMainWindow):
    def __init__(self, title, icon, size, fixed_size, geometry, style, frame, movable, win_top, spacing, content_margin, move, tool, cursor):
        super().__init__()

        self._qwidget = DEFAULT_WINDOW_LAYOUT
        self._title = title
        self._size = size
        self._fixed_size = fixed_size
        self._icon = icon
        self._geometry = geometry
        self._movable = movable
        self._frame = frame
        self._top = win_top
        self._spacing = spacing
        self._content_margin = content_margin
        self._move = move
        self._tool = tool
        self._cursor = cursor

        if self._cursor == False:
            self.setCursor(Qt.BlankCursor)
        
        if self._tool == True:
            self.setWindowFlag(Qt.Tool)
    
        self._query_fixed_size = False
        self._custom_title_bar = False

        width, height = self._size
        if width != None and height != None:
            self.resize(int(width), int(height))

        positionx, positiony = self._move
        if positionx != None and positiony != None:
            self.move(positionx, positiony)

        if self._geometry != None:
            if len(self._geometry) == 4:
                x, y, w, h = self._geometry
                self.setGeometry(x, y, w, h)

        self.setWindowTitle(self._title)

        if self._top == True:
            self.setWindowFlag(Qt.WindowStaysOnTopHint)

        app.setStyle(style)
    
        fixed_width, fixed_height = self._fixed_size
        if fixed_width != None and fixed_height != None:
            self._query_fixed_size = True
            self.setFixedSize(QSize(int(fixed_width), int(fixed_height)))

        global layout
        layout = QVBoxLayout()

        layout.setSpacing(self._spacing)

        if type(self._content_margin) != int:
            if len(self._content_margin) == 4:
                left, top, right, bottom = self._content_margin
                layout.setContentsMargins(left, top, right, bottom)
            elif len(self._content_margin) == 2:
                top_bottom, left_right = self._content_margin
                layout.setContentsMargins(
                    left_right, top_bottom, left_right, top_bottom)
            else:
                ...
        else:
            layout.setContentsMargins(
                self._content_margin, self._content_margin, self._content_margin, self._content_margin)

        self._qwidget.setLayout(layout)

        if self._frame == False:
            self.setWindowFlag(Qt.FramelessWindowHint)

            # make window transparent and border cornered

            # self.setAttribute(Qt.WA_TranslucentBackground)
            # DEFAULT_WINDOW_LAYOUT.setWindowOpacity(1)
            # DEFAULT_WINDOW_LAYOUT.setStyleSheet('''
            #     border-bottom-left-radius: 10px; 
            #     border-bottom-right-radius: 10px; 
            #     border-top-left-radius: 0px;
            #     border-top-right-radius: 0px;
            #     ''')
            # self.setStyleSheet('border-top-left-radius: 10px; border-top-right-radius: 10px;')


        self.setWindowIcon(QIcon(init_image(self._icon)))

    def WindowMenubar(self, menu_item, actions: list | None = None):
        if menu_item != None:
            menu_bar = self.menuBar()
            Parent = menu_bar.addMenu(menu_item)

            if actions != None:
                for item in actions:

                    item_type = item[0]

                    if item_type == ELEM_TYPE_ITEM:

                        item_label = item[1]

                        if item_label != DEFAULT_SEPARATOR_MARKER:
                            Child = Parent.addAction(INIT_ITEM(self, item))
                        else:
                            Parent.addSeparator()
                    elif item_type == ELEM_TYPE_SEPARATOR:
                        Parent.addSeparator()

                    else:
                        pass
                        # DO NOTHING FOR NOW. SETUP LATER

    def WindowToolbar(self, name, tool_items, movable, position, ID, size, border, orientation, newline, toggle_view):
        
        toolbar = INIT_WIDGET(ID, QToolBar(name))
        
        if newline == True:
            self.addToolBarBreak()

        width, height = size
        if width != None or height != None:
            toolbar.setIconSize(QSize(width, height))

        toolbar_position = position.lower()

        positions = {
            top     : Qt.TopToolBarArea,
            bottom  : Qt.BottomToolBarArea,
            left    : Qt.LeftToolBarArea,
            right   : Qt.RightToolBarArea
        }

        try:
            self.addToolBar(positions[toolbar_position], toolbar)
        except:
            raise ValueError(position)

        if tool_items != None:
            for item in tool_items:
                if type(item) != type(list()):
                    widget_type, widget_items = check_func(item)
                    LayItOut(toolbar, widget_type, widget_items)
                    # toolbar.addWidget(widget)
                else:

                    item_type = item[0]

                    if item_type == ELEM_TYPE_ITEM:

                        item_label = item[1]

                        if item_label != DEFAULT_SEPARATOR_MARKER:
                            toolbar.addAction(INIT_ITEM(self, item))
                        else:
                            toolbar.addSeparator()
                    elif item_type == ELEM_TYPE_SEPARATOR:
                        toolbar.addSeparator()

                    else:
                        pass
                        # DO NOTHING FOR NOW. SETUP LATER

        toolbar.setMovable(movable)
        toolbar.toggleViewAction().setVisible(toggle_view)
        
        orientations = {
            vertical: Qt.Vertical,
            horizontal: Qt.Horizontal
        }

        try:
            if orientation.lower() in ['v', 'h']:
                change = {
                    'v': vertical,
                    'h': horizontal
                }

                orientation = change[orientation.lower()]

            toolbar.setOrientation(orientations[orientation.lower()])
        except:
            raise ValueError(orientation)

        if border == False:
            toolbar.setStyleSheet('border-bottom: 0px')

    # Status bar functions

    def init_status(self):
        self.setStatusBar(QStatusBar(self))

    def ADD_PERMANENT_WIDGET(self, widget_type, widget_items):
        lyt = self.statusBar()
        LayItOut([lyt, 'addPermanentWidget'], widget_type, widget_items)

    def ADD_NORMAL_WIDGET(self, widget_type, widget_items):
        lyt = self.statusBar()
        LayItOut([lyt, 'addWidget'], widget_type, widget_items)

    def SHOW_STATUSBAR_MESSAGE(self, text, time):
        if time != None:
            time = time * 1000
            self.statusBar().showMessage(text, time)
        else:
            self.statusBar().showMessage(text)

    def CLEAR_STATUSBAR_MESSAGE(self):
        self.statusBar().clearMessage()

    def REMOVE_STATUSBAR_WIDGET(self, ID):
        if ID in WIDGET_ID_SAFE:
            self.statusBar().removeWidget(WIDGET_ID_SAFE[ID])
        else:
            raise IdError(f'id "{ID}" does not exist')

    def mousePressEvent(self, event):
        if self._movable == True:
            window.setCursor(Qt.SizeAllCursor)

        self.old_position = event.globalPos()
        return self.old_position

    def mouseMoveEvent(self, event):
        try:
            omega = QPoint(event.globalPos() - self.old_position)

            if self._custom_title_bar == False and self._movable == True and self._frame == False:
                self.move(self.x() + omega.x(), self.y() + omega.y())
                self.old_position = event.globalPos()
            else:
                return omega
        except:
            ...
        
    def mouseReleaseEvent(self, event: QMouseEvent):
        window.setCursor(Qt.ArrowCursor)

    def WindowTitlebar(self, title, icon, widgets, alignment, backgound_color,  text_color, default):
        current_window_style = window.style().name().lower()

        if default == False:
            if current_window_style == SYSTEM_PLATFORM_FUSION:
                [
                    CONTROL_MINIMIZED, 
                    CONTROL_RESTORE, 
                    CONTROL_MAXIMIZED, 
                    CONTROL_CLOSE,
                    CLOSE_EMPTY,
                    MAXIMIZE_EMPTY,
                    MINIMIZE_EMPTY,
                    RESTORE_EMPTY
                ] = FUSION_CONTROLS()
            
            elif current_window_style == windows or windows in current_window_style:
                # title_padding = 6
                
                [
                    CONTROL_MINIMIZED, 
                    CONTROL_RESTORE, 
                    CONTROL_MAXIMIZED, 
                    CONTROL_CLOSE,
                    CLOSE_EMPTY,
                    MAXIMIZE_EMPTY,
                    MINIMIZE_EMPTY,
                    RESTORE_EMPTY
                ] = WINDOWS_CONTROLS()

        else:
            [
                CONTROL_MINIMIZED, 
                CONTROL_RESTORE, 
                CONTROL_MAXIMIZED, 
                CONTROL_CLOSE,
                CLOSE_EMPTY,
                MAXIMIZE_EMPTY,
                MINIMIZE_EMPTY,
                RESTORE_EMPTY
            ] = CLERA_CONTROLS()

        if self._custom_title_bar == False and self._frame == False:
            if alignment != None:
                if alignment.lower() == 'center':
                    align = 'center'
                else:
                    align = None
            else:
                align = None

            def window_state():
                state = str(self.windowState())
                state = state.split('.')
                state = state[1].lower()
                return state

            def control_action(key: str = ''):
                state = window_state()
                max = GET(MAXIMIZE_BUTTON_ID)

                if key == 'max':
                    if state == 'windowmaximized':
                        self.setWindowState(Qt.WindowNoState)
                    elif state == 'windownostate':
                        max.icon(RESTORE_EMPTY)
                        self.setWindowState(Qt.WindowMaximized)
                elif key == 'min':
                    # Change Minimize Icon To Empty... [BUG]
                    self.setWindowState(Qt.WindowMinimized)
                

            if icon != None:
                titlebar_icon = Image(icon, id=ICON_IMAGE_ID, size=20)
            else:
                titlebar_icon = empty()

            # valid_styles = [SYSTEM_PLATFORM_FUSION, SYSTEM_PLATFORM_WINDOWS, 'windowsvista']
            def icon_controls(slot_one, slot_two, slot_three, size):
                def change_appearance(id, icon):
                    GET(id).icon(icon)   
                
                def change_appearance_maximize(status: str):
                    state = window_state()
                    max = GET(MAXIMIZE_BUTTON_ID)

                    if status == 'leave':
                        if state == 'windowmaximized':
                            max.icon(RESTORE_EMPTY)
                        elif state == 'windownostate':
                            max.icon(MAXIMIZE_EMPTY)
                    elif status == 'enter':
                        if state == 'windowmaximized':
                            max.icon(CONTROL_RESTORE)
                        elif state == 'windownostate':
                            max.icon(CONTROL_MAXIMIZED)
                        
                close_switch = (
                    call(change_appearance, CLOSE_BUTTON_ID, CONTROL_CLOSE),
                    call(change_appearance, CLOSE_BUTTON_ID, CLOSE_EMPTY)
                )

                minimize_switch = (
                    call(change_appearance, MINIMIZE_BUTTON_ID, CONTROL_MINIMIZED),
                    call(change_appearance, MINIMIZE_BUTTON_ID, MINIMIZE_EMPTY)
                )
                
                maximize_switch = (
                    call(change_appearance_maximize, 'enter'),
                    call(change_appearance_maximize, 'leave')
                )
                
                
                control_buttons = [
                    Button(icon=MAXIMIZE_EMPTY, id=MAXIMIZE_BUTTON_ID,
                        func=call(control_action, 'max'), focus=False, icon_size=size, hover=maximize_switch),
                    Button(icon=MINIMIZE_EMPTY, id=MINIMIZE_BUTTON_ID,
                        func=call(control_action, 'min'), focus=False, icon_size=size, hover=minimize_switch),
                    Button(icon=CLOSE_EMPTY, id=CLOSE_BUTTON_ID,
                        func=Window.quit, focus=False, icon_size=size, hover=close_switch)
                ]

                if align != center:
                    if widgets == None:
                        policy = expand
                    else:
                        policy = fixed
                else:
                    policy = expand

                items = [
                    titlebar_icon,
                    Text(title, id=TITLE_TEXT_ID,
                        sizepolicy=(policy, fixed), alignment=align),
                    control_buttons[slot_one],
                    control_buttons[slot_two],
                    control_buttons[slot_three]
                    
                ]

                return items

            if default == False:
                if current_window_style == SYSTEM_PLATFORM_FUSION:
                    title_items = icon_controls(1, 0, 2, 18) 
                else:
                    title_items = icon_controls(1, 0, 2, 40) 
            else:
               title_items = icon_controls(0, 1, 2, 18) 


            container = INIT_WIDGET(
                '-clera_titlebar_container-', QToolBar('Container'))
            titlebar = INIT_WIDGET('titlebar', QToolBar('Titlebar'))

            class init_titlebar(QWidget):
                def __init__(self):
                    super().__init__()
                    cs_layout = QHBoxLayout()
                    self.setLayout(cs_layout)
                    cs_layout.setContentsMargins(0, 0, 0, 0)
                    cs_layout.addWidget(titlebar)
                    window.setCentralWidget(self)

                def mousePressEvent(self, event: QMouseEvent):
                    self.old_position = window.mousePressEvent(event)
                    window.setCursor(Qt.SizeAllCursor)

                def mouseMoveEvent(self, event: QMouseEvent):
                    omega = window.mouseMoveEvent(event)
                    window.move(window.x() + omega.x(), window.y() + omega.y())
                    self.old_position = window.mousePressEvent(event)

                def mouseReleaseEvent(self, event: QMouseEvent):
                    window.setCursor(Qt.ArrowCursor)

                def mouseDoubleClickEvent(self, event: QMouseEvent):
                    if window._fixed_size == (None, None):
                        control_action('max')

            container_socket = init_titlebar()
            container_socket.setContentsMargins(0, 0, 0, 0)

            container.addWidget(container_socket)
            container.setStyleSheet('margin: 0; padding: 0; border: 0px;')

            container.setMovable(False)
            titlebar.setMovable(False)

            self.addToolBar(Qt.TopToolBarArea, container)

            container.toggleViewAction().setVisible(False)
            titlebar.toggleViewAction().setVisible(False)

            titlebar.setIconSize(QSize(20, 20))

            # self.addToolBar(Qt.TopToolBarArea, titlebar)

            self.addToolBarBreak()

            if widgets != None:
                titlebar_widget = []

                def init_titlebar_items(start, stop):
                    for _index in range(start, stop):
                        titlebar_widget.append(title_items[_index])

                if align == center:
                    for widget in widgets:
                        # titlebar_widget.append(widget)
                        append_items(titlebar_widget, widget)
                    else:
                        init_titlebar_items(0, 5)             
                else:
                    init_titlebar_items(0, 2)
                    for widget in widgets:
                        # titlebar_widget.append(widget)
                        append_items(titlebar_widget, widget)
                    else:
                        init_titlebar_items(2, 5)
                        # print(titlebar_widget)

                title_items = titlebar_widget

            for item in title_items:
                if type(item) != type(list()):
                    widget_type, widget_items = check_func(item)
                    LayItOut(titlebar, widget_type, widget_items)
                    # titlebar.addWidget(widget)

            titlebar.setOrientation(Qt.Horizontal)

            # button_style_query = button_style.lower()

            # button_styles = {
            #     circle: CONTROL_BUTTON_CIRCLE,
            #     square: CONTROL_BUTTON_SQUARE 
            # }

            # try:
            #     control_button_style = button_styles[button_style_query]
            # except:
            #     ...
            #     # raise an error

            title = GET(TITLE_TEXT_ID)
            minimize = GET(MINIMIZE_BUTTON_ID)
            maximize = GET(MAXIMIZE_BUTTON_ID)
            close = GET(CLOSE_BUTTON_ID)

            def init_title_icon(icon, value: str = 'left'):
                if icon != None:
                    icon = GET(ICON_IMAGE_ID)
                    icon.style(f'margin-{value}: 10px;')

            init_title_icon(icon)

            titlebar_padding = "7px"

            if default == False:
                if current_window_style == SYSTEM_PLATFORM_FUSION:
                    fusion_style(minimize, maximize, close)
                elif current_window_style == SYSTEM_PLATFORM_WINDOWS or windows in current_window_style:
                    windows_style(minimize, maximize, close)
                    titlebar_padding = 0
                else:
                    ...
            else:
                clera_style(minimize, maximize, close)

            title.style(
                f'color: {text_color}; margin: 0 4px;')
            container.setStyleSheet(
                f'border-bottom: 0px; background: {backgound_color}; max-height: 30px; color: {text_color}; padding: {titlebar_padding} 0')

            self._custom_title_bar = True


# ------------------------------------------------------------------------#

###########################################################################
############################## WINDOWS CLASS ##############################
###########################################################################

# ------------------------------------------------------------------------#


class Window:
    def __init__(self, title: str = DEFAULT_WINDOW_TITLE, icon: str = DEFAULT_WINDOW_ICON, size: tuple = DEFAULT_WINDOW_SIZE,
                 geometry: tuple = DEFAULT_WINDOW_GEOMETRY, style: str = DEFAULT_WINDOW_STYLE, fixed_size: tuple = DEFAULT_WINDOW_FIXED_SIZE, frame: bool = True,
                 movable: bool = False, top: bool = False, spacing: int = 5, margin: tuple = (5, 5, 5, 5), move: tuple = (None, None), tool: bool = False, cursor: bool = True):
        '''
        :param title:
        :param icon:
        :param size:
        :param geometry:
        :param style:
        :param fixed_size:
        :param frame:
        :param movable:
        :param top:
        :param spacing:
        :param margin:
        :param move:
        :param tool:
        :param cursor:
        '''
        global window

        self.window_title = title
        self.window_icon = icon
        self.window_size = size
        self.window_fixed_size = fixed_size
        self.window_geometry = geometry
        self.window_style = style
        self.frame = frame
        self.movable = movable
        self.top = top
        self.spacing = spacing
        self.content_margin = margin
        self.move = move
        self.tool = tool
        self.cursor = cursor

        window = MainWindow(self.window_title, self.window_icon,
                            self.window_size, self.window_fixed_size, self.window_geometry, self.window_style, self.frame,
                            self.movable, self.top, self.spacing, self.content_margin, self.move, self.tool, self.cursor)
    
    def __register_cursor__(self):
        app.setOverrideCursor(window.cursor())
        app.changeOverrideCursor(window.cursor())

    def run(self, css: None = None):
        # if self.splashscreen != None:
        #     self.init_splashscreen()

        window.show()
        # self.__register_cursor__() # block cursor

        if css != None:
            init_window_css(css)

        if len(LINK_ITEMS_INCLUDED) != 0:
            init_linked_files()

        def window_state():
            state = str(window.windowState())
            state = state.split('.')
            state = state[1].lower()
            return state

        state = window_state()
        try:
            max = GET(MAXIMIZE_BUTTON_ID)

            if state == 'windowmaximized':
                max.value(CONTROL_RESTORE)

            if window._query_fixed_size == True:
                max.delete()

            if window._custom_title_bar == True:
                menu_bar = window.menuBar()
                menu_bar.clear()

        except:
            ...

        app.exec()
        self.quit()

    def close(self):
        self.quit()

    def quit(self):
        app.quit()

    def update(self, remove_id, widget):
        replace_widget = WIDGET_ID_SAFE[remove_id]

        widget_type, widget_items = check_func(widget)

        try:
            layout.indexOf(replace_widget)
            LayItOut([layout, replace_widget, 'replaceWidget'],
                     widget_type, widget_items)
            layout.removeWidget(replace_widget)
            replace_widget.deleteLater()
            replace_widget = None
        except:
            pass

    def normal(self):
        window.setWindowState(Qt.WindowNoState)

    def minimize(self):
        window.setWindowState(Qt.WindowMinimized)

    def maximize(self):
        window.setWindowState(Qt.WindowMaximized)

    def details(self):
        screen = window.screen().virtualSize()
        _title = window.windowTitle()

        if len(_title) == 0:
            _title = None

        size = window.size()

        window_details = {
            'position': window.geometry().getCoords()[:2],
            'screen': (screen.width(), screen.height()),
            'style': window.style().name(),
            'size': (size.width(), size.height()),
            'title': _title,
            'system_styles': QStyleFactory().keys(),
            'style_reference': FILE_LINKS
        }

        return window_details

    def title(self, value: any = None):
        if value != None:
            window.setWindowTitle(value)
        
    def resize(self, size: tuple, fixed: bool=False):
        width, height = size

        if width != None and height != None:
            if fixed == True:
                window.setFixedSize(QSize(int(width), int(height)))
            else:
                window.resize(QSize(int(width), int(height)))
    
    def screenshot(self, filename: str):
        details = self.details()
        x, y = details['position']
        w, h = details['size']
        
        if window.isHidden() == False:
            window.screen().grabWindow(x=x, y=y, w=w, h=h).save(filename)

    def _cursor(self, hide: bool = False):
        if hide == True:
            window.setCursor(Qt.BlankCursor)
        elif hide == False:
            window.unsetCursor()

        self.__register_cursor__()

    def _move(self, position: tuple = (None, None), top: bool = None):
        positionx, positiony = position

        if positionx != None and positiony != None:
            window.move(positionx, positiony)

        def handle_top_flag():
            if top == True:
                window.setWindowFlag(Qt.WindowStaysOnTopHint)
            elif top == False:
                window.setWindowFlags(window.windowFlags() & ~Qt.WindowStaysOnTopHint)

            window.show()

        handle_top_flag()

    # def init_splashscreen(self):
    #     splash_screen = QSplashScreen(QPixmap(init_image(self.splashscreen)), Qt.WindowStaysOnTopHint)
    #     splash_screen.show()
        
    #     if self.splash_function != None:
    #     # Perform a function during splash screen
    #         self.splash_function() 
        
    #     splash_screen.finish(DEFAULT_WINDOW_LAYOUT)
    
    def style(self, css: None=None, reset: bool = False):
        set_style(window, css, reset)

    # def _tool(self):
    #     window.setWindowFlag(~Qt.Tool)


    # def frames(self, value):
    #     # if value != window.frame:

    #     if value == False:
    #         window.setWindowFlag(Qt.FramelessWindowHint)
    #     elif value == True:
    #         window.setWindowFlag(~Qt.FramelessWindowHint)

    #     print(window.windowFlags())
    #     window.show()


# ------------------------------------------------------------------------#

###########################################################################
############################## CORE HANDLERS ##############################
###########################################################################

# ------------------------------------------------------------------------#


def handle_group(widgets, grouplayout, strict):
    groupcontent = QButtonGroup(grouplayout)
    for items in widgets:

        WidgetType, items = check_func(items)
        groupcontent.addButton(
            LayItOut(grouplayout, WidgetType, items))

    groupcontent.setExclusive(strict)


def init_column(hbox, vbox, property):
    hbox.addLayout(vbox)

    for properties in property[1]:
        col_hbox = QHBoxLayout()
        vbox.addLayout(col_hbox)
        for property in properties:
            WidgetType, property = check_func(property)
            if WidgetType != ELEM_TYPE_COLUMN:
                LayItOut(col_hbox, WidgetType, property)
            else:
                hbox.addLayout(vbox)
                for properties in property[1]:
                    col_hbox = QHBoxLayout()
                    vbox.addLayout(col_hbox)
                    for property in properties:
                        WidgetType, property = check_func(property)
                        LayItOut(col_hbox, WidgetType, property)


def init_menubar(menu_items):
    if menu_items != None:
        for items in menu_items:
            if len(items) == 2:
                name, actions = items
            else:
                if type(items[0]) == type(str()):
                    name = items[0]
                    actions = None
                else:
                    name = None
                    actions = items[0]

            window.WindowMenubar(name, actions)


# ------------------------------------------------------------------------#

###########################################################################
############################# LAYOUT PROCESSOR ############################
###########################################################################

# ------------------------------------------------------------------------#


def Box(widgets, margin: tuple | int = None, spacing: int=None, _parent: any=None):
    containers = [ELEM_TYPE_COLUMN, ELEM_TYPE_FIELDSET,
                  ELEM_TYPE_GROUP]
    box_layout = QVBoxLayout()

    if _parent == None:
        box_widget = QWidget()

        if get_parent(BOX_IDENTIFIER):
            box_widget = DEFAULT_WINDOW_LAYOUT
            box_layout = layout
            window.setCentralWidget(box_widget)
    else:
        box_widget = _parent

    box_widget.setLayout(box_layout)

    for items in widgets:
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        box_layout.addLayout(hbox)

        for item in items:
            widget_type, widget_items = check_func(item)

            if widget_type not in containers:
                LayItOut(hbox, widget_type, widget_items)
            elif widget_type == ELEM_TYPE_COLUMN:
                init_column(hbox, vbox, widget_items)
            elif widget_type == ELEM_TYPE_FIELDSET:

                Notrequired, name, widgets, id, fieldset_layout = widget_items
                if widgets != None:

                    groupbox = INIT_WIDGET(id, QGroupBox(name))
                    hbox.addWidget(groupbox)

                    if fieldset_layout.lower() in DEFAULT_VERTICAL_TYPES:
                        groupbox_layout = QVBoxLayout()
                    elif fieldset_layout.lower() in DEFAULT_HORIZONTAL_TYPES:
                        groupbox_layout = QHBoxLayout()
                    else:
                        raise ValueError(fieldset_layout)

                    groupbox.setLayout(groupbox_layout)

                    for items in widgets:
                        widget_type, widget_items = check_func(items)
                        if widget_type == ELEM_TYPE_GROUP:

                            NotRequired, widgets, group_layout, strict = items
                            if widgets != None:
                                if group_layout.lower() in DEFAULT_HORIZONTAL_TYPES:
                                    group_element_layout = QHBoxLayout()
                                elif group_layout.lower() in DEFAULT_VERTICAL_TYPES:
                                    group_element_layout = QVBoxLayout()
                                else:
                                    raise ValueError(group_layout)

                                groupbox_layout.addLayout(group_element_layout)
                                handle_group(widgets, group_element_layout, strict)
                        else:
                            LayItOut(groupbox_layout,
                                     widget_type, widget_items)

            elif widget_type == ELEM_TYPE_GROUP:

                Notrequired, widgets, group_layout, strict = widget_items

                if widgets != None:

                    if group_layout.lower() in DEFAULT_VERTICAL_TYPES:
                        group_element_layout = QVBoxLayout()
                    elif group_layout.lower() in DEFAULT_HORIZONTAL_TYPES:
                        group_element_layout = QHBoxLayout()
                    else:
                        raise ValueError(group_layout)
                    box_layout.addLayout(group_element_layout)
                    handle_group(widgets, group_element_layout, strict)
    # returns a QWidget and layout like QVBoxLayout
    
    is_margin = init_content_margin(box_layout, margin)
    init_spacing(box_layout, spacing)

    return [box_widget, box_layout, is_margin]


def Grid(widgets, margin: tuple | int=None, spacing: int=None):
    grid_widget = QWidget()
    grid = QGridLayout()

    grid_layout = QVBoxLayout()

    if get_parent(GRID_IDENTIFIER):
        grid_widget = DEFAULT_WINDOW_LAYOUT
        grid_layout = layout

        window.setCentralWidget(grid_widget)
        grid_layout.addLayout(grid)

    grid_widget.setLayout(grid)

    grid_pos_x = 0
    grid_pos_y = 0

    for items in widgets:
        for item in items:
            widget_type, widget_items = check_func(item)
            LayItOut(grid, widget_type, widget_items, grid_pos_x, grid_pos_y)
            grid_pos_y += 1
        grid_pos_y = 0
        grid_pos_x += 1

    is_margin = init_content_margin(grid_layout, margin)
    init_spacing(grid_layout, spacing)
    return [grid_widget, grid_layout, is_margin]


class ScrollArea:
    def __init__(self, widgets: None = None, id: None = None, contain: bool = True):
        '''
        ScrollArea

        :param widgets:
        :param id:
        :param contain:
        '''

        elem_type = ELEM_TYPE_SCROLL_AREA
        self.scroll_widget = QWidget()

        if  get_parent(ELEM_TYPE_TAB) and get_parent(SCROLL_AREA_IDENTIFIER):
            # layout.addWidget(scroll_area)
            window.setCentralWidget(self.scroll_widget)

        scroll_layout = QVBoxLayout()

        scroll_area = INIT_WIDGET(id, QScrollArea())
        scroll_layout.addWidget(scroll_area)
        self.scroll_widget.setLayout(scroll_layout)
        
        if widgets != None:
            widgets = widgets[0]
            scroll_area.setWidget(widgets)
        scroll_area.setAlignment(Qt.AlignBottom)
        scroll_area.setWidgetResizable(contain)

        

    def __repr__(self):
        return [self.scroll_widget]

    def __call__(self):
        return [self.scroll_widget]
        


class scrollarea(ScrollArea):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Stack:
    def __init__(self, widgets: None = None, id: None = None, current_changed: None = None, widget_removed: None = None):
        '''
        Stack Widget

        :param widgets:
        :param id:
        :param current_changed:
        :param widget_removed:
        '''
        self.stacked_widget = INIT_WIDGET(id, QStackedWidget())
        layout_default = QVBoxLayout()
        stack_default = QWidget()

        def init_stack(widget):
            stack_layout = widget[1]
            is_margin = widget[2]
            
            try:
                widget = widget[0]
            except:
                widget = widget()[0]
            
            if is_margin != True:
                init_content_margin(stack_layout, 0)
            self.stacked_widget.addWidget(widget)

        if widgets != None:
            if process_request(ELEM_TYPE_SCROLL_AREA, str(type(widgets)).lower()):
                widgets = widgets()
            
            if type(widgets[0]) == sample_list:
                for widget in widgets:
                    init_stack(widget)    
            else:
                init_stack(widgets)    
        
        layout_default.addWidget(self.stacked_widget)
        stack_default.setLayout(layout_default)

        self.stacked_widget.currentChanged.connect(current_changed)
        self.stacked_widget.widgetRemoved.connect(widget_removed)
        
        layout_default.setContentsMargins(0, 0, 0, 0)
        window.setCentralWidget(stack_default)

    def set(self, index):
        self.stacked_widget.setCurrentIndex(index)

    def show(self, widget):
        widget, layout = widget
        self.stacked_widget.setCurrentWidget(widget)


class stack(Stack):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# ------------------------------------------------------------------------#

###########################################################################
############################## CORE ELEMENTS ##############################
###########################################################################

# ------------------------------------------------------------------------#


class Menubar:
    def __init__(self, menu_items: list | None = None):
        '''
        Menu Bar

        :param menu_items:
        '''

        self.menu_items = menu_items

        init_menubar(self.menu_items)


class menubar(Menubar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Titlebar:
    def __init__(self, title: str = path.basename(sys.argv[0]), icon: str = None, widgets: list = None, alignment: None = None, text_color: str = 'white',
                 background_color: str = 'rgb(32, 32, 32)', default: bool = False):
        '''
        Titlebar

        :param title:
        :param widgets:
        :param alignment:
        :param text_color:
        :param background_color:
        :param height:
        :param button_style:
        '''
        window.WindowTitlebar(title, icon, widgets, alignment,
                              background_color, text_color, default)


class titlebar(Titlebar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Toolbar:
    def __init__(self, name, tool_items: list | None = None, movable: bool = False,
                 position: str = top, id: None = None, iconsize: tuple = (None, None),
                 border: bool = True, orientation: str = SET_HORIZONTAL, newline: bool = False, toggle_view: bool = True):
        '''
        Toolbar Element

        :param name:
        :param tool_items:
        :param movable:
        :param position:
        :param id:
        :param iconsize:
        :param border:
        :param orientation:
        :param newline:
        '''

        window.WindowToolbar(name,  tool_items, movable,  position,  id,  iconsize,  border,
                             orientation, newline, toggle_view)


class toolbar(Toolbar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Statusbar:
    def __init__(self):
        window.init_status()

    def message(self, text: str = '', time: None = None):
        '''
        Display temporary status message

        :param text:
        :param time: in seconds.
        '''
        window.SHOW_STATUSBAR_MESSAGE(text, time)

    def clear(self):
        window.CLEAR_STATUSBAR_MESSAGE()

    def add(self, widget, type: str = SET_NORMAL):
        type = type.upper()
        widget_type, widget_items = check_func(widget)
        if type == SET_NORMAL:
            window.ADD_NORMAL_WIDGET(widget_type, widget_items)
        elif type == SET_STATIC:
            window.ADD_PERMANENT_WIDGET(widget_type, widget_items)
        else:
            raise ValueError(f'"{type}" is an invalid type value')

    def remove(self, id):
        window.REMOVE_STATUSBAR_WIDGET(id)


class statusbar(Statusbar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class File(QFileDialog):
    def __init__(self):
        ...

    def open(self: None = QFileDialog, caption: str = None, filter: str = '(All Files: *)', directory: str = None, type: str = DEFAULT_OPEN_FILE_TYPE):
        '''
        Open File Dialog

        :param caption:
        :param filter:
        :param directory:
        :param type:
        '''

        open_type = type.lower()

        if type == OPEN_FILE_TYPE_SINGLE:
            file = self.getOpenFileName(
                caption=caption,
                dir=directory,
                filter=get_filter(filter))

            # file_names = file[0]
            return file

        elif open_type == OPEN_FILE_TYPE_MULTI:
            files = self.getOpenFileNames(
                caption=caption,
                dir=directory,
                filter=get_filter(filter))

            return files

    def save(self: None = QFileDialog, filter: str = '(All Files: *)'):
        '''
        Save File Dialog

        :param filter:
        '''

        file = self.getSaveFileName(filter=get_filter(filter))

        return file


class file(File):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Folder(QFileDialog):
    def __init__(self, caption: str = None, directory: str = None):
        '''
        Folder Dialog

        :param caption:
        :param directory:
        '''
        
        self.folder = self.getExistingDirectory(caption=caption,
                                                dir=directory)

    def __repr__(self):
        return self.folder


class folder(Folder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Popup:
    def __init__(self, title: None = None, widgets: None = None, id: None = None, size: tuple = (None, None), fixed_size: tuple = (None, None), move: tuple = (None, None),
                 modal: bool = False, frame: bool = True, lock: bool = False, center: bool = True, margin: tuple | int = None, spacing: int = None):
        '''
        Popup Window

        :param title:
        :param widgets:
        :param id:
        :param size:
        :param fixe_size:
        :param move:
        :param modal:
        :param frame:
        :param lock:
        :param center:
        :param margin:
        :param spacing:
        '''

        if lock == True:
            parent = DEFAULT_WINDOW_LAYOUT
        else:
            parent = None

        elem_type = ELEM_TYPE_POPUP

        popup = INIT_WIDGET(id, QDialog(parent))
        
        self.popup = popup

        popup.setWindowTitle(title)

        if widgets != None:
            Box(widgets, margin, spacing, popup)
            # popup.setLayout(popup_layout[1])

        popup.setModal(modal)

        width, height = size
        if width != None and height != None:
            popup.resize(int(width), int(height))
        
        fixed_width, fixed_height = fixed_size
        if fixed_width != None and fixed_height != None:
            popup.setFixedSize(QSize(int(fixed_width), int(fixed_height)))

        # popup.resize(200, 120)
        
        def center_self():
            win = window.geometry().center()
            _size = popup.size()
            
            x = (win.x() - (_size.width() / 2))
            y = (win.y() - (_size.height() / 2))
            
            popup.move(x, y)

        if frame == False:
            popup.setWindowFlag(Qt.FramelessWindowHint)

        # Display Popup Window
        if popup.isModal:
            popup.show()
        else:
            popup.exec()

        position_x, position_y = move
        if position_x != None and position_y != None:
            popup.move(position_x, position_y)
        else:
            if center == True:
                center_self()


        self.rtn = [elem_type, id, popup]

    def __call__(self):
        return self.rtn

    def result(self):
        return self.popup.result()

    def close(self):
        self.popup.close()
    

class popup(Popup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ColorPicker:
    def __init__(self, title: None = None, id: None = None, modal: bool = False, 
                 frame: bool = True, lock: bool = False, color_selected: None = None, 
                 native: bool = True, current: str | None = None):

        if lock == True:
            parent = DEFAULT_WINDOW_LAYOUT
        else:
            parent = None

        elem_type = ELEM_TYPE_POPUP

        popup = INIT_WIDGET(id, QColorDialog(parent))

        self.popup = popup

        popup.setWindowTitle(title)

        
        popup.setModal(modal)

        # popup.resize(200, 120)

        if frame == False:
            popup.setWindowFlag(Qt.FramelessWindowHint)

        if native == False:
            popup.setOption(QColorDialog.DontUseNativeDialog)
        
        popup.setOption(QColorDialog.ShowAlphaChannel)
        popup.colorSelected.connect(color_selected)

        if popup.isModal:
            popup.show()
        else:
            popup.exec()

        def get_rgb_value(mode, current):
            current = current.removeprefix(f'{mode}(').removesuffix(')')
            current = current.split(',')

            current = [int(value) for value in current]

            if len(current) == 3:
                r, g, b = current
                current = QColor(r, g, b)
            else:
                r, g, b, a = current
                current = QColor(r, g, b, a)
            
            popup.setCurrentColor(current)


        if current.startswith('rgba'):
            get_rgb_value('rgba', current)
        elif current.startswith('rgb'):
            get_rgb_value('rgb', current)
        else:
            popup.setCurrentColor(current)
            
        self.rtn = [elem_type, id, popup]

    def __call__(self):
        return self.rtn


class colorpicker(ColorPicker):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TabWidget:
    def __init__(self, tabs: None = None, id: None = None, movable: bool = False, closable: bool = False,
                 close_requested: None = None, clicked: None = None, current_changed: None = None):
        '''
        Tab Widget

        :param tabs:
        :param id:
        :param movable:
        :param closable:
        :param close_requested:
        :param clicked:
        :param current_changed:
        '''

        elem_type = ELEM_TYPE_TAB

        tab_widget = INIT_WIDGET(id, QTabWidget())

        if tabs != None:
            add_tabs(tab_widget, tabs)

        tab_widget.setMovable(movable)
        tab_widget.setTabsClosable(closable)

        tab_widget.tabCloseRequested.connect(close_requested)
        tab_widget.tabBarClicked.connect(clicked)
        tab_widget.currentChanged.connect(current_changed)

        layout.addWidget(tab_widget)
        window.setCentralWidget(DEFAULT_WINDOW_LAYOUT)

        self.rtn = [elem_type, id]

    def __call__(self):
        return self.rtn


class tabwidget(TabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Highlighter(QSyntaxHighlighter):
    def __init__(self, mapping, parent=None):
        super().__init__(parent)
        self.mapping = mapping

    def highlightBlock(self, text):
        for pattern, format in self.mapping.items():
            for match in re.finditer(pattern, text):
                start, end = match.span()
                self.setFormat(start, end-start, format)


class Highlight:
    def __init__(self, widget_id, synthax, id: None = None):

        mapping = {}

        for item in synthax.items():
            pattern, format = item
        
            pattern = rf'{pattern}'
            _format = INIT_FORMAT(format)

            mapping[pattern] = _format
        
        self.widget = WIDGET_ID_SAFE[widget_id]
        self.synthax = INIT_WIDGET(id, Highlighter(mapping))
        self.synthax.setDocument(self.widget.document())
        self.synthax.document()


def thread(target, wait: bool = False, *args, **kwargs):
    if wait == True:
        return lambda: clera_multi_threading.start(target, *args, **kwargs)
    elif wait == False:
        clera_multi_threading.start(target, *args, **kwargs)


def screen():
    try:
        core = window
    except:
        core = DEFAULT_WINDOW_LAYOUT

    size = core.screen().virtualSize()

    return (size.width(), size.height())


def screenshot(filename: str):
    try:
        core = window
    except:
        core = DEFAULT_WINDOW_LAYOUT

    core.screen().grabWindow().save(filename)


def shortcut(keys: str, func: None = None):
    _shortcut = QShortcut(keys, window)
    _shortcut.activated.connect(func)


class GET:
    def __init__(self, id):

        '''
        GET ELEMENT

        :param id:

        :method value:
        :method update:
        :method delete:
        :method append:
        :method html:
        :method insert_html:
        :method plain_text:
        :method alignment:
        :method is_default:
        :method is_readonly:
        :method style:
        :method is_checked:
        :method hidden:
        :method hide:
        :method diabled:
        :method disable:
        :method enable:
        :method is_hidden:
        :method is_disabled:
        :method select_all:
        :method copy:
        :method cut:
        :method undo:
        :method redo:
        :method paste:
        :method clear:
        :method add:
        :method remove:
        :method current:
        :method count:
        :method selected_items:
        :method set:
        :method index:
        :method reset:
        :method minimum:
        :method maximum:
        :method is_text_visible:
        :method reject:
        :method accept:
        :method focus:
        :method cursor:
        :method setcursor:
        :method icon:
        :method show:
        :method scrollbar:
        :method checked:
        '''
        self.id = id
        self.widget = WIDGET_ID_SAFE[self.id]
        self.widget_type = str(type(self.widget))

    def __repr__(self):
        allowed = [
            [
                GET_ELEM_TYPE_PROGRESS_BAR,
                GET_ELEM_TYPE_SLIDER,
                GET_ELEM_TYPE_DIAL
            ],

            GET_ELEM_TYPE_TEXTAREA
        ]

        if process_request(allowed[0], self.widget_type):
            return str(self.widget.value())
        elif process_request(allowed[1], self.widget_type):
            return self.widget.toPlainText()
        elif process_request(GET_ELEM_TYPE_COLOR_POPUP, self.widget_type):
            return str(self.widget.selectedColor().name(QColor.HexRgb))
        else:
            return self.widget.text()

    def value(self, value: str | None = None):
        allowed = [
            GET_ELEM_TYPE_PROGRESS_BAR,
            GET_ELEM_TYPE_SLIDER,
            GET_ELEM_TYPE_DIAL
        ]

        if process_request(allowed, self.widget_type):
            self.widget.setValue(int(value))
        else:
            self.widget.setText(str(value))

    def update(self, widget):
        widget_type, widget_items = check_func(widget)

        try:
            layout.indexOf(self.widget)
            LayItOut([layout, self.widget, 'replaceWidget'],
                     widget_type, widget_items)
            layout.removeWidget(self.widget)
            self.widget.deleteLater()
            self.widget = None
        except:
            ...

        # WIDGET_ID_SAFE.pop(self.id)

    def delete(self):
        layout.removeWidget(self.widget)
        self.widget.deleteLater()
        self.widget = None

        # WIDGET_ID_SAFE.pop(self.id)

    def append(self, value: str = ''):
        allowed = [
            GET_ELEM_TYPE_TEXTAREA
        ]

        if process_request(allowed, self.widget_type):
            self.widget.append(value)

    def html(self, value):
        allowed = [
            GET_ELEM_TYPE_TEXTAREA
        ]

        if process_request(allowed, self.widget_type):
            self.widget.setHtml(value)

    def insert_html(self, value):
        allowed = [
            GET_ELEM_TYPE_TEXTAREA
        ]

        if process_request(allowed, self.widget_type):
            self.widget.insertHtml(value)

    def plain_text(self, value: None = None):
        allowed = [
            GET_ELEM_TYPE_TEXTAREA
        ]

        if process_request(allowed, self.widget_type):
            if value != None:
                self.widget.setPlainText(value)
            else:
                return self.widget.toPlainText()

    def alignment(self, value: None = None):
        if value != None:
            make_alignment(self.widget, value)
        else:
            return self.widget.alignment()

    def is_default(self):
        return self.widget.isDefault()

    def is_readonly(self):
        return self.widget.isReadonly()

    def style(self, css: None = None, reset: bool = False):
        set_style(self.widget, css, reset)

    def is_checked(self):
        return self.widget.isChecked()

    def hidden(self, value: bool | None = None):
        if value != None:
            self.widget.setHidden(value)

    def hide(self):
        self.widget.setHidden(True)
    
    def disabled(self, value: bool | None = None):
        if value != None:
            self.widget.setDisabled(value)

    def disable(self):
        self.widget.setDisabled(True)

    def enable(self):
        self.widget.setEnabled(True)

    def is_hidden(self):
        return self.widget.isHidden()

    def is_disabled(self):
            return self.widget.isDisabled()

    def select_all(self):
        allowed = [
            GET_ELEM_TYPE_TEXTAREA
        ]

        if process_request(allowed, self.widget_type):
            self.widget.selectAll()

    def copy(self):
        allowed = [
            GET_ELEM_TYPE_TEXTAREA
        ]

        if process_request(allowed, self.widget_type):
            self.widget.copy()

    def cut(self):
        allowed = [
            GET_ELEM_TYPE_TEXTAREA
        ]

        if process_request(allowed, self.widget_type):
            self.widget.cut()

    def undo(self):
        allowed = [
            GET_ELEM_TYPE_TEXTAREA
        ]

        if process_request(allowed, self.widget_type):
            self.widget.undo()

    def redo(self):
        allowed = [
            GET_ELEM_TYPE_TEXTAREA
        ]

        if process_request(allowed, self.widget_type):
            self.widget.redo()

    def paste(self):
        allowed = [
            GET_ELEM_TYPE_TEXTAREA
        ]

        if process_request(allowed, self.widget_type):
            self.widget.paste()

    def clear(self):
        allowed = [
            GET_ELEM_TYPE_TEXTAREA,
            GET_ELEM_TYPE_LISTWIDGET,
            GET_ELEM_TYPE_SELECT,
            GET_ELEM_TYPE_TAB_WIDGET,

            GET_ELEM_TYPE_INPUT
        ]

        if process_request(allowed[0:4], self.widget_type):
            self.widget.clear()
        elif process_request(allowed[4], self.widget_type):
            self.widget.setText('')

    def add(self, items):
        allowed = [
            GET_ELEM_TYPE_LISTWIDGET,
            GET_ELEM_TYPE_SELECT,
            GET_ELEM_TYPE_TAB_WIDGET,
            GET_ELEM_TYPE_STACKED
        ]

        if process_request(allowed[0], self.widget_type):
            add_list_items(self.widget, items)
        elif process_request(allowed[1], self.widget_type):
            if type(items[0]) == sample_list:
                pass
            elif type(items[0]) == sample_string:
                items = [items]
        elif process_request(allowed[2], self.widget_type):
            add_tabs(self.widget, items)
        elif process_request(allowed[3], self.widget_type):
            add_stacks(self.widget, items)

    def remove(self, items):
        allowed = [
            GET_ELEM_TYPE_LISTWIDGET,
            GET_ELEM_TYPE_SELECT,
            GET_ELEM_TYPE_TAB_WIDGET,
            GET_ELEM_TYPE_STACKED
        ]

        if process_request(allowed[0], self.widget_type):
            self.widget.takeItem(items)
        elif process_request(allowed[1], self.widget_type):
            self.widget.removeItem(items)
        elif process_request(allowed[2], self.widget_type):
            self.widget.removeTab(items)
        elif process_request(allowed[3], self.widget_type):
            def init_remove(widget):
                widget, layout = widget
                if widget != None:
                    self.widget.removeWidget(widget)
            
            
            if type(items) == sample_integer:
                # Handle later
                items = [self.widget.widget(items), None]
                init_remove(items)
            elif type(items[0]) == sample_list:
                for item in items:
                    init_remove(item)
            else:
                init_remove(items)


    def current(self):
        allowed = [
            GET_ELEM_TYPE_LISTWIDGET,
            GET_ELEM_TYPE_SELECT,
            [
                GET_ELEM_TYPE_TAB_WIDGET,
                GET_ELEM_TYPE_STACKED
            ]
        ]

        if process_request(allowed[0], self.widget_type):
            return self.widget.currentRow()
        elif process_request(allowed[1], self.widget_type):
            return self.widget.currentText()
        elif process_request(allowed[2], self.widget_type):
            return self.widget.currentIndex()

    def count(self):
        allowed = [
            GET_ELEM_TYPE_LISTWIDGET,
            GET_ELEM_TYPE_SELECT,
            GET_ELEM_TYPE_TAB_WIDGET,
            GET_ELEM_TYPE_STACKED
        ]

        if process_request(allowed, self.widget_type):
            return self.widget.count()

    def selected_items(self):
        allowed = [
            GET_ELEM_TYPE_LISTWIDGET,
        ]

        if process_request(allowed, self.widget_type):
            selected_items = [items.text()
                              for items in self.widget.selectedItems()]
            return selected_items

    def set(self, value):
        allowed = [
            GET_ELEM_TYPE_SELECT,
            GET_ELEM_TYPE_STACKED
        ]

        if process_request(allowed, self.widget_type):
            self.widget.setCurrentIndex(value)


    def index(self):
        allowed = [
            GET_ELEM_TYPE_SELECT,
            GET_ELEM_TYPE_STACKED
        ]

        if process_request(allowed, self.widget_type):
            return self.widget.currentIndex()

    def reset(self):
        allowed = [
            GET_ELEM_TYPE_PROGRESS_BAR,
        ]

        if process_request(allowed, self.widget_type):
            self.widget.reset()

    def minimum(self):
        allowed = [
            GET_ELEM_TYPE_PROGRESS_BAR,
        ]

        if process_request(allowed, self.widget_type):
            return self.widget.minimum()

    def maximum(self):
        allowed = [
            GET_ELEM_TYPE_PROGRESS_BAR,
        ]

        if process_request(allowed, self.widget_type):
            return self.widget.maximum()

    def is_text_visible(self):
        allowed = [
            GET_ELEM_TYPE_PROGRESS_BAR,
        ]

        if process_request(allowed, self.widget_type):
            return self.widget.isTextVisible()

    def reject(self, result: int = None):
        allowed = [
            GET_ELEM_TYPE_POPUP,
        ]

        if process_request(allowed, self.widget_type):
            self.widget.reject()
            if result != None:
                self.widget.setResult(result)

    def accept(self, result: int = None):
        allowed = [
            GET_ELEM_TYPE_POPUP,
        ]

        if process_request(allowed, self.widget_type):
            self.widget.accept()
            if result != None:
                self.widget.setResult(result)
    
    def focus(self, value: bool = True):
        allowed = [
            GET_ELEM_TYPE_INPUT,
            GET_ELEM_TYPE_TEXTAREA
        ]

        if process_request(allowed, self.widget_type):
            self.widget.setFocus()
    

    def has_focus(self, value: bool = True):
        allowed = [
            GET_ELEM_TYPE_INPUT,
            GET_ELEM_TYPE_TEXTAREA
        ]

        if process_request(allowed, self.widget_type):
            return self.widget.hasFocus()

    def cursor(self):
        allowed = [
            GET_ELEM_TYPE_INPUT,
            GET_ELEM_TYPE_TEXTAREA
        ]

        if process_request(allowed, self.widget_type):
            cursor = self.widget.textCursor()
            position = cursor.position()

            return cursor, position

    
    def setcursor(self, cursor):
        cursor, position = cursor

        cursor.setPosition(position)
        self.widget.setTextCursor(cursor)

    def icon(self, path):
        self.widget.setIcon(QIcon(init_image(path)))

    def show(self, widget):
        allowed = [
            GET_ELEM_TYPE_STACKED,
            GET_ELEM_TYPE_TAB_WIDGET,

        ]

        if process_request(allowed[0], self.widget_type):
            widget, layout = widget
            self.widget.setCurrentWidget(widget)
        elif process_request(allowed[1], self.widget_type):
            self.widget.setCurrentIndex(widget)

    def scrollbar(self, scrollbar: None = None, bar_type: str = 'v', id: None = None):
        allowed = [
            GET_ELEM_TYPE_TEXTAREA
        ]

        if process_request(allowed, self.widget_type):
            if scrollbar != None:
                if bar_type == 'v':
                    self.widget.setVerticalScrollBar(scrollbar)
                elif bar_type == 'h':
                    self.widget.setHorizontalScrollBar(scrollbar)
            else:
                if bar_type == 'v':
                    bar =  self.widget.verticalScrollBar()
                elif bar_type == 'h':
                    bar = self.widget.horizontalScrollBar()
                else:
                    bar = None

                if bar != None:
                    return INIT_WIDGET(id, bar)
                else:
                    return bar
                
    def hex(self):
        allowed = [
            GET_ELEM_TYPE_COLOR_POPUP
        ]

        if process_request(allowed, self.widget_type):
            return self.widget.selectedColor().name(QColor.HexRgb)

    
    def rgba(self):
        allowed = [
            GET_ELEM_TYPE_COLOR_POPUP
        ]

        if process_request(allowed, self.widget_type):
            return self.widget.selectedColor().getRgb()


    def checked(self, value: bool = True):
        allowed = [
            GET_ELEM_TYPE_RADIO_BUTTON,
            GET_ELEM_TYPE_CHECK_BOX
        ]

        if process_request(allowed, self.widget_type):
            self.widget.setChecked(value)

class get(GET):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# ------------------------------------------------------------------------#

###########################################################################
############################## EASE OF ACCESS #############################
###########################################################################

# ------------------------------------------------------------------------#


class Exit(Button):
    def __init__(self, label: str = 'Exit', icon: None = None, id: None = None,
                 disabled: bool = False, default: bool = False, grid: tuple = (None, None),
                 sizepolicy: tuple = (None, None), checkable: bool = False, checked: bool = False, hidden: bool = False, focus: bool = True, 
                 icon_size: int = 20, statustip: str = None, tooltip: str = None, shortcut: str = None, hover: None = None):

        elem_type = ELEM_TYPE_BUTTON

        self.rtn = [elem_type, label, Window.quit, icon, id,
                    disabled, default, grid, sizepolicy, checkable, checked, hidden, focus, icon_size, statustip, tooltip, shortcut, hover]

    def __call__(self):
        return self.rtn


class exit(Exit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Copy(Button):
    def __init__(self, Target_ID, button_text: str = 'Copy', icon: None = None,
                 id: None = None, disabled: bool = False, default: bool = False,
                 grid: tuple = (None, None), sizePolicy: tuple = (None, None), checked: bool = False, hidden: bool = False, focus: bool = True, 
                 icon_size: int = 20, statustip: str = None, tooltip: str = None, shortcut: str = None, hover: None = None):

        elem_type = elem_type, id = pre_widget_process('copy')
        METHOD_COPY.append(f'{id}:{Target_ID}')

        self.rtn = [elem_type, button_text, action_copy, icon, id,
                    disabled, default, grid, sizePolicy, True, checked, hidden, focus, icon_size, statustip, tooltip, shortcut, hover]

    def __call__(self):
        return self.rtn


class copy(Copy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Cut(Button):
    def __init__(self, Target_ID, button_text: str = 'Cut', icon: None = None,
                 id: None = None, disabled: bool = False, default: bool = False,
                 grid: tuple = (None, None), sizePolicy: tuple = (None, None), checked: bool = False, hidden: bool = False, focus: bool = True, 
                 icon_size: int = 20, statustip: str = None, tooltip: str = None, shortcut: str = None, hover: None = None):

        elem_type, id = pre_widget_process('cut')
        METHOD_CUT.append(f'{id}:{Target_ID}')

        self.rtn = [elem_type, button_text, action_cut, icon, id,
                    disabled, default, grid, sizePolicy, True, checked, hidden, focus, icon_size, statustip, tooltip, shortcut, hover]

    def __call__(self):
        return self.rtn


class cut(Cut):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Paste(Button):
    def __init__(self, Target_ID, button_text: str = 'Paste', icon: None = None,
                 id: None = None, disabled: bool = False, default: bool = False,
                 grid: tuple = (None, None), sizePolicy: tuple = (None, None), checked: bool = False, hidden: bool = False, focus: bool = True, 
                 icon_size: int = 20, statustip: str = None, tooltip: str = None, shortcut: str = None, hover: None = None):

        elem_type, id = pre_widget_process('paste')
        METHOD_PASTE.append(f'{id}:{Target_ID}')

        self.rtn = [elem_type, button_text, action_paste, icon, id,
                    disabled, default, grid, sizePolicy, True, checked, hidden, focus, icon_size, statustip, tooltip, shortcut, hover]

    def __call__(self):
        return self.rtn


class paste(Paste):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Undo(Button):
    def __init__(self, Target_ID, button_text: str = 'Undo', icon: None = None,
                 id: None = None, disabled: bool = False, default: bool = False,
                 grid: tuple = (None, None), sizePolicy: tuple = (None, None), checked: bool = False, hidden: bool = False, focus: bool = True, 
                 icon_size: int = 20, statustip: str = None, tooltip: str = None, shortcut: str = None, hover: None = None):

        elem_type = elem_type, id = pre_widget_process('undo')
        METHOD_UNDO.append(f'{id}:{Target_ID}')

        self.rtn = [elem_type, button_text, action_undo, icon, id,
                    disabled, default, grid, sizePolicy, True, checked, hidden, focus, icon_size, statustip, tooltip, shortcut, hover]

    def __call__(self):
        return self.rtn


class undo(Undo):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Redo(Button):
    def __init__(self, Target_ID, button_text: str = 'Redo', icon: None = None,
                 id: None = None, disabled: bool = False, default: bool = False,
                 grid: tuple = (None, None), sizePolicy: tuple = (None, None), checked: bool = False, hidden: bool = False, focus: bool = True, 
                 icon_size: int = 20, statustip: str = None, tooltip: str = None, shortcut: str = None, hover: None = None):

        elem_type = elem_type, id = pre_widget_process('redo')
        METHOD_REDO.append(f'{id}:{Target_ID}')

        self.rtn = [elem_type, button_text, action_redo, icon, id,
                    disabled, default, grid, sizePolicy, True, checked, hidden, focus, icon_size, statustip, tooltip, shortcut, hover]

    def __call__(self):
        return self.rtn


class redo(Redo):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# ------------------------------------------------------------------------#

###########################################################################
############################## CONTROL BUTTONS ############################
###########################################################################

# ------------------------------------------------------------------------#


def minimize():
    return GET(MINIMIZE_BUTTON_ID)


def maximize():
    return GET(MAXIMIZE_BUTTON_ID)


def close():
    return GET(CLOSE_BUTTON_ID)


def title():
    return GET(TITLE_TEXT_ID)


# ------------------------------------------------------------------------#

###########################################################################
############################### MANUAL WINDOW #############################
###########################################################################

# ------------------------------------------------------------------------#


# def main():
#     window = Window()
#     Box([[Button('UNAVAILABLE')]])
#     window.run()


# ------------------------------------------------------------------------#

###########################################################################
########################### CLERA STYLING EDITOR ##########################
###########################################################################

# ------------------------------------------------------------------------#

# def key():
#     print(QStyleFactory.keys())

# key()
