
from pygments.style import Style
from pygments.token import Keyword, Name, Literal, Number, String, Operator, \
                           Comment, Punctuation


class GraphiteStyle(Style):

    background_color = "transparent";
    default_style = ""

    styles = {
        Keyword:                'bold #eeeeee',
        Keyword.Constant:       'bold #88ccee',
        Keyword.Namespace:      'bold #ee8888',
        Keyword.Pseudo:         'bold #88ccee',
        Name:                   '#88ccee',
        Name.Builtin:           'bold #88eeee',
        Name.Class:             'bold #88ccee',
        Name.Function:          'bold #88ccee',
        Name.Decorator:         '#eeccee',
        Literal:                '#eeeecc',
        Number:                 '#eeeecc',
        String:                 '#88cc88',
        String.Escape:          'bold #88cc88',
        Operator:               '#eeeeee',
        Operator.Word:          'bold #eeeeee',
        Punctuation:            '#eeeeee',
        Comment:                '#cccccc',
    }


