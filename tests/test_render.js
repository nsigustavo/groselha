$(document).ready(function(){

    test("filter toHtml with &aacute;", function() {
        var $html = $("<div><p content='text_html|toHtml' /></div>").jptRender({"text_html": "<b>texto com &aacute;</b>"});
        equal($html.find('b').text(), "texto com á", '');
    });

    test("filter toHtml", function() {
        var $html = $("<div><p content='text_html|toHtml' /></div>").jptRender({"text_html": "<b>texto</b>"});
        equal($html.find('b').length, 1, '');
    });

    test("should remove element if var not in context", function() {
        var $html = $("<div><img condition='image' /></div>").jptRender({});
        equal($html.find('img').length, 0, 'img not removed');
    });

    test("should remove condition statement if var in context", function() {
        var $html = $("<img condition='image' />").jptRender({
            'image': 'test.png'
        });
        ok(!$html.attr('condition'), 'condition not statement removed');
    });;

    test("should substitute content", function() {
        var $html = $("<a content='title'>title</a>").jptRender({
            'title': 'example'
        });
        equal($html.text(), 'example', 'did not substitute tag content');
    });

    test("should substitute attribute of context", function() {
        var $html = $("<a content='tweet.title'>title</a>").jptRender({
            'tweet': {
                'title': 'example'
            }
        });
        equal($html.text(), 'example', 'not subistitute content of tag');
    });

    test("should replace the tag with the text equivalent to the value in the dictionary", function() {
        var $html = $("<div><a>Titulo:<span replace='title'>title</span></a></div>").jptRender({
            'title': 'example'
        });
        equal($html.find('a').text(), 'Titulo:example', 'did not replace tag span');
    });

    test("should repeat this tag for each item in my list of object values", function() {
        var context = {
            'tweets': [{
                'text': 'New project new Jpt'
            },
            {
                'text': 'new Jpt is cool'
            }]
        };
        var $html = $("<ul><li repeat='tweet tweets' ><a content='tweet.text'>test</a></li></ul>").jptRender(context);
        equal($html.find('li').length, 2, 'did not repeat tag li');
    });

    test("should not render the tag if repeating in an empty list", function() {
        var context = {
            'tweets': []
        };
        var $html = $("<ul><li repeat='tweet tweets' ><a content='tweet.text'>test</a></li></ul>").jptRender(context);
        equal($html.find('li').length, 0, 'tag li exists');
    });

    test("should repeat this tag for each item in my list of object values and apply new context", function() {
        var context = {
            'tweets': [{
                'text': 'New project new Jpt'
            },
            {
                'text': 'new Jpt is cool'
            }]
        };
        var $html = $("<ul><li repeat='tweet tweets' ><a content='tweet.text'>test</a></li></ul>").jptRender(context);
        first_link = $($html.find('a')[0])
        equal(first_link.text(), 'New project new Jpt', 'Not apply new context');
    });

    test("The condition statement should remove element if a function in context return false", function() {
        var context = {
            test: function() {
                return false;
            }
        };
        var $html = $("<div><img condition='test'/></div>").jptRender(context);
        equal($html.find('img').length, 0, 'img not removed');
    });

    test("The condition statement not should remove element if a function in context return true", function() {
        var context = {
            test: function() {
                return true;
            }
        }
        var $html = $("<div><img condition='test'/></div>").jptRender(context);
        equal($html.find('img').length, 1, 'img removed');
    });

    test("The content statement should subtitute content of tag with returned of function", function() {
        var context = {
            title: function() {
                return 'Jpt is cool';
            }
        };
        var $html = $("<div><title content='title'>title</title></div>").jptRender(context);
        equal($html.find('title').text(), 'Jpt is cool', 'The statement did not replace the text');
    });

    test("The replace statement should subtitute tag with returned of function", function() {
        var context = {
            title: function() {
                return 'Jpt is cool';
            }
        };
        var $html = $("<div>title:<span replace='title'>title</span></div>").jptRender(context);
        equal($html.text(), 'title:Jpt is cool', 'The statement did not replace the text');
    });


    test("The value of src attribute should be replace with value of context", function() {
        var $html = $("<div>image:<img attr:src='photo.src' src='' /></div>").jptRender({
            'photo': {'src':'image.png'}
        });
        equal($html.find('img').attr('src'), 'image.png', 'The attribute src not replaced for image.png');
    });

    test("The value of attributes should be replace with values of context", function() {
        var $html = $("<div>image:<img  attr:alt='text' attr:src='photo' /></div>").jptRender({
            'photo': 'image.png',
            'text': 'alternative text'
        });
        equal($html.find('img').attr('alt'), 'alternative text', 'The attribute alt not replaced for alternative text');
        equal($html.find('img').attr('src'), 'image.png', 'The attribute src not replaced for image.png');
    });

    test("The value of attributes should be replaced with values of context with function return", function() {
        var $html = $("<div>image:<img attr:src='photo' /></div>").jptRender({
            photo: function() {
                return 'image.png'
            }
        });
        equal($html.find('img').attr('src'), 'image.png', 'The attribute src not replaced for image.png');
    });

    test("The condition should  verify values of context with function return", function() {
        var $html = $("<div>image:<img condition='photo' attr:src='photo' src='' /></div>").jptRender({
            photo: function() {
                return 'image.png'
            }
        });
        equal($html.find('img').attr('src'), 'image.png', 'The attribute src not replaced for image.png');
    });

    test("element with `condition` should not render if function in context returns falsy", function() {
        context = {
            photo: function() {
                return undefined
            }
        }
        var $html = $("<div>image:<img condition='photo' attr:src='photo' src='' /></div>").jptRender(context);
        equal($html.find('img').length, 0);
    });

    test("repeat should keep ordering", function() {
        var $html = $("<ul><li repeat='item items' content='item'></li></ul>").jptRender({
            items: [1, 2, 3]
        });
        equal($html.find('li').eq(0).text(), '1');
        equal($html.find('li').eq(1).text(), '2');
        equal($html.find('li').eq(2).text(), '3');
    });

    test("repeat should consider variables to access information about the current repetition", function() {
        var $html = $("<table><tr><th>start</th><th>end</th><th>odd</th><th>even</th><th>index</th><th>number</th><th>Name</th></tr><tr repeat='name names'><td content='repeat.start'>true</td><td content='repeat.end'>true</td><td content='repeat.odd'>true</td><td content='repeat.even'>true</td><td content='repeat.index'>0</td><td content='repeat.number'>1</td><td content='name'>Gustavo</td></tr></table>").jptRender({
            names: ['Gustavo','Zacaster', 'Hugo']
        });
        equal($html.html(),'<tbody><tr><th>start</th><th>end</th><th>odd</th><th>even</th><th>index</th><th>number</th><th>Name</th></tr><tr><td>true</td><td>false</td><td>true</td><td>false</td><td>0</td><td>1</td><td>Gustavo</td></tr><tr><td>false</td><td>false</td><td>false</td><td>true</td><td>1</td><td>2</td><td>Zacaster</td></tr><tr><td>false</td><td>true</td><td>true</td><td>false</td><td>2</td><td>3</td><td>Hugo</td></tr></tbody>');
    });

    test("should render templateTags", function() {
        $.jpt.extendTemplateTags({hello: function($node){
                                            return "hello "+$node.attr('name')
                                        }
                                })
        var $html = $("<h1><hello name='Gustavo Rezende'>guy</hello></h1>").jptRender({'a':3});
        equal($html.text(), 'hello Gustavo Rezende');
    });
    test("deve formartar uma string", function() {
        var $html = $("<h1 content='string:hello {{name}}'></h1>").jptRender({'name':'Gustavo Rezende'});
        equal($html.text(), 'hello Gustavo Rezende');
    });

    test("deve formartar uma string com multiplos contextos", function() {
        var context = {'user':{'alias':'groselha','name':'Gustavo Rezende'}};
        var $html = $("<h1 content='string:hello {{user.alias}}, {{user.name}}'></h1>").jptRender(context);
        equal($html.text(), 'hello groselha, Gustavo Rezende');
    });


});
