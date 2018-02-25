# -*- coding: UTF-8 -*-
"""Default values of the parameters"""

GRAPH_WIDTH_NAME = u'width'
GRAPH_WIDTH = u'700'

GRAPH_HEIGHT_NAME = u'height'
GRAPH_HEIGHT = u'300'

GRAPH_XAXIS_NAME = u'x'
GRAPH_YAXIS_NAME = u'y'
GRAPH_TITLE_NAME = u'title'
GRAPH_TOOLTIP_NAME = u'tooltip'
GRAPH_LEGEND_NAME = u'legend'


# Sequence of the default colors
CURVE_COLOR_NAME = u'color'
CURVE_COLORS = [u'#0051FF', u'#FF0000', u'#19D400', u'#000000',
                u'#FF8214', u'#B700FF', u'#1E9E19', u'#9C571F',
                u'#8C8741']

CURVE_SYMBOLS = [u'circle',
                 u'square',
                 u'diamond',
                 u'triangle',
                 u'triangle-down']

CURVE_STYLES = [u'solid', u'longdash', u'shortdash', u'shortdot',
                u'shortdashdot', u'shortdashdotdot', u'dot', u'dash',
                u'dashdot', u'longdashdot', u'longdashdotdot']

CURVE_STYLE_NAME = u'style'

CURVE_STYLE_AUTO = u'auto'

# Default curve thickness
CURVE_WIDTH_NAME = u'width'
CURVE_WIDTH = u'3'

# Numbers of the columns in data
CURVE_YCOL_NUMBER_NAME = u'ycol'
CURVE_YCOL_NUMBER = None

CURVE_XCOL_NUMBER_NAME = u'xcol'
CURVE_XCOL_NUMBER = None

# X coordinates are the row number
CURVE_XCOL_NUMBER_VALUE = u'number'

# Data source
CURVE_DATA_NAME = u'data'
CURVE_DATA_OBJECT_NAME = u'data'


# If CURVE_DATA is None, data reads from command content
# else CURVE_DATA is name of the Attachment
CURVE_DATA = None

CURVE_TITLE_NAME = u'title'
CURVE_HIDE_NAME = u'hide'


DATA_COLUMNS_SEPARATOR_NAME = u'colsep'
DATA_COLUMNS_SEPARATOR_DEFAULT = r'\s+'

# For selection render engine (at the time is not used)
RENDER_NAME = u'render'
RENDER_HIGHCHARTS = u'highcharts'


# Axis properties
AXIS_TITLE_NAME = u'title'
AXIS_MIN_NAME = u'min'
AXIS_MAX_NAME = u'max'

# Axis types
AXIS_TYPE_NAME = u'type'
AXIS_TYPE_DATE = u'datetime'

# Data properties
DATA_FORMAT_COL = u'formatcol'
DATA_SKIP_ROWS_NAME = u'skiprows'

AXIS_MAJOR_TICK_INTERVAL_NAME = u'tickstep'

TOOLBAR_DATAGRAPH = 'Plugin_DataGraph'
MENU_DATAGRAPH = 'Plugin_DataGraph'
