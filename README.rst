Groselha Page Template
========================

Groselha Page Templates are an HTML/XML generation tool for python end javascript.
This appendix is a reference to Groselha Page Templates standards:
It also describes some Grosa-specific behaviors that are not part of the standards.
This page template has been inspired in zpt http://docs.zope.org/zope2/zope2book/AppendixC.html.

Grosa Overview
------------

The Groselha Page Templates (Grosa) standard is an 
attribute language used to create dynamic templates. 
It allows elements of a document to be replaced, repeated, or omitted.

A  statement has a name (the attribute name) and a body (the attribute value).
For example, an content statement might look like: content="name"


Grosa Statements
--------------

These are the statements:

    * attr:* - dynamically change element attributes.
    * condition - test conditions.
    * content - replace the content of an element.
    * repeat - repeat an element.
    * replace - replace the content of an element and remove the 
      element leaving the content.


Order of Operations
-------------------

When there is only one statement per element, the order in which they 
are executed is simple. Starting with the root element, each element’s 
statements are executed, then each of its child elements 
is visited, in order, to do the same.
Any combination of statements may appear on the same elements, 
except that the content and replace statements may not appear together.
Due to the fact that JPG sees statements as XML attributes, even in HTML documents, 
it cannot use the order in which statements are written in the tag 
to determine the order in which they are executed. 
When an element has multiple statements, they are executed in this order:
repeat, condition, content or replace, attrs.

attr:attribute: Replace element attributes
==========================================

The attr:attribute statement replaces the value of an attribute (or creates an attribute) 
with a dynamic value. You can qualify an attribute name with a namespace prefix, 
for example::
    <img attr:src="photo.src" />


If the expression associated with an attribute assignment evaluates to nothing, 
then that attribute is deleted from the statement element.
If the expression evaluates to default, then that attribute is left unchanged. 
Each attribute assignment is independent, so attr:attribute may be assigned in the same 
statement in which some attributes are deleted and others are left alone.

If you use attrs on an element with an active replace command, 
the attrs statement is ignored.

Examples
--------

Replacing a link::

    <a href="/sample/link.html" attr:href="materia.absolute_url">

Replacing two attrs::

    <textarea rows="80" cols="20" attr:rows="element.rows" attr:cols="element.cols">



content: Replace the content of an element
==========================================

Rather than replacing an entire element, you can insert 
text or structure in place of its children with the content statement. 
The statement argument is exactly like that of replace, and 
is interpreted in the same fashion. If the expression evaluates to nothing, 
the statement element is left childless. If the expression evaluates to default, 
then the element’s contents are unchanged.

The default replacement behavior is text, which replaces angle-brackets and 
ampersands with their HTML entity equivalents.

TODO: The structure keyword passes the replacement text through unchanged, 
allowing HTML/XML markup to be inserted. This can break your page if the 
text contains unanticipated markup (e.g.. text submitted via a web form), 
which is the reason that it is not the default.

Examples
--------

Inserting the user name::

    <p content="user.getUserName">Fred Farkas</p>

Inserting HTML/XML::

    <p content="structure context.getStory">
        marked <b>up</b> content goes here.
    </p>


replace: Replace an element
===========================

The replace statement replaces an element with dynamic content. 
It replaces the statement element with either text or a structure (unescaped markup).
The body of the statement is an expression with an optional type prefix.
The value of the expression is converted into an escaped string if you prefix 
the expression with text or omit the prefix, and is inserted unchanged 
if you prefix it with structure. Escaping consists of converting 
“&amp;” to “&amp;amp;”, “&lt;” to “&amp;lt;”, and “&gt;” to “&amp;gt;”.

If the value is nothing, then the element is simply removed. 
If the value is default, then the element is left unchanged.

Examples
--------

The two ways to insert the title of a template::

    <span replace="template.title">Title</span>

Inserting HTML/XML::

TODO:    <div replace="structure table" />

Inserting nothing::

    <div replace="nothing">
      This element is a comment.
    </div>


repeat: Repeat an element
=========================

The repeat statement replicates a sub-tree of your document once for 
each item in a sequence. The expression should evaluate to a sequence. 
If the sequence is empty, then the statement element is deleted, 
otherwise it is repeated for each value in the sequence. 
If the expression is default, then the element is left unchanged, 
and no new variables are defined.

The variable_name is used to define a local variable and a repeat variable. 
For each repetition, the local variable is set to the current sequence element, 
and the repeat variable is set to an iteration object.

Repeat Variables
----------------

You use repeat variables to access information about the current repetition 
(such as the repeat index). The repeat variable has the same name as the local variable, 
but is only accessible through the built-in variable named repeat.

The following information is available from the repeat variable:
----------------------------------------------------------------

    * index - repetition number, starting from zero.
    * number - repetition number, starting from one.
    * even - true for even-indexed repetitions (0, 2, 4, ...).
    * odd - true for odd-indexed repetitions (1, 3, 5, ...).
    * start - true for the starting repetition (index 0).
    * end - true for the ending, or final, repetition.
    * length - length of the sequence, which will be the total number of repetitions.


Examples
--------
Iterating over a sequence of strings::

    <p repeat="txt messages">
      <span replace="txt" />
    </p>

Inserting a sequence of table rows, and using the repeat variable to number the rows::

    <table>
      <tr repeat="item context.cart">
        <td content="item.number">1</td>
        <td content="item.description">Widget</td>
        <td content="item.price">$1.50</td>
      </tr>
    </table>


condition: Conditionally insert or remove an element
====================================================

The condition statement includes the statement element in the template 
only if the condition is met, and omits it otherwise. 
If its expression evaluates to a true value, 
then normal processing of the element continues, 
otherwise the statement element is immediately removed from the template. 
For these purposes, the value nothing is false, 
and default has the same effect as returning a true value.

Note::
    Groselha considers missing variables, null, zero, and empty strings false;
    all other values are true.


Examples
--------

Test a variable before inserting it (the first example tests for existence and truth, 
while the second only tests for existence)::

    <p condition="message" content="message">message goes here</p>

Test for alternate conditions::

    <div repeat="number range">
      <p condition="repeat.even">Even</p>
      <p condition="repeat.odd">Odd</p>
    </div>
                
Built-in Functions and variables
================================

Groselha expressions have the same built-ins as Javascrit-based Scripts with a few additions.

These standard Groselha built-ins are available:

    * window        - The window object represents an open window in a browser.
    * document      -
    * navigator     - The navigator object contains information about the browser.
    * screen        - The screen object contains information about the visitor's screen.
    * history       - The history object contains the URLs visited by the user (within a browser window).
    * location      - The location object contains information about the current URL.
    * undefined     - Indicates that a variable has not been assigned a value

TODO:Grosa String expressions
===========================

String expressions interpret the expression in attribute with '' or "" as text.
The string can contain variable substitutions of the form %(name),
where name is a variable name, and path is a path expression.
The escaped string value of the path expression is inserted into the string.
To prevent a % from being interpreted this way, it must be escaped as \%.


Examples
--------

Basic string formatting::

    <span replace="'%(this) and %(that)'">
      Spam and Eggs
    </span>

Using paths::

    <p content="'to %(request.form.total)'">
      to 12
    </p>

Including a % sign::

    <p content="'percent: %(percent)\%(test)'">
      percent: 42%(test)
    </p>


Grosa-specific Behaviors
======================

The behavior of Groselha Page Templates is almost completely described by the
statements specifications. Grosas do, however, have a few additional 
features that are not described in the standards.

#TODO: