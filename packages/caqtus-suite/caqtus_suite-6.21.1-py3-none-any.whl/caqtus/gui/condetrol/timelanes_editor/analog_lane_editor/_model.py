from typing import Optional, Any, assert_never

from PySide6.QtCore import QObject, QModelIndex, Qt, QPersistentModelIndex
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu

from caqtus.types.expression import Expression
from caqtus.types.timelane import AnalogTimeLane, Ramp, Step
from .._time_lane_model import ColoredTimeLaneModel

_DEFAULT_INDEX = QModelIndex()


class AnalogTimeLaneModel(ColoredTimeLaneModel[AnalogTimeLane]):
    # ruff: noqa: N802
    def __init__(self, name: str, parent: Optional[QObject] = None):
        lane = AnalogTimeLane([Expression("...")])
        super().__init__(name, lane, parent)

    def data(self, index, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        value = self._lane[index.row()]
        if role == Qt.ItemDataRole.DisplayRole:
            if isinstance(value, Expression):
                return str(value)
            elif isinstance(value, Ramp):
                return "\u279F"
            else:
                assert_never(value)
        elif role == Qt.ItemDataRole.EditRole:
            if isinstance(value, Expression):
                return str(value)
            return None
        elif role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignCenter
        else:
            return super().data(index, role)

    def flags(self, index) -> Qt.ItemFlag:
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
        flags = super().flags(index)
        if isinstance(self._lane[index.row()], Ramp):
            flags &= ~Qt.ItemFlag.ItemIsEditable
        return flags

    def setData(self, index, value: Any, role: int = Qt.ItemDataRole.EditRole):
        if not index.isValid():
            return False
        if role == Qt.ItemDataRole.EditRole:
            start, stop = self._lane.get_bounds(Step(index.row()))
            if isinstance(value, str):
                self._lane[start:stop] = Expression(value)
                self.dataChanged.emit(index, index)
                return True
            elif isinstance(value, Ramp):
                self._lane[start:stop] = value
                self.dataChanged.emit(index, index)
                return True
            else:
                raise TypeError(f"Invalid type for value: {type(value)}")
        return False

    def insertRow(
        self, row, parent: QModelIndex | QPersistentModelIndex = _DEFAULT_INDEX
    ) -> bool:
        return self.insert_value(row, Expression("..."))

    def get_cell_context_actions(self, index: QModelIndex) -> list[QAction | QMenu]:
        if not index.isValid():
            return []

        cell_type_menu = QMenu("Cell type")
        value = self._lane[index.row()]
        expr_action = cell_type_menu.addAction("expression")
        if isinstance(value, Expression):
            expr_action.setCheckable(True)
            expr_action.setChecked(True)
        else:
            expr_action.triggered.connect(
                lambda: self.setData(index, "...", Qt.ItemDataRole.EditRole)
            )
        ramp_action = cell_type_menu.addAction("ramp")
        if isinstance(value, Ramp):
            ramp_action.setCheckable(True)
            ramp_action.setChecked(True)
        else:
            ramp_action.triggered.connect(
                lambda: self.setData(index, Ramp(), Qt.ItemDataRole.EditRole)
            )

        return super().get_cell_context_actions(index) + [cell_type_menu]
