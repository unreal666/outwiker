# -*- coding: UTF-8 -*-

import wx

from ..i18n import get_
from ..diagramrender import DiagramRender

from .baseshapesdialog import BaseShapesDialog
from .propertyfactory import PropertyFactory


class InsertDiagramDialog (BaseShapesDialog):
    defaultShape = u"box"

    def __init__ (self, parent):
        super (InsertDiagramDialog, self).__init__ (parent)
        global _
        _ = get_()

        self.SetTitle (_(u"Insert Diagram"))

        self.__createGui()
        self.Fit()
        self.Center(wx.CENTRE_ON_SCREEN)


    def _getShapesList (self):
        return DiagramRender.shapes


    @property
    def isShapeDefault (self):
        """
        Свойство должно вернуть True, если выбрана фигура по умолчанию, и False в противном случае
        """
        return self._shape.GetStringSelection() == self.defaultShape


    def __createGui (self):
        mainSizer = wx.FlexGridSizer (cols = 2)
        mainSizer.AddGrowableCol (0)
        mainSizer.AddGrowableCol (1)

        propFactory = PropertyFactory (self)

        propFactory.createOrientation (self,
                                       mainSizer,
                                       _(u"Orientation"))

        self._createShapeRow (self,
                              mainSizer,
                              _(u"Default nodes shape"))

        propFactory.createColor (self,
                                 mainSizer,
                                 _(u"Set default nodes background color"),
                                 "white",
                                 "backColor",
                                 "isBackColorChanged")

        propFactory.createColor (self,
                                 mainSizer,
                                 _(u"Set default text color"),
                                 "black",
                                 "textColor",
                                 "isTextColorChanged")

        propFactory.createInteger (self,
                                   mainSizer,
                                   _(u"Set default font size"),
                                   "fontSize",
                                   "isFontSizeChanged",
                                   1,
                                   100,
                                   11)

        propFactory.createInteger (self,
                                   mainSizer,
                                   _(u"Set default nodes width"),
                                   "width",
                                   "isWidthChanged",
                                   1,
                                   1000,
                                   128)

        propFactory.createInteger (self,
                                   mainSizer,
                                   _(u"Set default nodes height"),
                                   "height",
                                   "isHeightChanged",
                                   1,
                                   1000,
                                   40)

        propFactory.createInteger (self,
                                   mainSizer,
                                   _(u"Set default horizontal span between nodes"),
                                   "spanWidth",
                                   "isSpanWidthChanged",
                                   0,
                                   1000,
                                   64)

        propFactory.createInteger (self,
                                   mainSizer,
                                   _(u"Set default vertical span between nodes"),
                                   "spanHeight",
                                   "isSpanHeightChanged",
                                   0,
                                   1000,
                                   40)

        helpLink = wx.HyperlinkCtrl (self,
                                     -1,
                                     _(u"Open the documentation page"),
                                     u"http://blockdiag.com/en/blockdiag/attributes/diagram.attributes.html")

        mainSizer.Add (helpLink,
                       flag = wx.ALIGN_LEFT | wx.ALL,
                       border = 4)

        mainSizer.AddSpacer (1)

        propFactory.createOkCancelButtons (mainSizer)

        # Выберем по умолчанию в качестве фигуры box
        boxIndex = self._shape.FindString (self.defaultShape)
        if boxIndex != wx.NOT_FOUND:
            self._shape.SetSelection (boxIndex)

        self.SetSizer (mainSizer)



class InsertDiagramController (object):
    def __init__ (self, dialog):
        """
        dialog - экземпляр класса InsertNodeDialog
        """
        self._dialog = dialog


    def showDialog (self):
        result = self._dialog.ShowModal()
        return result


    def getResult (self):
        """
        Возвращает кортеж из строк: (начало викикоманды с параметрами, конец викикоманды)
        Считается, что этот метод вызывают после того, как showDialog вернул значение wx.ID_OK
        """
        params = self._getParamString (self._dialog).strip()

        if len (params) == 0:
            return (u"(:diagram:)\n",
                    u"\n(:diagramend:)")
        else:
            return (u"(:diagram:)\n{}\n".format (params),
                    u"\n(:diagramend:)")


    def _getParamString (self, dialog):
        params = []
        params.append (self._getOrientationParam (dialog))
        params.append (self._getShapeParam (dialog))
        params.append (self._getBackColorParam (dialog))
        params.append (self._getTextColorParam (dialog))
        params.append (self._getFontSizeParam (dialog))
        params.append (self._getWidthParam (dialog))
        params.append (self._getHeightParam (dialog))
        params.append (self._getSpanWidthParam (dialog))
        params.append (self._getSpanHeightParam (dialog))

        return u"\n".join ([param for param in params if len (param.strip()) != 0])


    def _getShapeParam (self, dialog):
        """
        Возвращает строку с параметром, задающим фигуру
        """
        shape = dialog.shape

        return u"default_shape = {};".format (shape) if not dialog.isShapeDefault else u""


    def _getBackColorParam (self, dialog):
        return u'default_node_color = "{}";'.format (dialog.backColor) if dialog.isBackColorChanged else u""


    def _getTextColorParam (self, dialog):
        return u'default_textcolor = "{}";'.format (dialog.textColor) if dialog.isTextColorChanged else u""


    def _getFontSizeParam (self, dialog):
        return u'default_fontsize = {};'.format (dialog.fontSize) if dialog.isFontSizeChanged else u""


    def _getWidthParam (self, dialog):
        return u'node_width = {};'.format (dialog.width) if dialog.isWidthChanged else u""


    def _getHeightParam (self, dialog):
        return u'node_height = {};'.format (dialog.height) if dialog.isHeightChanged else u""

    def _getSpanWidthParam (self, dialog):
        return u'span_width = {};'.format (dialog.spanWidth) if dialog.isSpanWidthChanged else u""


    def _getSpanHeightParam (self, dialog):
        return u'span_height = {};'.format (dialog.spanHeight) if dialog.isSpanHeightChanged else u""


    def _getOrientationParam (self, dialog):
        return u'orientation = {};'.format (dialog.orientation) if dialog.orientationIndex != 0 else u""
