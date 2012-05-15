Class = function(){};
Class.new = function(context) {
 var cls = function(){};
 cls.prototype = context || {};
 cls.new =  function(){
     var object = new cls;
     if (object.initialize)
         object.initialize.apply(object, arguments);
     return object;
 };
 return cls;
};

GrosaAjax = Class.new({

    initialize: function(template_link, param){
        this.observers = [];
        var that = this;
        that.template = null;
        that.contexts = [];
        $.get(template_link, param, function(template){
           that.template = $(template);
           that._renderCallbacks();
        }, "html");
    },
    render: function(context, callback){
        this.contexts.push({context: context, callback: callback});
        this._renderCallbacks();
    },
    jsonPusher: function(render_name, callback){
        GrosaAjax.prototype = {
            render_name: function(json){
                this.render(json, callback);
         }
        };
    },
    get: function(path, param, callback){
        var that = this;
        $.get(path, param, function(context){that._ajax_callback(JSON.parse(context), callback)});
    },
    post: function(path, param, callback){
        var that = this;
        $.post(path, param, function(context){that._ajax_callback(JSON.parse(context), callback)}, "html");
    },
    getJSON: function(path, param, callback){
        var that = this;
        var callback = callback?callback:param;
        var param = (callback===param)?undefined:param;
        $.getJSON(path, param, function(data){that._ajax_callback(data, callback)});
    },
    _ajax_callback: function(context, callback){
        this.contexts.push({context: context, callback: callback});
        this._renderCallbacks();
    },
    _renderCallbacks: function(){
        if (this.template){
            while (this.contexts.length != 0) {
                var context = this.contexts.pop(0);
                var html = this.template.grosaRender(context.context);
                context.callback(html);
                this.notifyObservers(html, context.context)
         }
     }
    },
    removeObserver: function(observer){
        this.observers.splice(this.observers.indexOf(observer), 1);
    },
	addObserver: function(callback){
        this.observers.push(callback);
    },
    notifyObservers: function(html, context){
        for (var i=0;i<this.observers.length;i++){
            if (this.observers[i].constructor === Function){  
                this.observers[i](html, context);
            }else{
                this.observers[i].update(html, context);
            }
        }
    }

    
    
})