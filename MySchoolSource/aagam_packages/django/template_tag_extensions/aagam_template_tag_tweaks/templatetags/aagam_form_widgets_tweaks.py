import re
import types
from copy import copy
from django.template import Library, Node, TemplateSyntaxError

register = Library()


def silence_without_field(fn):
    def wrapped(field, attr):
        if not field:
            return ""
        return fn(field, attr)

    return wrapped


def _process_field_attributes(field, attr, process):
    # split attribute name and value from 'attr:value' string
    # params = attr.split(':', 1)
    # attribute = params[0]
    params = re.split(r"(?<!:):(?!:)", attr, 1)
    # attribute = params[0]
    attribute = params[0].replace("::", ":")
    value = params[1] if len(params) == 2 else True
    field = copy(field)
    # decorate field.as_widget method with updated attributes
    old_as_widget = field.as_widget

    def as_widget(self, widget=None, attrs=None, only_initial=False):
        attrs = attrs or {}
        process(widget or self.field.widget, attrs, attribute, value)
        if attribute == "type":  # change the Input type
            self.field.widget.input_type = value
            del attrs["type"]
        html = old_as_widget(widget, attrs, only_initial)
        self.as_widget = old_as_widget
        return html

    field.as_widget = types.MethodType(as_widget, field)
    return field


@register.filter("attr")
@silence_without_field
def set_attr(field, attr):
    def process(widget, attrs, attribute, value):  # pylint: disable=unused-argument
        attrs[attribute] = value

    return _process_field_attributes(field, attr, process)


@register.filter("add_error_attr")
@silence_without_field
def add_error_attr(field, attr):
    if hasattr(field, "errors") and field.errors:
        return set_attr(field, attr)
    return field


@register.filter("append_attr")
@silence_without_field
def append_attr(field, attr):
    def process(widget, attrs, attribute, value):
        if attrs.get(attribute):
            attrs[attribute] += " " + value
        elif widget.attrs.get(attribute):
            attrs[attribute] = widget.attrs[attribute] + " " + value
        else:
            attrs[attribute] = value

    return _process_field_attributes(field, attr, process)


@register.filter("add_class")
@silence_without_field
def add_class(field, css_class):
    return append_attr(field, "class:" + css_class)


@register.filter("add_label_class")
@silence_without_field
def add_label_class(field, css_class):
    return field.label_tag(attrs={"class": css_class})


@register.filter("add_error_class")
@silence_without_field
def add_error_class(field, css_class):
    if hasattr(field, "errors") and field.errors:
        return add_class(field, css_class)
    return field


@register.filter("add_required_class")
@silence_without_field
def add_required_class(field, css_class):
    if hasattr(field.field, "required") and field.field.required:
        return add_class(field, css_class)
    return field


@register.filter("set_data")
@silence_without_field
def set_data(field, data):
    return set_attr(field, "data-" + data)


@register.filter(name="field_type")
def field_type(field):
    """
    Template filter that returns field class name (in lower case).
    E.g. if field is CharField then {{ field|field_type }} will
    return 'charfield'.
    """
    if hasattr(field, "field") and field.field:
        return field.field.__class__.__name__.lower()
    return ""


@register.filter(name="widget_type")
def widget_type(field):
    """
    Template filter that returns field widget class name (in lower case).
    E.g. if field's widget is TextInput then {{ field|widget_type }} will
    return 'textinput'.
    """
    if (
        hasattr(field, "field")
        and hasattr(field.field, "widget")
        and field.field.widget
    ):
        return field.field.widget.__class__.__name__.lower()
    return ""


# ======================== render_field tag ==============================

ATTRIBUTE_RE = re.compile(
    r"""
    (?P<attr>
        [@\w:_\.-]+
    )
    (?P<sign>
        \+?=
    )
    (?P<value>
    ['"]? # start quote
        [^"']*
    ['"]? # end quote
    )
""",
    re.VERBOSE | re.UNICODE,
)


@register.tag
def render_field(parser, token):
    """
    Render a form field using given attribute-value pairs

    Takes form field as first argument and list of attribute-value pairs for
    all other arguments.  Attribute-value pairs should be in the form of
    attribute=value or attribute="a value" for assignment and attribute+=value
    or attribute+="value" for appending.
    """
    error_msg = (
        '%r tag requires a form field followed by a list of attributes and values in the form attr="value"'
        % token.split_contents()[0]
    )
    try:
        bits = token.split_contents()
        tag_name = bits[0]  # noqa
        form_field = bits[1]
        attr_list = bits[2:]
    except ValueError:
        raise TemplateSyntaxError(error_msg)

    form_field = parser.compile_filter(form_field)

    set_attrs = []
    append_attrs = []
    for pair in attr_list:
        match = ATTRIBUTE_RE.match(pair)
        if not match:
            raise TemplateSyntaxError(error_msg + ": %s" % pair)
        dct = match.groupdict()
        attr, sign, value = (
            dct["attr"],
            dct["sign"],
            parser.compile_filter(dct["value"]),
        )
        if sign == "=":
            set_attrs.append((attr, value))
        else:
            append_attrs.append((attr, value))

    return FieldAttributeNode(form_field, set_attrs, append_attrs)


class FieldAttributeNode(Node):
    def __init__(self, field, set_attrs, append_attrs):
        self.field = field
        self.set_attrs = set_attrs
        self.append_attrs = append_attrs

    def render(self, context):
        bounded_field = self.field.resolve(context)
        field = getattr(bounded_field, "field", None)
        if getattr(bounded_field, "errors", None) and "WIDGET_ERROR_CLASS" in context:
            bounded_field = append_attr(
                bounded_field, "class:%s" % context["WIDGET_ERROR_CLASS"]
            )
        if field and field.required and "WIDGET_REQUIRED_CLASS" in context:
            bounded_field = append_attr(
                bounded_field, "class:%s" % context["WIDGET_REQUIRED_CLASS"]
            )
        for k, v in self.set_attrs:
            if k == "type":
                bounded_field.field.widget.input_type = v.resolve(context)
            else:
                bounded_field = set_attr(
                    bounded_field, "%s:%s" % (k, v.resolve(context))
                )
        for k, v in self.append_attrs:
            bounded_field = append_attr(
                bounded_field, "%s:%s" % (k, v.resolve(context))
            )
        return str(bounded_field)


# ======================== remove_attr tag ==============================


@register.filter("remove_attr")
@silence_without_field
def remove_attr(field, attr):
    if attr in field.field.widget.attrs:
        del field.field.widget.attrs[attr]
    return field


@register.filter(name='get_dic_item')
def get_dic_item(dictionary, key):
    return dictionary.get(key)


@register.filter(name='get_attr')
def get_attr(value, arg):
    return getattr(value, arg)


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter(name='contains')
def has_group(path, search_string):
    return path.__contains__(search_string)


@register.simple_tag()
def setvar(val=None):
  return val


@register.simple_tag()
def math(operand1, operator, operand2):
    add = ['add', 'addition', 'plus']
    sub = ['sub', 'subtraction', 'minus']
    mul = ['mul', 'multiplication', 'multiply']
    div = ['div', 'division', 'divide']
    mod = ['mod', 'rem', 'remainder', 'modulus']
    pow = ['pow', 'power', 'raiseto', 'powerof', 'exponent', 'exponentiation']
    log = ['log', 'logarithm']
    if operator in add:
        return operand1 + operand2
    elif operator in sub:
        return operand1 - operand2
    elif operator in mul:
        return operand1 * operand2
    elif operator in div:
        return operand1 / operand2
    elif operator in mod:
        return operand1 % operand2
    elif operator in pow:
        return operand1 ** operand2
    elif operator in log:
        return math.log(operand1, operand2)
    else:
        raise ArithmeticError(f'Couldn\'t find the operator {operator} in math function')


@register.filter(name='add')
def add(operand1, operand2):
    return math(operand1, "add", operand2)


@register.filter(name='sub')
def sub(operand1, operand2):
    return math(operand1, "sub", operand2)


@register.filter(name='mul')
def mul(operand1, operand2):
    return math(operand1, "mul", operand2)


@register.filter(name='div')
def div(operand1, operand2):
    return math(operand1, "div", operand2)


@register.filter(name='mod')
def mod(operand1, operand2):
    return math(operand1, "mod", operand2)


@register.filter(name='pow')
def pow(operand1, operand2):
    return math(operand1, "pow", operand2)


@register.filter(name='log')
def log(operand1, operand2):
    return math(operand1, "log", operand2)