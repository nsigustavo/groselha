# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup, Tag, NavigableString
import re
from copy import deepcopy, copy


class Grosa(object):
    """Groselha Page Template"""
    regex_repeat = re.compile("(?P<item_name>.*)\s+(?P<acessor>.*)")
    filters = {
        'toHtml': lambda html: BeautifulSoup(html)
    }
    
    @classmethod
    def push_filter(cls, filter):
        cls.filters[filter.func_name] = filter
        return filter

    def __init__(self, template_path):
        f = open(template_path,'r')
        self.template = BeautifulSoup(f.read())

    def render(self, context):
        self._render_template(self.template.childGenerator(), context)
        return self.template.prettify()

    def _render_template(self, tags, context):
        for tag_template in tags:
            if type(tag_template) == Tag:
                self._render_template_tag(tag_template, context)

    def _render_template_tag(self, tag_template, context):
        if not self.render_repeat(tag_template, context):
            self.render_condition(tag_template, context)
            self.render_content(tag_template, context)
            self.render_replace(tag_template, context)
            self.render_attributes(tag_template, context)
            self._render_template(tag_template.childGenerator(), context)

    def render_repeat(self, tag_template, context):
        if tag_template.has_key('repeat'):
            item_name, acessor = self.regex_repeat.search(tag_template['repeat']).groups()
            elements = self.get_value(context, acessor)
            tag_parent = tag_template.parent
            position = tag_parent.index(tag_template)
            tag_template.extract()
            del tag_template['repeat']
            index = 0
            number = 1
            for item in elements:
                context['repeat'] = {
                    "index": index,
                    "number": number,
                    "even": bool(index % 2),
                    "odd": bool(number % 2),
                    "start": index==0,
                    "end": number==len(elements),
                }
                new_tag = deepcopy(tag_template)
                context[str(item_name)] = item
                index += 1
                number += 1
                tag_parent.insert(position+index, new_tag)
                self._render_template_tag(new_tag, context)
            return True
        return False

    def render_replace(self, tag_template, context):
        if tag_template.has_key('replace'):
            acessor = tag_template['replace']
            value = self.get_value(context, acessor)
            if isinstance(value, (str, unicode)):
                if type(tag_template.previousSibling) == NavigableString:
                    tag_template.previousSibling.replaceWith(NavigableString(unicode( tag_template.previousSibling) + value))
                    tag_template.extract()
                elif type(tag_template.nextSibling) == NavigableString:
                    tag_template.nextSibling.replaceWith(NavigableString(value + unicode( tag_template.nextSibling)))
                    tag_template.extract()
                else:
                    tag_template.replaceWith(NavigableString(value))
            else:
                tag_template.replaceWith(value)

    def render_condition(self, tag_template, context):
        if tag_template.has_key('condition'):
            acessor = tag_template['condition']
            value = self.get_value(context, acessor)
            if not value:
                tag_template.extract()
            else:
                del tag_template['condition']

    def render_content(self, tag_template, context):
        if tag_template.has_key('content'):
            acessor = tag_template['content']
            value = self.get_value(context, acessor)
            if not isinstance(value, Tag):
                tag_template.string = value
            else:
                for child in tag_template.childGenerator():
                    child.extract()
                if isinstance(value, Tag):
                    tag_template.append(value)
            del tag_template['content']

    def string_expressions(self, context, string_expressions):
        regex_stringtemplate = re.compile(r"{{([\.\w\|]+)}}")
        def get_value_string_expressions(acessor):
            return self.get_value(context, acessor.group()[2:-2])
        return regex_stringtemplate.sub(get_value_string_expressions, string_expressions)

    def get_value(self, context, acessor):
        if not acessor: return None
        if acessor.startswith('string:'):
            return self.string_expressions(context, acessor[7:])
        result = context
        attribute_path = str(acessor.split('|')[0])
        for attribute in attribute_path.split('.'):
            if hasattr(result, '__getitem__'):
                result = result.get(attribute, None)
            else:
                result = getattr(result, attribute, None)
            if callable(result):
                result = result()
        if result is context: return None
        return self.apply_filters(result, acessor.split('|')[1:])

    def apply_filters(self, result, filters):
        #import ipdb; ipdb.set_trace();
        for filter in [self.filters[filter_name] for filter_name in filters]:
            result = filter(result)
        return result

    def render_attributes(self, tag_template, context):
        attrs = copy(tag_template.attrs)
        for attr, acessor in attrs:
            if attr.startswith('attr:'):
                attribute_name = attr[5:]
                del tag_template[attr]
                value = self.get_value(context, acessor)
                tag_template[attribute_name] = value
