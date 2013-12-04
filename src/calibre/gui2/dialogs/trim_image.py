#!/usr/bin/env python
# vim:fileencoding=utf-8
from __future__ import (unicode_literals, division, absolute_import,
                        print_function)

__license__ = 'GPL v3'
__copyright__ = '2013, Kovid Goyal <kovid at kovidgoyal.net>'

import sys

from PyQt4.Qt import (
    QDialog, QGridLayout, QToolBar, Qt, QLabel, QIcon, QDialogButtonBox, QSize,
    QApplication, QKeySequence)

from calibre.gui2 import gprefs
from calibre.gui2.tweak_book.editor.image import Canvas

class TrimImage(QDialog):

    def __init__(self, img_data, parent=None):
        QDialog.__init__(self, parent)
        self.l = l = QGridLayout(self)
        self.setLayout(l)
        self.setWindowTitle(_('Trim Image'))

        self.bar = b = QToolBar(self)
        l.addWidget(b)
        b.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        b.setIconSize(QSize(32, 32))

        self.msg = la = QLabel('\xa0' + _(
            'Select a region by dragging with your mouse on the image, and then click trim'))
        self.sz = QLabel('')

        self.canvas = c = Canvas(self)
        c.image_changed.connect(self.image_changed)
        c.load_image(img_data)
        self.undo_action = u = c.undo_action
        u.setShortcut(QKeySequence(QKeySequence.Undo))
        self.redo_action = r = c.redo_action
        r.setShortcut(QKeySequence(QKeySequence.Redo))
        self.trim_action = ac = self.bar.addAction(QIcon(I('trim.png')), _('&Trim'), c.trim_image)
        ac.setShortcut(QKeySequence('Ctrl+T'))
        ac.setToolTip('%s [%s]' % (_('Trim image by removing borders outside the selected region'), ac.shortcut().toString(QKeySequence.NativeText)))
        ac.setEnabled(False)
        c.selection_state_changed.connect(self.selection_changed)
        l.addWidget(c)
        self.bar.addAction(self.trim_action)
        self.bar.addSeparator()
        self.bar.addAction(u)
        self.bar.addAction(r)
        self.bar.addSeparator()
        self.bar.addWidget(la)
        self.bar.addSeparator()
        self.bar.addWidget(self.sz)

        self.bb = bb = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        bb.accepted.connect(self.accept)
        bb.rejected.connect(self.reject)
        l.addWidget(bb)

        self.resize(QSize(800, 600))
        geom = gprefs.get('image-trim-dialog-geometry', None)
        if geom is not None:
            self.restoreGeometry(geom)
        self.setWindowIcon(self.trim_action.icon())

    def selection_changed(self, has_selection):
        self.trim_action.setEnabled(has_selection)
        self.msg.setVisible(not has_selection)

    def image_changed(self, qimage):
        self.sz.setText('\xa0' + _('Size:') + '%dx%d' % (qimage.width(), qimage.height()))

    def cleanup(self):
        self.canvas.cleanup()
        gprefs.set('image-trim-dialog-geometry', bytearray(self.saveGeometry()))

    def accept(self):
        self.cleanup()
        QDialog.accept(self)

    def reject(self):
        self.cleanup()
        QDialog.reject(self)

if __name__ == '__main__':
    app = QApplication([])
    with open(sys.argv[-1], 'rb') as f:
        data = f.read()
    d = TrimImage(data)
    d.exec_()

