(function( $ ){
    $.grosa = {};
    $.grosa.filters = {
        toHtml:function(text){
            return $('<div>'+text+'</div>').contents();
        }    
    };
    $.grosa.extendFilter = function(extensions){
        $.extend($.grosa.filters, extensions);
    };
    $.grosa.templateTags = {};
    $.grosa.extendTemplateTags = function(extensions){
        $.extend($.grosa.templateTags, extensions);
    };
    function get_variable_in_context(context, acessor_array){
            if (!context) return undefined;
            var current_acessor = acessor_array[0];
			var current_context;
			if (context.hasOwnProperty(current_acessor)){
				current_context = context[current_acessor];
			} 
			else if ($.grosa.filters.hasOwnProperty(current_acessor)){
				current_context = $.grosa.filters[current_acessor];
			}
			else if (window.hasOwnProperty(current_acessor)){
                current_context = window[current_acessor];
			}
            if (acessor_array.length > 1) {
                var current_acessor_array = acessor_array.splice(1, acessor_array.length);
                return get_variable_in_context(current_context, current_acessor_array);
            } else {
                return current_context;
            }
    }
    function getElement(acessor){
        if (!acessor) return undefined;
        if (acessor.slice(0, 7) == 'string:'){
            return stringTemplate(acessor.slice(7), this);
        }
        acessors = acessor.split('|');
        var result;
        for (var i=0;i<acessors.length;i++){
            acessor = acessors[i];
            var content = get_variable_in_context(this, acessor.split('.'));
            result = (content && $.isFunction(content))?content(result):content;
        }
        return result;
    }
    function stringTemplate(template, context){
        return template.replace(
                /{{([\.\w]+)}}/g,
                function(match, acessor){
                    return context.getElement(acessor);
                })
    }
    function renderCondition(context){
        var acessor = this.attr('condition');
        this.removeAttr('condition');
        if (acessor){
            var result = context.getElement(acessor);
            if( !result ) this.remove();
        }
    }
    function renderContent(context){
        var acessor = this.attr('content');
        this.removeAttr('content');
        if (acessor){
            var content = context.getElement(acessor);
        	typeof(content) == "object"?this.html(content):this.text(content);
        }
    }
    function renderReplace(context){
        var acessor = this.attr('replace');
        this.removeAttr('replace');
        if (acessor){
            var node = context.getElement(acessor);
            this.replaceWith(node);
        };
    }
    function renderRepeat(context){
        var acessor = this.attr('repeat');
        if (acessor){
            var $tag_base = this,
                repeat_definition = acessor.split(/\s+/),
                item_name = repeat_definition[0],
                acessor = repeat_definition[1];
            var elements = context.getElement(acessor) || [],
                index = 0 ,
                number = 1;
            $tag_base.removeAttr('repeat');
            $(elements).each(function(key, item){
                context.repeat = {
                    index: index,
                    number: number,
                    even: !!(index%2),
                    odd: !!(number%2),
                    start: ((index===0)?true:false),
                    end: ((number==elements.length)?true:false)
                };
                var $new_tag = $tag_base.clone();
                context[item_name]=item;
                var $new_element = $new_tag.grosaRender(context)
                $new_element.insertBefore($tag_base);
                index++;
                number++;
            });
            this.remove();
        };
    }
    function renderAttrs(context){
            var statements=[];
            for (var n=0; n<this[0].attributes.length; n++){
                if (this[0].attributes[n].nodeName.substr(0,5) == 'attr:'){
                    var statement = this[0].attributes[n].nodeName,
                        attr = statement.substr(5, statement.length);
                    statements.push(attr);
                }
            }
            for (var i=0; i<statements.length; i++){
				var statement = statements[i];
                try{
                    var acessor = this.attr('attr:'+statement);
                    this.removeAttr('attr:'+statement)
                    var value = new String(context.getElement(acessor));
                    this.attr(statement, value);
                }
                catch(error){
                    console.log("Error in fill atribute "+statement+" with "+value+". "+error.message);
                }
            }
    }
    function renderTemplateTags(context){
        for (var tagName in $.grosa.templateTags)
            if (this[0].tagName.toLowerCase()==tagName.toLowerCase()){
                var result = $.grosa.templateTags[tagName].call(context, this);
                this.replaceWith(result);
            };
    }
    $.fn.grosaRender = function(context) {
      context.getElement = getElement
      var html =  this.clone();
      html.renderInline(context);
      return html
    };
    $.fn.renderInline = function(context) {
        context.getElement = getElement;
        var acessor = this.attr('repeat');
        if (acessor){
            renderRepeat.call(this, context);
        }else{
            var contents = this.contents('*');
            for ( var i=0; i<contents.length; i++ )
                contents.eq(i).renderInline(context);
        }
        renderCondition.call(this, context);
        renderContent.call(this, context);
        renderReplace.call(this, context);
        renderAttrs.call(this, context);
        renderTemplateTags.call(this, context)
    };
})( jQuery );