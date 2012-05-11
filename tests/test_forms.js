$(document).ready(function(){

    test("should render templateTags fieldText", function() {
        var $html = $("<form><fieldText name='test' title='fill this field' /></form>").jptRender({});
        equal($html.html(), $('<form><div class="field" id="id_test"><label for="test">fill this field</label><input type="text" name="test" /></div></form>').html());
    });

    test("should render templateTags fieldSelect", function() {
        var template = $("<form><fieldSelect name='test' title='fill this field' options='tests' /></form>")
        var $html = template.jptRender({'tests':[['a','A'],['b','B']]});
        var html_esperado = $('<form><div class="field" id="id_test"><label for="test">fill this field</label><select name="test" ><option value="a">A</option><option value="b">B</option></select></div></form>')
        equal($html.html(), html_esperado.html());
    });

    test("fieldTextarea field defines a multi-line text input control.", function() {
        var template = $("<form><fieldTextarea name='test' title='fill this field' /></form>")
        var $html = template.jptRender({'test':'defaul of textarea'});
        var html_esperado = $('<form><div class="field" id="id_test"><label for="test">fill this field</label><textarea name="test">defaul of textarea</textarea></div></form>')
        equal($html.html(), html_esperado.html());
    });

})