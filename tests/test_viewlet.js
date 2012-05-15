htmls = {
    '/url/template/test.html':'<span content="name">teste</span>'
}
$.esperado = {}
$.get = function(url, parameters, callback){
    $.esperado.url = url;
    $.esperado.parameters = parameters;
    callback(htmls[url])
}


$(function(){

    test("deve capturar a template", function() {
        GrosaAjax = GrosaAjax.new('/url/template/test.html');
        equal(GrosaAjax.template.html(), $('<span>teste</span>').html());
    });

    test("deve renderizar a template", function() {
        GrosaAjax = GrosaAjax.new('/url/template/test.html').render({'name':'Gustavo'}, function(html){
            $.esperado.html = html
        });
        equal($.esperado.html.html(), $('<span>Gustavo</span>').html());
    });

})