from groselha import Grosa

from BeautifulSoup import BeautifulSoup
from unittest2 import TestCase, main


class GrosaTestCase(TestCase):

    def template(self, template, context):
        grosa_template = Grosa(template)
        html = BeautifulSoup(grosa_template.render(context))
        class Equal:
            @staticmethod
            def equal(result):
                self.assertEqual(html.prettify(), BeautifulSoup(result).prettify())
        return Equal()

    def test_should_subtitute_attribute_of_context(self):
        self.template(u"<b content='tweet.title'>title</b>", {'tweet': {'title': 'example'}}).equal("<b>example</b>")
    
    def test_should_subtitute_content(self):
        self.template(u"<b content='title'>Title</b>", {'title': 'example'}).equal("<b>example</b>")
    
    def test_not_filtered_toHtml_should_render_html_scaped(self):
        self.template(u"<div><p content='text_html' /></div>", {"text_html": "<b>text</b>"}).equal("<div><p>&lt;b&gt;text&lt;/b&gt;</p></div>")
    
    def test_filter_toHtml_should_render_no_scaped_text(self):
        self.template(u"<div><p content='text_html|toHtml'>teste</p></div>", {"text_html": "<b>texto com &aacute;</b>"}).equal("<div><p><b>texto com &aacute;</b></p></div>")
    
    def test_should_remove_element_if_var_not_in_context(self):
        self.template(u"<div><img condition='image' /></div>", {}).equal("<div></div>")
    
    def test_should_remove_condition_statement_if_var_in_context(self):
        self.template(u"<div><img condition='image' /></div>", {'image': 'test.png'}).equal("<div><img /></div>")
  
    def test_should_replace_the_tag_with_the_text_equivalent_to_the_value_in_the_dictionary(self):
        self.template(u"<div><a>Titulo:<span replace='title'>title</span></a></div>", {'title': 'example'}).equal("<div><a>Titulo:example</a></div>")
        self.template(u"<div><a><span replace='title'>title</span>:Titulo</a></div>", {'title': 'example'}).equal("<div><a>example:Titulo</a></div>")
  
    def test_should_repeat_this_tag_for_each_item_in_my_list_of_object_values(self):
        context = {
            'tweets': [
                {'text': 'New project new grosa'},
                {'text': 'new grosa is cool'}
            ]
        }
        self.template(u"<ul><li repeat='tweet tweets' ><a content='tweet.text'>test</a></li></ul>", context
                        ).equal("<ul><li><a>New project new grosa</a></li><li><a>new grosa is cool</a></li></ul>")
  
    def test_should_not_render_the_tag_if_repeating_in_an_empty_list(self):
        context = {
            'tweets': []
        };
        self.template(u"<ul><li repeat='tweet tweets' ><a content='tweet.text'>test</a></li></ul>", context
                        ).equal("<ul></ul>")
  
    def test_repeat_should_keep_ordering(self):
        context = {"items": [1, 2, 3]}
        self.template(u"<ul><li repeat='item items' content='item'></li></ul>", context).equal(
                      "<ul><li>1</li><li>2</li><li>3</li></ul>")
    def test_repeat_should_consider_variables_to_acess_information_about_the_current_repetition(self):
        context = {"names": ['Gustavo','Zacaster', 'Hugo']}
        template = self.template(u"""
    <table>
        <tr>
            <th>start</th>
            <th>end</th>
            <th>odd</th>
            <th>even</th>
            <th>index</th>
            <th>number</th>
            <th>Name</th>
        </tr>
        <tr repeat='name names'>
            <td content='repeat.start'>true</td>
            <td content='repeat.end'>true</td>
            <td content='repeat.odd'>true</td>
            <td content='repeat.even'>true</td>
            <td content='repeat.index'>0</td>
            <td content='repeat.number'>1</td>
            <td content='name'>Gustavo</td>
        </tr>
    </table>
        """, context)
        template.equal("""
   <table> 
     <tr>  <th>   start  </th>  <th>   end    </th>  <th>   odd   </th>  <th>   even   </th>  <th> index  </th>  <th>   number  </th>  <th>   Name  </th> </tr>
     <tr>  <td>   True   </td>  <td>   False  </td>  <td>   True  </td>  <td>   False  </td>  <td>    0   </td>  <td>      1    </td>  <td>   Gustavo  </td> </tr>
     <tr>  <td>   False  </td>  <td>   False  </td>  <td>   False </td>  <td>   True   </td>  <td>    1   </td>  <td>      2    </td>  <td>   Zacaster  </td> </tr>
     <tr>  <td>   False  </td>  <td>   True   </td>  <td>   True  </td>  <td>   False  </td>  <td>    2   </td>  <td>      3    </td>  <td>   Hugo  </td> </tr>
   </table>
  """)
  
    def test_The_condition_statement_should_remove_element_if_a_function_in_context_return_false(self):
        def test():
            return False
        
        context = {"test": test}
        
        self.template(u"<div><img condition='test'/></div>", context).equal("<div></div>")
  
    def test_The_condition_statement_not_should_remove_element_if_a_function_in_context_return_false(self):
        def test():
            return True
    
        context = {"test": test}
        
        self.template(u"<div><img condition='test'/></div>", context).equal("<div><img /></div>")
    
    def test_The_content_statement_should_subtitute_content_of_tag_with_returned_of_function(self):
        def title():
            return 'grosa is cool'
    
        context = {"title": title}
        
        self.template(u"<head><title content='title'/></head>", context).equal("<head><title>grosa is cool</title></head>")
    
    def test_The_replace_statement_should_subtitute_tag_with_returned_of_function(self):
        def title():
            return 'grosa is cool'
    
        context = {"title": title}
    
        self.template(u"<div>title:<span replace='title'>title</span></div>", context).equal("<div>title:grosa is cool</div>")
  
    def test_should_format_string(self):
        template = self.template(u"<h1 content='string:hello {{name}}'></h1>", {'name':'Gustavo Rezende'})
        template.equal("<h1>hello Gustavo Rezende</h1>")
  
    def test_must_format_a_string_with_multiple_contexts(self):
        template = self.template(u"<h1 content='string:hello {{user.alias}}, {{user.name}}'></h1>", {'user':{'alias':'groselha','name':'Gustavo Rezende'}})
        template.equal("<h1>hello groselha, Gustavo Rezende</h1>")
  
    def test_The_value_of_src_attribute_should_be_replace_with_value_of_context(self):
        context =  {'photo': {'src':'image.png'}}
        self.template(u"<div>image:<img attr:src='photo.src' src='' /></div>", context).equal("<div>image:<img src='image.png' /></div>")
  
    def test_The_value_of_attributes_should_be_replace_with_values_of_context(self):
        context =  {
            'photo': 'image.png',
            'text': 'alternative text'
        }
        self.template(u"<div>image:<img  attr:alt='text' attr:src='photo' /></div>", context).equal("<div>image:<img alt='alternative text' src='image.png' /></div>")
    
    def test_The_value_of_attributes_should_be_replaced_with_values_of_context_with_function_return(self):
        def photo():
            return 'image.png'
        context = {"photo": photo}
        self.template(u"<div>image:<img attr:src='photo' /></div>", context).equal("<div>image:<img src='image.png' /></div>")
    
    def test_the_condition_should_verify_values_of_context_with_function_returned(self):
        def photo():
            return 'image.png'
        context = {"photo": photo}
        self.template(u"<div>image:<img condition='photo' attr:src='photo' src='' /></div>", context).equal("<div>image:<img src='image.png' /></div>")
    
    def test_element_with_condition_should_not_render_if_function_in_context_returns_falsy(self):
        def photo():pass
        context = {"photo": photo}
        self.template(u"<div>image:<img condition='photo' attr:src='photo' src='' /></div>", context).equal("<div>image:</div>")

    def test_should_replace_multiples_(self):
        self.template(u"""
            <p>
            	Exibindo 
            	<span class="inicio" content="inicio"> </span>
            	a <span class="fim" content="fim"> </span>
            	de <span class="total" content="total"></span>
            	resultados.
            </p>""", {"inicio":1, "fim":10, "total":100}).equal("""
            <p>
            	Exibindo 
            	<span class="inicio">1</span> 
            	a <span class="fim">10</span>  
            	de <span class="total">100</span> 
            	resultados.
            </p>""")

    # def test_should_render_templateTags(self):
    #     @Grosa.extendTemplateTags
    #     def hello(node):
    #         return "hello "+ node["name"]
    #     self.template(u"<h1><hello name='Gustavo Rezende'>guy</hello></h1>").equal("<h1>hello Gustavo Rezende</h1>")

if __name__ == '__main__':
    main()
