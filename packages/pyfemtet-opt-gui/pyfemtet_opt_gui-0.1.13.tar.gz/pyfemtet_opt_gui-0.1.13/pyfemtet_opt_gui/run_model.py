from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QStandardItem
from PySide6.QtWidgets import QStyledItemDelegate, QComboBox

from pyfemtet_opt_gui.item_as_model import MyStandardItemAsTableModel, _isnumeric


import pyfemtet_opt_gui._p as _p


class RunConfigTableDelegate(QStyledItemDelegate):

    def __init__(self, model: 'RunModel'):
        super().__init__()
        self._model: 'RunModel' = model

    def createEditor(self, parent, option, index):
        col, row = index.column(), index.row()
        col_name = self._model.get_col_name(col)
        key_name = self._model.get_key_name(row)
        if col_name == 'value' and key_name == 'アルゴリズム':
            # コンボボックスエディタを作成
            comboBox = QComboBox(parent)
            comboBox.addItems(['PoFBoTorch', 'TPE', 'NSGA2', 'Random', 'QMC'])
            comboBox.setFrame(False)
            return comboBox
        return super().createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        col, row = index.column(), index.row()
        col_name = self._model.get_col_name(col)
        key_name = self._model.get_key_name(row)
        if col_name == 'value' and key_name == 'アルゴリズム':
            # コンボボックスにデータを設定
            value = index.model().data(index, Qt.ItemDataRole.EditRole)
            editor.setCurrentText(value)
        else:
            super().setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        col, row = index.column(), index.row()
        col_name = self._model.get_col_name(col)
        key_name = self._model.get_key_name(row)
        if col_name == 'value' and key_name == 'アルゴリズム':
            # コンボボックスのデータをモデルに設定
            model.setData(index, editor.currentText(), Qt.ItemDataRole.EditRole)
        else:
            super().setModelData(editor, model, index)

    def paint(self, painter, option, index):
        col, row = index.column(), index.row()
        col_name = self._model.get_col_name(col)
        key_name = self._model.get_key_name(row)
        if col_name == 'value' and key_name == 'アルゴリズム':
            # index...proxyindex
            # _model...original
            value = self._model.get_item(index.row()+1, index.column()).text()
            combo = QComboBox()
            combo.addItems([value])
            combo.setCurrentText(value)
            combo.setFrame(False)

            painter.save()

            painter.translate(option.rect.topLeft())
            combo.resize(option.rect.size())
            combo.render(painter, QPoint())

            painter.restore()
        else:
            super().paint(painter, option, index)


class RunModel(MyStandardItemAsTableModel):
    """A table to set arguments for FEMOpt.optimize().

    use              | key          | value                           | description
    --------------------------------------------------------------------------------------------
    checkbox         | n_trials     | 10 (positive int only)          | 指定回数の解析が終了すると最適化を終了します。
    checkbox         | timeout      | 10 (minutes, positive int only) | 指定時間（分）のプロセスが終了すると最適化を終了します。
    None             | n_parallel   | 1 (positive int only)           | 指定数の Femtet プロセスを使用して並列計算します。並列数分のライセンスが必要です。

    # if both n_trials and timeout are Unchecked, show warning.
    # use and key  are uneditable.
    # if Uncheckable, the row is disabled excluding use column.

    """
    HEADER = ['use', 'key', 'value', 'description']
    ROW_COUNT = 4  # including header row

    def initialize_table(self):
        # initialize table
        table: QStandardItem = self._item
        table.clearData()
        table.setText(self._category)
        table.setRowCount(self.ROW_COUNT)
        table.setColumnCount(3)
        self.set_header(self.HEADER)
        self._root.setColumnCount(max(self._root.columnCount(), self._item.columnCount()))

    def __init__(self, table_item: QStandardItem, root: QStandardItem, parent=None):
        super().__init__(table_item=table_item, root=root, parent=parent)

        self.initialize_table()

        # notify to start editing to the abstract model
        self.beginResetModel()

        # set data to table
        self._item.setRowCount(self.ROW_COUNT)

        # ===== n_trial =====
        # use
        item = QStandardItem()
        item.setCheckable(True)
        item.setCheckState(Qt.CheckState.Unchecked)
        self._item.setChild(1, 0, item)
        # item
        item = QStandardItem('n_trials')
        self._item.setChild(1, 1, item)
        # value
        item = QStandardItem('10')
        self._item.setChild(1, 2, item)
        # description
        item = QStandardItem('指定回数の解析が終了すると最適化を終了します。')
        self._item.setChild(1, 3, item)

        # ===== timeout =====
        # use
        item = QStandardItem()
        item.setCheckable(True)
        item.setCheckState(Qt.CheckState.Unchecked)
        self._item.setChild(2, 0, item)
        # item
        item = QStandardItem('timeout')
        self._item.setChild(2, 1, item)
        # value
        item = QStandardItem('3')
        self._item.setChild(2, 2, item)
        # description
        item = QStandardItem('指定時間（分）のプロセスが終了すると最適化を終了します。')
        self._item.setChild(2, 3, item)

        # ===== n_parallel =====
        # use
        item = QStandardItem()
        self._item.setChild(3, 0, item)
        # item
        item = QStandardItem('n_parallel')
        self._item.setChild(3, 1, item)
        # value
        item = QStandardItem('1')
        self._item.setChild(3, 2, item)
        # description
        item = QStandardItem('指定数の Femtet プロセスを使用して並列計算します。並列数分のライセンスが必要です。')
        self._item.setChild(3, 3, item)

        # ===== algorithm =====
        # use
        row = 4
        item = QStandardItem()
        self._item.setChild(row, 0, item)
        # item
        item = QStandardItem('アルゴリズム')
        self._item.setChild(row, 1, item)
        # value
        item = QStandardItem('PoFBoTorch')
        self._item.setChild(row, 2, item)
        # description
        item = QStandardItem('サンプリングアルゴリズムを指定します。')
        self._item.setChild(row, 3, item)

        # notify to end editing to the abstract model
        self.endResetModel()

    def get_key_name(self, row) -> str:
        col = self.get_col_from_name('key')
        return self.get_item(row, col).text()

    def flags(self, index):
        if not index.isValid(): return super().flags(index)

        col, row = index.column(), index.row()
        col_name = self.get_col_name(col)

        # use is checkable
        if col_name == 'use':
            return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable

        # if checkbox is false, disable the row (excluding use column).
        key_name = self.get_key_name(row)
        if key_name in ['n_trials', 'timeout']:
            use_col = self.get_col_from_name('use')
            use_item = self.get_item(row, use_col)
            if use_item.checkState() == Qt.CheckState.Unchecked:
                if col_name != 'use':
                    return ~Qt.ItemFlag.ItemIsEnabled

        # key is uneditable
        if col_name == 'key':
            return Qt.ItemFlag.ItemIsEnabled

        # description is uneditable
        if col_name == 'description':
            return Qt.ItemFlag.ItemIsEnabled

        return super().flags(index)

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole) -> bool:
        if not index.isValid(): return super().setData(index, value, role)

        col, row = index.column(), index.row()
        col_name = self.get_col_name(col)

        # set_to must be numeric if direction is 'Set to...'
        if col_name == 'value':

            name_col = self.get_col_from_name('key')
            name_index = self.createIndex(row, name_col)
            name_value = self.data(name_index)

            if name_value == 'n_trials':
                raise_alert = False

                if not _isnumeric(value):
                    raise_alert = True
                else:
                    if float(value) != int(value):
                        raise_alert = True
                    else:
                        if int(value) <= 0:
                            raise_alert = True

                if raise_alert:
                    _p.logger.error('自然数を入力してください。')
                    return False

            if name_value == 'n_parallel':
                raise_alert = False

                if not _isnumeric(value):
                    raise_alert = True
                else:
                    if float(value) != int(value):
                        raise_alert = True
                    else:
                        if int(value) <= 0:
                            raise_alert = True

                if raise_alert:
                    _p.logger.error('自然数を入力してください。')
                    return False

            if name_value == 'timeout':
                raise_alert = False

                if not _isnumeric(value):
                    raise_alert = True
                else:
                    if float(value) <= 0:
                        raise_alert = True

                if raise_alert:
                    _p.logger.error('正の数を入力してください。')
                    return False

        return super().setData(index, value, role)

    def get_finish_conditions(self):
        finish_conditions = {}
        for row in range(1, self.rowCount()):
            col = self.get_col_from_name('use')
            item = self.get_item(row, col)

            # if checkable but unchecked, ignore
            if item.isCheckable() and item.checkState() == Qt.CheckState.Unchecked:
                continue

            # if used finish condition, add to out
            arg_key = self.get_key_name(row)
            if (arg_key == 'n_trials') or (arg_key == 'timeout'):
                col = self.get_col_from_name('value')
                arg_value = self.get_item(row, col).text()
                finish_conditions[arg_key] = arg_value

        return finish_conditions
