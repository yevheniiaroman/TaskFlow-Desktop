from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QLineEdit, QComboBox, QLabel,
    QHeaderView, QMessageBox, QFrame, QStackedWidget, QTextEdit,
    QScrollArea, QDialog, QFormLayout
)
from PyQt6.QtCore import Qt
from controllers.task_controller import TaskController
from models.task import Task

KANBAN_STYLESHEET = """
QMainWindow {
    background-color: #ffffff;
}
QWidget {
    font-family: 'Segoe UI', -apple-system, Arial, sans-serif;
    font-size: 13px;
    color: #1f2328;
}
/* Top Header Bar (GitHub Projects Style) */
#TopHeader {
    background-color: #f6f8fa;
    border-bottom: 1px solid #d0d7de;
}
#ProjectTitle {
    font-size: 22px;
    font-weight: 700;
    color: #1f2328;
}
QPushButton#TabBtn {
    background-color: transparent;
    border: none;
    border-bottom: 2px solid transparent;
    padding: 10px 16px;
    font-size: 14px;
    font-weight: 500;
    color: #656d76;
    border-radius: 0px;
}
QPushButton#TabBtn:hover {
    color: #1f2328;
    background-color: #eaeef2;
}
QPushButton#TabBtn[active="true"] {
    color: #1f2328;
    font-weight: 600;
    border-bottom: 3px solid #fd8c73;
    background-color: #ffffff;
}
/* Search Bar */
#FilterBar {
    background-color: #ffffff;
    border-bottom: 1px solid #d0d7de;
}
QLineEdit#SearchBox {
    background-color: #f6f8fa;
    border: 1px solid #d0d7de;
    border-radius: 6px;
    padding: 7px 12px;
    font-size: 13px;
    color: #1f2328;
}
QLineEdit#SearchBox:focus {
    background-color: #ffffff;
    border: 1.5px solid #0969da;
}
/* Kanban Column */
#KanbanColumn {
    background-color: #f6f8fa;
    border: 1px solid #d0d7de;
    border-radius: 8px;
}
#ColumnTitle {
    font-size: 16px;
    font-weight: 700;
    color: #1f2328;
}
#ColumnSubtitle {
    font-size: 10px;
    color: #656d76;
    margin-bottom: 2px;
}
#CountBadge {
    background-color: #eaeef2;
    color: #1f2328;
    font-size: 11px;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 10px;
}
/* Task Card */
#TaskCard {
    background-color: #ffffff;
    border: 1px solid #d0d7de;
    border-radius: 6px;
}
#TaskCard:hover {
    border: 1.5px solid #0969da;
}
#CardId {
    color: #656d76;
    font-size: 10px;
    font-weight: 500;
}
#CardTitle {
    color: #1f2328;
    font-size: 14px;
    font-weight: 600;
    padding-top: 2px;
    padding-bottom: 4px;
}
#P1Badge {
    background-color: #fff1e5;
    color: #bc4c00;
    border: 1px solid #ffb77c;
    border-radius: 10px;
    padding: 1px 6px;
    font-size: 10px;
    font-weight: 600;
}
#P2Badge {
    background-color: #ddf4ff;
    color: #0969da;
    border: 1px solid #80ccff;
    border-radius: 10px;
    padding: 1px 6px;
    font-size: 10px;
    font-weight: 600;
}
#P3Badge {
    background-color: #f6f8fa;
    color: #57606a;
    border: 1px solid #d0d7de;
    border-radius: 10px;
    padding: 1px 6px;
    font-size: 10px;
    font-weight: 600;
}
#SharedBadge {
    background-color: #f6f8fa;
    color: #57606a;
    border: 1px solid #d0d7de;
    border-radius: 10px;
    padding: 1px 7px;
    font-size: 10px;
}
/* Buttons */
QPushButton {
    background-color: #f6f8fa;
    border: 1px solid #d0d7de;
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 12px;
    font-weight: 500;
    color: #24292f;
}
QPushButton:hover {
    background-color: #f3f4f6;
}
QPushButton#GreenBtn {
    background-color: #1f883d;
    color: #ffffff;
    border: 1px solid #1a7f37;
    font-size: 13px;
    font-weight: 600;
}
QPushButton#GreenBtn:hover {
    background-color: #1a7f37;
}
QPushButton#CardActionBtn {
    background-color: #f6f8fa;
    border: 1px solid #d0d7de;
    border-radius: 4px;
    padding: 1px 5px;
    font-size: 10px;
}
QPushButton#CardActionBtn:hover {
    background-color: #eaeef2;
}
QPushButton#DangerBtn {
    background-color: #cf222e;
    color: #ffffff;
    border: none;
}
QPushButton#DangerBtn:hover {
    background-color: #a40e26;
}
/* Table in Team View */
QTableWidget {
    background-color: #ffffff;
    border: 1px solid #d0d7de;
    border-radius: 6px;
    gridline-color: #eaeef2;
    font-size: 13px;
}
QHeaderView::section {
    background-color: #f6f8fa;
    color: #24292f;
    font-size: 13px;
    font-weight: 700;
    padding: 9px;
    border: none;
    border-bottom: 1px solid #d0d7de;
}
"""

STATUS_COLUMNS = [
    ("Backlog", "#656d76", "This item hasn't been started"),
    ("Ready", "#0969da", "This is ready to be picked up"),
    ("In Progress", "#bf8700", "This is actively being worked on"),
    ("In Review", "#8250df", "This item is in review"),
    ("Done", "#1a7f37", "This has been completed"),
]


class TaskDialog(QDialog):
    """Fereastră popup curată pentru crearea sau editarea unui Task."""
    def __init__(self, parent, users: list[dict], task: Task = None, default_status: str = "Backlog"):
        super().__init__(parent)
        self.task = task
        self.setWindowTitle(f"Edit TaskFlow #{task.id}" if task else "Create New Task")
        self.setFixedWidth(420)
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.title_input = QLineEdit(task.title if task else "")
        self.title_input.setPlaceholderText("e.g., Implement Supabase sync...")

        self.desc_input = QTextEdit(task.description if task else "")
        self.desc_input.setMaximumHeight(70)
        self.desc_input.setPlaceholderText("Details or subtasks...")

        self.assignee_combo = QComboBox()
        self.assignee_combo.setEditable(True)
        for u in users:
            self.assignee_combo.addItem(u["name"])
        self.assignee_combo.addItem("Shared")
        if task:
            self.assignee_combo.setCurrentText(task.assignee)

        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["P1", "P2", "P3"])
        if task and task.priority in ["P1", "P2", "P3"]:
            self.priority_combo.setCurrentText(task.priority)

        self.status_combo = QComboBox()
        self.status_combo.addItems([c[0] for c in STATUS_COLUMNS])
        self.status_combo.setCurrentText(task.status if task else default_status)

        self.date_input = QLineEdit(task.due_date if task else "2026-11-30")

        form.addRow("Title:", self.title_input)
        form.addRow("Notes:", self.desc_input)
        form.addRow("Assignee:", self.assignee_combo)
        form.addRow("Priority:", self.priority_combo)
        form.addRow("Column:", self.status_combo)
        form.addRow("Due Date:", self.date_input)
        layout.addLayout(form)

        btns = QHBoxLayout()
        if task:
            self.delete_btn = QPushButton("Delete")
            self.delete_btn.setObjectName("DangerBtn")
            self.delete_btn.clicked.connect(self._on_delete)
            btns.addWidget(self.delete_btn)

        btns.addStretch()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        save_btn = QPushButton("Save Task")
        save_btn.setObjectName("GreenBtn")
        save_btn.clicked.connect(self.accept)

        btns.addWidget(cancel_btn)
        btns.addWidget(save_btn)
        layout.addLayout(btns)
        self.deleted = False

    def _on_delete(self):
        self.deleted = True
        self.accept()


class MainWindow(QMainWindow):
    def __init__(self, controller: TaskController):
        super().__init__()
        self.controller = controller
        self.selected_user_id = None
        self.setWindowTitle("TaskFlow — Desktop Project & Administration Board")
        self.resize(1340, 720)
        self.setStyleSheet(KANBAN_STYLESHEET)
        self._setup_ui()
        self.refresh_all()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # --- 1. TOP HEADER (GitHub Projects Style) ---
        header = QFrame()
        header.setObjectName("TopHeader")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(18, 12, 18, 0)
        header_layout.setSpacing(8)

        title_row = QHBoxLayout()
        proj_lbl = QLabel("🌐  TaskFlow")
        proj_lbl.setObjectName("ProjectTitle")
        title_row.addWidget(proj_lbl)
        title_row.addStretch()

        status_pill = QLabel(f"● {self.controller.get_connection_status()}")
        status_pill.setStyleSheet("color: #0969da; background-color: #ddf4ff; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: 600;")
        title_row.addWidget(status_pill)

        btn_reschedule = QPushButton("⏰ End-of-Day Reschedule (REQ04)")
        btn_reschedule.clicked.connect(self.handle_auto_reschedule)
        title_row.addWidget(btn_reschedule)

        btn_new = QPushButton("＋ New Task")
        btn_new.setObjectName("GreenBtn")
        btn_new.clicked.connect(lambda: self.open_task_dialog())
        title_row.addWidget(btn_new)

        header_layout.addLayout(title_row)

        # Tab-uri de navigare
        tabs_row = QHBoxLayout()
        tabs_row.setSpacing(4)
        self.tab_board_btn = QPushButton("◫  Current sprint (Board)")
        self.tab_board_btn.setObjectName("TabBtn")
        self.tab_board_btn.setProperty("active", True)
        self.tab_board_btn.clicked.connect(lambda: self.switch_tab(0))

        self.tab_team_btn = QPushButton("👥  Team && Roles Administration")
        self.tab_team_btn.setObjectName("TabBtn")
        self.tab_team_btn.setProperty("active", False)
        self.tab_team_btn.clicked.connect(lambda: self.switch_tab(1))

        tabs_row.addWidget(self.tab_board_btn)
        tabs_row.addWidget(self.tab_team_btn)
        tabs_row.addStretch()
        header_layout.addLayout(tabs_row)

        root.addWidget(header)

        # --- 2. FILTER BAR ---
        filter_bar = QFrame()
        filter_bar.setObjectName("FilterBar")
        f_layout = QHBoxLayout(filter_bar)
        f_layout.setContentsMargins(18, 10, 18, 10)

        self.search_input = QLineEdit()
        self.search_input.setObjectName("SearchBox")
        self.search_input.setPlaceholderText("🔍  Filter by keyword or team member (e.g., Evghenia, Ivo, Alexandra)...")
        self.search_input.textChanged.connect(self.refresh_board)
        f_layout.addWidget(self.search_input)

        btn_refresh = QPushButton("↻ Refresh")
        btn_refresh.clicked.connect(self.refresh_all)
        f_layout.addWidget(btn_refresh)
        root.addWidget(filter_bar)

        # --- 3. STACKED PAGES ---
        self.pages = QStackedWidget()
        self.board_page = QWidget()
        self._setup_board_page()
        self.team_page = QWidget()
        self._setup_team_page()

        self.pages.addWidget(self.board_page)
        self.pages.addWidget(self.team_page)
        root.addWidget(self.pages)

    def switch_tab(self, index: int):
        self.pages.setCurrentIndex(index)
        self.tab_board_btn.setProperty("active", index == 0)
        self.tab_team_btn.setProperty("active", index == 1)
        for btn in (self.tab_board_btn, self.tab_team_btn):
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    # --- PAGINA 1: KANBAN BOARD ---
    def _setup_board_page(self):
        layout = QHBoxLayout(self.board_page)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        self.column_widgets = {}
        self.column_counts = {}

        for status_name, dot_color, desc_text in STATUS_COLUMNS:
            col_frame = QFrame()
            col_frame.setObjectName("KanbanColumn")
            col_layout = QVBoxLayout(col_frame)
            col_layout.setContentsMargins(12, 12, 12, 12)
            col_layout.setSpacing(6)

            # Antet coloană
            top = QHBoxLayout()
            dot = QLabel("●")
            dot.setStyleSheet(f"color: {dot_color}; font-size: 15px;")
            lbl = QLabel(status_name)
            lbl.setObjectName("ColumnTitle")
            count_lbl = QLabel("0")
            count_lbl.setObjectName("CountBadge")

            add_col_btn = QPushButton("+")
            add_col_btn.setFixedSize(26, 26)
            add_col_btn.setStyleSheet("border: none; font-weight: bold; font-size: 16px; color: #656d76;")
            add_col_btn.clicked.connect(lambda _, s=status_name: self.open_task_dialog(default_status=s))

            top.addWidget(dot)
            top.addWidget(lbl)
            top.addWidget(count_lbl)
            top.addStretch()
            top.addWidget(add_col_btn)
            col_layout.addLayout(top)

            sub = QLabel(desc_text)
            sub.setObjectName("ColumnSubtitle")
            col_layout.addWidget(sub)

            # Zonă scrollabilă pentru carduri
            scroll = QScrollArea()
            scroll.setWidgetResizable(True)
            scroll.setFrameShape(QFrame.Shape.NoFrame)
            scroll.setStyleSheet("background-color: transparent;")

            cards_container = QWidget()
            cards_container.setStyleSheet("background-color: transparent;")
            cards_layout = QVBoxLayout(cards_container)
            cards_layout.setContentsMargins(0, 4, 0, 4)
            cards_layout.setSpacing(10)
            cards_layout.addStretch()

            scroll.setWidget(cards_container)
            col_layout.addWidget(scroll)

            layout.addWidget(col_frame)
            self.column_widgets[status_name] = cards_layout
            self.column_counts[status_name] = count_lbl

    def _create_task_card(self, task: Task) -> QFrame:
        card = QFrame()
        card.setObjectName("TaskCard")
        c_layout = QVBoxLayout(card)
        c_layout.setContentsMargins(12, 10, 12, 10)
        c_layout.setSpacing(6)

        # Rând 1: ID + Butoane mutare stânga/dreapta
        r1 = QHBoxLayout()
        id_lbl = QLabel(f"🟢 TaskFlow #{task.id}")
        id_lbl.setObjectName("CardId")
        r1.addWidget(id_lbl)
        r1.addStretch()

        statuses = [c[0] for c in STATUS_COLUMNS]
        curr_idx = statuses.index(task.status) if task.status in statuses else 0

        if curr_idx > 0:
            btn_left = QPushButton("◀")
            btn_left.setObjectName("CardActionBtn")
            btn_left.setToolTip(f"Move to {statuses[curr_idx - 1]}")
            btn_left.clicked.connect(lambda _, t=task, s=statuses[curr_idx - 1]: self.move_task_status(t, s))
            r1.addWidget(btn_left)

        if curr_idx < len(statuses) - 1:
            btn_right = QPushButton("▶")
            btn_right.setObjectName("CardActionBtn")
            btn_right.setToolTip(f"Move to {statuses[curr_idx + 1]}")
            btn_right.clicked.connect(lambda _, t=task, s=statuses[curr_idx + 1]: self.move_task_status(t, s))
            r1.addWidget(btn_right)

        btn_edit = QPushButton("✎")
        btn_edit.setObjectName("CardActionBtn")
        btn_edit.setToolTip("Edit / Delete Task")
        btn_edit.clicked.connect(lambda _, t=task: self.open_task_dialog(task=t))
        r1.addWidget(btn_edit)

        c_layout.addLayout(r1)

        # Rând 2: Titlu
        title_lbl = QLabel(task.title)
        title_lbl.setObjectName("CardTitle")
        title_lbl.setWordWrap(True)
        c_layout.addWidget(title_lbl)

        # Rând 3: Etichete (Prioritate + Assignee)
        r3 = QHBoxLayout()
        r3.setSpacing(6)
        prio_lbl = QLabel(task.priority)
        if task.priority in ("P1", "High"):
            prio_lbl.setObjectName("P1Badge")
        elif task.priority in ("P2", "Medium"):
            prio_lbl.setObjectName("P2Badge")
        else:
            prio_lbl.setObjectName("P3Badge")

        assignee_lbl = QLabel(task.assignee)
        assignee_lbl.setObjectName("SharedBadge")

        r3.addWidget(prio_lbl)
        r3.addWidget(assignee_lbl)
        r3.addStretch()
        c_layout.addLayout(r3)

        return card

    def refresh_board(self):
        query = self.search_input.text()
        tasks = self.controller.load_tasks(query, "All")

        for status_name, col_layout in self.column_widgets.items():
            while col_layout.count() > 1:
                item = col_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

        counts = {c[0]: 0 for c in STATUS_COLUMNS}
        for task in tasks:
            col_name = task.status if task.status in self.column_widgets else "Backlog"
            card = self._create_task_card(task)
            target_layout = self.column_widgets[col_name]
            target_layout.insertWidget(target_layout.count() - 1, card)
            counts[col_name] += 1

        for status_name, count in counts.items():
            self.column_counts[status_name].setText(str(count))

    def move_task_status(self, task: Task, new_status: str):
        self.controller.edit_task(
            task.id, task.title, task.description, task.assignee,
            task.priority, new_status, task.due_date
        )
        self.refresh_board()

    def open_task_dialog(self, task: Task = None, default_status: str = "Backlog"):
        dlg = TaskDialog(self, self.controller.get_users(), task, default_status)
        if dlg.exec():
            try:
                if task and dlg.deleted:
                    self.controller.remove_task(task.id)
                elif task:
                    self.controller.edit_task(
                        task.id,
                        dlg.title_input.text(),
                        dlg.desc_input.toPlainText(),
                        dlg.assignee_combo.currentText(),
                        dlg.priority_combo.currentText(),
                        dlg.status_combo.currentText(),
                        dlg.date_input.text()
                    )
                else:
                    self.controller.create_task(
                        dlg.title_input.text(),
                        dlg.desc_input.toPlainText(),
                        dlg.assignee_combo.currentText(),
                        dlg.priority_combo.currentText(),
                        dlg.status_combo.currentText(),
                        dlg.date_input.text()
                    )
                self.refresh_board()
            except ValueError as e:
                QMessageBox.warning(self, "Validation Error", str(e))

    def handle_auto_reschedule(self):
        count = self.controller.run_end_of_day_scheduler()
        self.refresh_board()
        QMessageBox.information(
            self,
            "End-of-Day Scheduler",
            f"Automated Rescheduling complete!\n{count} uncompleted task(s) moved to next day (+1) and priority escalated."
        )

    # --- PAGINA 2: TEAM & ROLES ---
    def _setup_team_page(self):
        layout = QHBoxLayout(self.team_page)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(16)

        left_box = QVBoxLayout()
        self.users_table = QTableWidget(0, 4)
        self.users_table.setHorizontalHeaderLabels(["ID", "Member Name", "Role", "Assigned Platform"])
        self.users_table.verticalHeader().setVisible(False)
        self.users_table.verticalHeader().setDefaultSectionSize(40)
        self.users_table.setColumnWidth(0, 45)
        self.users_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.users_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.users_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.users_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.users_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.users_table.itemSelectionChanged.connect(self.on_user_selected)
        left_box.addWidget(self.users_table)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_del = QPushButton("Remove Selected Member")
        btn_del.setObjectName("DangerBtn")
        btn_del.clicked.connect(self.handle_delete_user)
        btn_row.addWidget(btn_del)
        left_box.addLayout(btn_row)

        right_panel = QFrame()
        right_panel.setFixedWidth(320)
        right_panel.setStyleSheet("background-color: #f6f8fa; border: 1px solid #d0d7de; border-radius: 8px;")
        p_layout = QVBoxLayout(right_panel)
        p_layout.setContentsMargins(16, 16, 16, 16)
        p_layout.setSpacing(10)

        lbl = QLabel("Manage Team Member")
        lbl.setStyleSheet("font-size: 16px; font-weight: 700; border: none;")
        p_layout.addWidget(lbl)

        p_layout.addWidget(QLabel("Full Name:"))
        self.user_name_input = QLineEdit()
        p_layout.addWidget(self.user_name_input)

        p_layout.addWidget(QLabel("Role:"))
        self.user_role_input = QLineEdit()
        p_layout.addWidget(self.user_role_input)

        p_layout.addWidget(QLabel("Platform:"))
        self.user_platform_combo = QComboBox()
        self.user_platform_combo.addItems(["Mobile Application", "Desktop Application", "Web Application", "Backend / Database"])
        p_layout.addWidget(self.user_platform_combo)

        self.btn_save_user = QPushButton("＋ Register Member")
        self.btn_save_user.setObjectName("GreenBtn")
        self.btn_save_user.clicked.connect(self.handle_save_user)
        p_layout.addWidget(self.btn_save_user)

        btn_clear = QPushButton("Clear Selection")
        btn_clear.clicked.connect(self.clear_user_form)
        p_layout.addWidget(btn_clear)
        p_layout.addStretch()

        layout.addLayout(left_box, 3)
        layout.addWidget(right_panel, 1)

    def refresh_all(self):
        self.refresh_board()
        self.refresh_users_table()

    def refresh_users_table(self):
        users = self.controller.get_users()
        self._current_users = users
        self.users_table.setRowCount(len(users))
        for row, u in enumerate(users):
            self.users_table.setItem(row, 0, QTableWidgetItem(str(u["id"])))
            self.users_table.setItem(row, 1, QTableWidgetItem(u["name"]))
            self.users_table.setItem(row, 2, QTableWidgetItem(u["role"]))
            self.users_table.setItem(row, 3, QTableWidgetItem(u["platform"]))

    def on_user_selected(self):
        row = self.users_table.currentRow()
        if row < 0 or row >= len(self._current_users):
            return
        user = self._current_users[row]
        self.selected_user_id = user["id"]
        self.user_name_input.setText(user["name"])
        self.user_role_input.setText(user["role"])
        self.user_platform_combo.setCurrentText(user["platform"])
        self.btn_save_user.setText(f"Save Changes #{user['id']}")

    def clear_user_form(self):
        self.selected_user_id = None
        self.users_table.clearSelection()
        self.user_name_input.clear()
        self.user_role_input.clear()
        self.btn_save_user.setText("＋ Register Member")

    def handle_save_user(self):
        try:
            if self.selected_user_id is None:
                self.controller.create_user(
                    self.user_name_input.text(),
                    self.user_role_input.text(),
                    self.user_platform_combo.currentText()
                )
            else:
                self.controller.edit_user(
                    self.selected_user_id,
                    self.user_name_input.text(),
                    self.user_role_input.text(),
                    self.user_platform_combo.currentText()
                )
            self.clear_user_form()
            self.refresh_users_table()
        except ValueError as e:
            QMessageBox.warning(self, "Validation Error", str(e))

    def handle_delete_user(self):
        if self.selected_user_id is None:
            return
        self.controller.remove_user(self.selected_user_id)
        self.clear_user_form()
        self.refresh_users_table()