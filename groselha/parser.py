# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup, Tag, NavigableString
import re
from copy import deepcopy, copy


class Grosa(object):
    """Groselha Page Template"""

    filters = {
        'toHtml': lambda html: BeautifulSoup(html)
    }
    
    @classmethod
    def push_filter(cls, filter):
        cls.filters[filter.func_name] = filter

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
        self.render_repeat(tag_template, context)
        self.render_condition(tag_template, context)
        self.render_content(tag_template, context)
        self.render_replace(tag_template, context)
        self.render_attributes(tag_template, context)
        if tag_template.childGenerator():
            self._render_template(tag_template.childGenerator(), context)

    def render_repeat(self, tag_template, context):
        if tag_template.has_key('repeat'):
            regex_repeat = re.compile("(?P<item_name>.*)\s+(?P<acessor>.*)")
            item_name, acessor = regex_repeat.search(tag_template['repeat']).groups()
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
            del tag_template

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
                tag_template.string = unicode(value, errors='replace')
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

#     $.fn.renderInline = function(context) {
#         context.getElement = getElement;
#         var acessor = this.attr('repeat');
#         if (acessor){
#             render_repeat.call(this, context);
#         }else{
#             var contents = this.contents('*');
#             for ( var i=0; i<contents.length; i++ )
#                 contents.eq(i).renderInline(context);
#         }
#         render_condition.call(this, context);
#         render_content.call(this, context);
#         render_replace.call(this, context);
#         renderAttrs.call(this, context);
#         renderTemplateTags.call(this, context)



# (function( $ ){
#     $.grosa = {};
#     $.grosa.filters = {
#         toHtml:function(text){
#             return $('<div>'+text+'</div>').contents();
#         }    
#     };
#     $.grosa.extendFilter = function(extensions){
#         $.extend($.grosa.filters, extensions);
#     };
#     $.grosa.templateTags = {};
#     $.grosa.extendTemplateTags = function(extensions){
#         $.extend($.grosa.templateTags, extensions);
#     };
#     function get_variable_in_context(context, acessor_array){
#             if (!context) return undefined;
#             var current_acessor = acessor_array[0];
#           var current_context;
#           if (context.hasOwnProperty(current_acessor)){
#               current_context = context[current_acessor];
#           } 
#           else if ($.grosa.filters.hasOwnProperty(current_acessor)){
#               current_context = $.grosa.filters[current_acessor];
#           }
#           else if (window.hasOwnProperty(current_acessor)){
#                 current_context = window[current_acessor];
#           }
#             if (acessor_array.length > 1) {
#                 var current_acessor_array = acessor_array.splice(1, acessor_array.length);
#                 return get_variable_in_context(current_context, current_acessor_array);
#             } else {
#                 return current_context;
#             }
#     }
#     function getElement(acessor){
#         if (!acessor) return undefined;
#         if (acessor.slice(0, 7) == 'string:'){
#             return stringTemplate(acessor.slice(7), this);
#         }
#         acessors = acessor.split('|');
#         var result;
#         for (var i=0;i<acessors.length;i++){
#             acessor = acessors[i];
#             var content = get_variable_in_context(this, acessor.split('.'));
#             result = (content && $.isFunction(content))?content(result):content;
#         }
#         return result;
#     }
#     function stringTemplate(template, context){
#         return template.replace(
#                 /{{([\.\w]+)}}/g,
#                 function(match, acessor){
#                     return context.getElement(acessor);
#                 })
#     }
#     function render_condition(context){
#         var acessor = this.attr('condition');
#         this.removeAttr('condition');
#         if (acessor){
#             var result = context.getElement(acessor);
#             if( !result ) this.remove();
#         }
#     }
#     function render_content(context){
#         var acessor = this.attr('content');
#         this.removeAttr('content');
#         if (acessor){
#             var content = context.getElement(acessor);
#           typeof(content) == "object"?this.html(content):this.text(content);
#         }
#     }
#     function render_replace(context){
#         var acessor = this.attr('replace');
#         this.removeAttr('replace');
#         if (acessor){
#             var node = context.getElement(acessor);
#             this.replaceWith(node);
#         };
#     }
#     function render_repeat(context){
#         var acessor = this.attr('repeat');
#         if (acessor){
#             var $tag_base = this,
#                 repeat_definition = acessor.split(/\s+/),
#                 item_name = repeat_definition[0],
#                 acessor = repeat_definition[1];
#             var elements = context.getElement(acessor) || [],
#                 index = 0 ,
#                 number = 1;
#             $tag_base.removeAttr('repeat');
#             $(elements).each(function(key, item){
#                 context.repeat = {
#                     index: index,
#                     number: number,
#                     even: !!(index%2),
#                     odd: !!(number%2),
#                     start: ((index===0)?true:false),
#                     end: ((number==elements.length)?true:false)
#                 };
#                 var $new_tag = $tag_base.clone();
#                 context[item_name]=item;
#                 var $new_element = $new_tag.grosaRender(context)
#                 $new_element.insertBefore($tag_base);
#                 index++;
#                 number++;
#             });
#             this.remove();
#         };
#     }
#     function renderAttrs(context){
#             var statements=[];
#             for (var n=0; n<this[0].attributes.length; n++){
#                 if (this[0].attributes[n].nodeName.substr(0,5) == 'attr:'){
#                     var statement = this[0].attributes[n].nodeName,
#                         attr = statement.substr(5, statement.length);
#                     statements.push(attr);
#                 }
#             }
#             for (var i=0; i<statements.length; i++){
#               var statement = statements[i];
#                 try{
#                     var acessor = this.attr('attr:'+statement);
#                     this.removeAttr('attr:'+statement)
#                     var value = new String(context.getElement(acessor));
#                     this.attr(statement, value);
#                 }
#                 catch(error){
#                     console.log("Error in fill atribute "+statement+" with "+value+". "+error.message);
#                 }
#             }
#     }
#     function renderTemplateTags(context){
#         for (var tagName in $.grosa.templateTags)
#             if (this[0].tagName.toLowerCase()==tagName.toLowerCase()){
#                 var result = $.grosa.templateTags[tagName].call(context, this);
#                 this.replaceWith(result);
#             };
#     }
#     $.fn.grosaRender = function(context) {
#       context.getElement = getElement
#       var html =  this.clone();
#       html.renderInline(context);
#       return html
#     };
#     $.fn.renderInline = function(context) {
#         context.getElement = getElement;
#         var acessor = this.attr('repeat');
#         if (acessor){
#             render_repeat.call(this, context);
#         }else{
#             var contents = this.contents('*');
#             for ( var i=0; i<contents.length; i++ )
#                 contents.eq(i).renderInline(context);
#         }
#         render_condition.call(this, context);
#         render_content.call(this, context);
#         render_replace.call(this, context);
#         renderAttrs.call(this, context);
#         renderTemplateTags.call(this, context)
#     };
# })( jQuery );