(function(){
    $.jpt.extendFilter({});
    
    var templateFieldSelect = $('<div class="field" attr:id="field.uid" ><label for="test" content="field.title"></label><select attr:name="field.name" ><option repeat="option_label field.options" attr:value="option_label.0" content="option_label.1" >lavel option</option></select></div>')
    
    $.jpt.extendTemplateTags({
       fieldText: function($node){
                  return $('<div class="field" id="id_'+$node.attr('name')+'" ><label for="test">'+$node.attr('title')+'</label><input type="text" name="'+$node.attr('name')+'" /></div>')
       },
       fieldSelect: function($node){
           var context = {'field': {
                               'uid': 'id_'+$node.attr('name'),
                               'name': $node.attr('name'),
                               'title': $node.attr('title'),
                               'options': this.getElement($node.attr('options'))
                               }
                            }
           return templateFieldSelect.jptRender(context)
       },
       fieldTextarea: function($node){
          return $('<div class="field" id="id_'+$node.attr('name')+'" ><label for="test">'+$node.attr('title')+'</label><textarea name="'+$node.attr('name')+'">'+(this.getElement($node.attr('name'))||'')+'</textarea></div>')
       },
    })
})()