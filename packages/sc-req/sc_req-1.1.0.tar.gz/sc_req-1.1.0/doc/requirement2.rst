
.. highlight:: rest

Examples (part 2)
=================

Basic Examples
--------------

Here you will find some basic requirements demonstrating references, backward or forward into the list of rst files.

.. req:req:: This is req 02-01
    :reqid: REQ-0201

    First requirements for local links (links in the same rst file)

Forward link to :req:req:`REQ-0203`.

.. req:req:: This is req 02-02
    :reqid: REQ-0202

    Second requirements for links in another rst file

Link in another rst file :req:req:`REQ-0102`

.. req:req:: This is req 02-03
    :reqid: REQ-0203

    Third requirements for local links (links in the same rst file)

Backward link to :req:req:`REQ-0201`.

.. req:req:: This is yet another example
    :reqid: REQ-0004

    This is a simple requirement to demonstrate references across multiple documents

See :req:req:`REQ-0002` and :req:req:`REQ-0004`

Req ``REQ-0002`` is referenced there: :req:ref:`REQ-0002`

Generating ID
-------------

.. req:req:: Generation 2

    This is a second test of ID generation

Table
=====

This chapter demonstrates the :rst:dir:`req:reqlist` directive.

This is a normal table:

.. list-table:: This is how a normal table looks
    :widths: 20 80
    :header-rows: 1
    :stub-columns: 1
    :width: 100%
    :align: left
    
    * 
      - A
      - B

    *
      - a
      - b

This is the list of all requirements defined in this document:

.. req:reqlist:: This is the list of all requirements (no filtering, no sorting)

This is still the list of all the requirements but with a customized list of columns.

.. req:reqlist:: This is a *list* produced using **all** options (no filtering, no sorting)
    :fields: reqid, title, priority, _parents
    :headers: ID, Title, Priority, Parents
    :widths: 20 70 10 20
    :width: 80%
    :align: right
    :header-rows: 0
    :stub-columns: 2

The same directive can be used to produce a plain list, with no table:

.. req:reqlist::
    :filter: title.find('second')>0

    {%for req in reqs%}{{req['reqid']}}, {%endfor%}

This directive accepts a content to better customize the rendering.

.. req:reqlist:: A custom output with the full content, sorted by reverse ID
    :sort: -reqid


    .. list-table:: {{caption}}
        :widths: 10 70 10 20

        * - ID
          - Description
          - Contract
          - Ref

    {%for req in reqs%}
        * - {{req['reqid']}}
          - {{req['title']}}

            {{req['content']|indent(8)}}

          - {{req['contract']|upper}}
          - :req:ref:`{{req['reqid']}}`
    {%endfor%}

.. warning::

    Do not forget to *indent* as needed values that can span multiple lines.
    
