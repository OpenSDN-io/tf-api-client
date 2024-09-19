#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Generated Fri Sep 30 10:39:12 2011 by generateDS.py version 2.6b.
#

import sys
import re as re_

etree_ = None
Verbose_import_ = False
(   XMLParser_import_none, XMLParser_import_lxml,
    XMLParser_import_elementtree
    ) = list(range(3))
XMLParser_import_library = None
try:
    # lxml
    from lxml import etree as etree_
    XMLParser_import_library = XMLParser_import_lxml
    if Verbose_import_:
        print("running with lxml.etree")
except ImportError:
    try:
        # cElementTree from Python 2.5+
        import xml.etree.cElementTree as etree_
        XMLParser_import_library = XMLParser_import_elementtree
        if Verbose_import_:
            print("running with cElementTree on Python 2.5+")
    except ImportError:
        try:
            # ElementTree from Python 2.5+
            import xml.etree.ElementTree as etree_
            XMLParser_import_library = XMLParser_import_elementtree
            if Verbose_import_:
                print("running with ElementTree on Python 2.5+")
        except ImportError:
            try:
                # normal cElementTree install
                import cElementTree as etree_
                XMLParser_import_library = XMLParser_import_elementtree
                if Verbose_import_:
                    print("running with cElementTree")
            except ImportError:
                try:
                    # normal ElementTree install
                    import elementtree.ElementTree as etree_
                    XMLParser_import_library = XMLParser_import_elementtree
                    if Verbose_import_:
                        print("running with ElementTree")
                except ImportError:
                    raise ImportError("Failed to import ElementTree from any known place")

def parsexml_(*args, **kwargs):
    if (XMLParser_import_library == XMLParser_import_lxml and
        'parser' not in kwargs):
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        kwargs['parser'] = etree_.ETCompatXMLParser()
    doc = etree_.parse(*args, **kwargs)
    return doc

#
# User methods
#
# Calls to the methods in these classes are generated by generateDS.py.
# You can replace these methods by re-implementing the following class
#   in a module named generatedssuper.py.

try:
    from generatedssuper import GeneratedsSuper
except ImportError as exp:

    class GeneratedsSuper(object):
        def gds_format_string(self, input_data, input_name=''):
            return input_data
        def gds_validate_string(self, input_data, node, input_name=''):
            return input_data
        def gds_format_integer(self, input_data, input_name=''):
            return '%d' % input_data
        def gds_validate_integer(self, input_data, node, input_name=''):
            return input_data
        def gds_format_integer_list(self, input_data, input_name=''):
            return '%s' % input_data
        def gds_validate_integer_list(self, input_data, node, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    fvalue = float(value)
                except (TypeError, ValueError) as exp:
                    raise_parse_error(node, 'Requires sequence of integers')
            return input_data
        def gds_format_float(self, input_data, input_name=''):
            return '%f' % input_data
        def gds_validate_float(self, input_data, node, input_name=''):
            return input_data
        def gds_format_float_list(self, input_data, input_name=''):
            return '%s' % input_data
        def gds_validate_float_list(self, input_data, node, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    fvalue = float(value)
                except (TypeError, ValueError) as exp:
                    raise_parse_error(node, 'Requires sequence of floats')
            return input_data
        def gds_format_double(self, input_data, input_name=''):
            return '%e' % input_data
        def gds_validate_double(self, input_data, node, input_name=''):
            return input_data
        def gds_format_double_list(self, input_data, input_name=''):
            return '%s' % input_data
        def gds_validate_double_list(self, input_data, node, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    fvalue = float(value)
                except (TypeError, ValueError) as exp:
                    raise_parse_error(node, 'Requires sequence of doubles')
            return input_data
        def gds_format_boolean(self, input_data, input_name=''):
            return '%s' % input_data
        def gds_validate_boolean(self, input_data, node, input_name=''):
            return input_data
        def gds_format_boolean_list(self, input_data, input_name=''):
            return '%s' % input_data
        def gds_validate_boolean_list(self, input_data, node, input_name=''):
            values = input_data.split()
            for value in values:
                if value not in ('true', '1', 'false', '0', ):
                    raise_parse_error(node, 'Requires sequence of booleans ("true", "1", "false", "0")')
            return input_data
        def gds_str_lower(self, instring):
            return instring.lower()
        def get_path_(self, node):
            path_list = []
            self.get_path_list_(node, path_list)
            path_list.reverse()
            path = '/'.join(path_list)
            return path
        Tag_strip_pattern_ = re_.compile(r'\{.*\}')
        def get_path_list_(self, node, path_list):
            if node is None:
                return
            tag = GeneratedsSuper.Tag_strip_pattern_.sub('', node.tag)
            if tag:
                path_list.append(tag)
            self.get_path_list_(node.getparent(), path_list)
        def get_class_obj_(self, node, default_class=None):
            class_obj1 = default_class
            if 'xsi' in node.nsmap:
                classname = node.get('{%s}type' % node.nsmap['xsi'])
                if classname is not None:
                    names = classname.split(':')
                    if len(names) == 2:
                        classname = names[1]
                    class_obj2 = globals().get(classname)
                    if class_obj2 is not None:
                        class_obj1 = class_obj2
            return class_obj1


#
# If you have installed IPython you can uncomment and use the following.
# IPython is available from http://ipython.scipy.org/.
#

## from IPython.Shell import IPShellEmbed
## args = ''
## ipshell = IPShellEmbed(args,
##     banner = 'Dropping into IPython',
##     exit_msg = 'Leaving Interpreter, back to program.')

# Then use the following line where and when you want to drop into the
# IPython shell:
#    ipshell('<some message> -- Entering ipshell.\nHit Ctrl-D to exit')

#
# Globals
#

ExternalEncoding = 'ascii'
Tag_pattern_ = re_.compile(r'({.*})?(.*)')
String_cleanup_pat_ = re_.compile(r"[\n\r\s]+")
Namespace_extract_pat_ = re_.compile(r'{(.*)}(.*)')

#
# Support/utility functions.
#

def showIndent(outfile, level):
    for idx in range(level):
        outfile.write('    ')

def quote_xml(inStr):
    if not inStr:
        return ''
    s1 = (isinstance(inStr, str) and inStr or
          '%s' % inStr)
    s1 = s1.replace('&', '&amp;')
    s1 = s1.replace('<', '&lt;')
    s1 = s1.replace('>', '&gt;')
    return s1

def quote_attrib(inStr):
    s1 = (isinstance(inStr, str) and inStr or
          '%s' % inStr)
    s1 = s1.replace('&', '&amp;')
    s1 = s1.replace('<', '&lt;')
    s1 = s1.replace('>', '&gt;')
    if '"' in s1:
        if "'" in s1:
            s1 = '"%s"' % s1.replace('"', "&quot;")
        else:
            s1 = "'%s'" % s1
    else:
        s1 = '"%s"' % s1
    return s1

def quote_python(inStr):
    s1 = inStr
    if s1.find("'") == -1:
        if s1.find('\n') == -1:
            return "'%s'" % s1
        else:
            return "'''%s'''" % s1
    else:
        if s1.find('"') != -1:
            s1 = s1.replace('"', '\\"')
        if s1.find('\n') == -1:
            return '"%s"' % s1
        else:
            return '"""%s"""' % s1

def get_all_text_(node):
    if node.text is not None:
        text = node.text
    else:
        text = ''
    for child in node:
        if child.tail is not None:
            text += child.tail
    return text

def find_attr_value_(attr_name, node):
    attrs = node.attrib
    attr_parts = attr_name.split(':')
    value = None
    if len(attr_parts) == 1:
        value = attrs.get(attr_name)
    elif len(attr_parts) == 2:
        prefix, name = attr_parts
        namespace = node.nsmap.get(prefix)
        if namespace is not None:
            value = attrs.get('{%s}%s' % (namespace, name, ))
    return value


class GDSParseError(Exception):
    pass

def raise_parse_error(node, msg):
    if XMLParser_import_library == XMLParser_import_lxml:
        msg = '%s (element %s/line %d)' % (msg, node.tag, node.sourceline, )
    else:
        msg = '%s (element %s)' % (msg, node.tag, )
    raise GDSParseError(msg)


class MixedContainer(object):
    # Constants for category:
    CategoryNone = 0
    CategoryText = 1
    CategorySimple = 2
    CategoryComplex = 3
    # Constants for content_type:
    TypeNone = 0
    TypeText = 1
    TypeString = 2
    TypeInteger = 3
    TypeFloat = 4
    TypeDecimal = 5
    TypeDouble = 6
    TypeBoolean = 7
    def __init__(self, category, content_type, name, value):
        self.category = category
        self.content_type = content_type
        self.name = name
        self.value = value
    def getCategory(self):
        return self.category
    def getContenttype(self, content_type):
        return self.content_type
    def getValue(self):
        return self.value
    def getName(self):
        return self.name
    def export(self, outfile, level, name, namespace):
        if self.category == MixedContainer.CategoryText:
            # Prevent exporting empty content as empty lines.
            if self.value.strip(): 
                outfile.write(self.value)
        elif self.category == MixedContainer.CategorySimple:
            self.exportSimple(outfile, level, name)
        else:    # category == MixedContainer.CategoryComplex
            self.value.export(outfile, level, namespace,name)
    def exportSimple(self, outfile, level, name):
        if self.content_type == MixedContainer.TypeString:
            outfile.write('<%s>%s</%s>' % (self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeInteger or \
                self.content_type == MixedContainer.TypeBoolean:
            outfile.write('<%s>%d</%s>' % (self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeFloat or \
                self.content_type == MixedContainer.TypeDecimal:
            outfile.write('<%s>%f</%s>' % (self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeDouble:
            outfile.write('<%s>%g</%s>' % (self.name, self.value, self.name))
    def exportLiteral(self, outfile, level, name):
        if self.category == MixedContainer.CategoryText:
            showIndent(outfile, level)
            outfile.write('model_.MixedContainer(%d, %d, "%s", "%s"),\n' % \
                (self.category, self.content_type, self.name, self.value))
        elif self.category == MixedContainer.CategorySimple:
            showIndent(outfile, level)
            outfile.write('model_.MixedContainer(%d, %d, "%s", "%s"),\n' % \
                (self.category, self.content_type, self.name, self.value))
        else:    # category == MixedContainer.CategoryComplex
            showIndent(outfile, level)
            outfile.write('model_.MixedContainer(%d, %d, "%s",\n' % \
                (self.category, self.content_type, self.name,))
            self.value.exportLiteral(outfile, level + 1)
            showIndent(outfile, level)
            outfile.write(')\n')


class MemberSpec_(object):
    def __init__(self, name='', data_type='', container=0):
        self.name = name
        self.data_type = data_type
        self.container = container
    def set_name(self, name): self.name = name
    def get_name(self): return self.name
    def set_data_type(self, data_type): self.data_type = data_type
    def get_data_type_chain(self): return self.data_type
    def get_data_type(self):
        if isinstance(self.data_type, list):
            if len(self.data_type) > 0:
                return self.data_type[-1]
            else:
                return 'xs:string'
        else:
            return self.data_type
    def set_container(self, container): self.container = container
    def get_container(self): return self.container

def cast_(typ, value):
    if typ is None or value is None:
        return value
    return typ(value)

#
# Data representation classes.
#

class contactlistType(GeneratedsSuper):
    member_data_items_ = [
        MemberSpec_('locator', 'xs:string', 0),
        MemberSpec_('description', 'xs:string', 0),
        MemberSpec_('contact', 'contactType', 1),
        ]
    subclass = None
    superclass = None
    def __init__(self, locator=None, description=None, contact=None):
        self.locator = cast_(None, locator)
        self.description = description
        if contact is None:
            self.contact = []
        else:
            self.contact = contact
    def factory(*args_, **kwargs_):
        if contactlistType.subclass:
            return contactlistType.subclass(*args_, **kwargs_)
        else:
            return contactlistType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_description(self): return self.description
    def set_description(self, description): self.description = description
    def get_contact(self): return self.contact
    def set_contact(self, contact): self.contact = contact
    def add_contact(self, value): self.contact.append(value)
    def insert_contact(self, index, value): self.contact[index] = value
    def get_locator(self): return self.locator
    def set_locator(self, locator): self.locator = locator
    def export(self, outfile, level, namespace_='', name_='contactlistType', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = []
        self.exportAttributes(outfile, level, already_processed, namespace_, name_='contactlistType')
        if self.hasContent_():
            outfile.write('>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='contactlistType'):
        if self.locator is not None and 'locator' not in already_processed:
            already_processed.append('locator')
            outfile.write(' locator=%s' % (self.gds_format_string(quote_attrib(self.locator).encode(ExternalEncoding), input_name='locator'), ))
    def exportChildren(self, outfile, level, namespace_='', name_='contactlistType', fromsubclass_=False):
        if self.description is not None:
            showIndent(outfile, level)
            outfile.write('<%sdescription>%s</%sdescription>\n' % (namespace_, self.gds_format_string(quote_xml(self.description).encode(ExternalEncoding), input_name='description'), namespace_))
        for contact_ in self.contact:
            contact_.export(outfile, level, namespace_, name_='contact')
    def hasContent_(self):
        if (
            self.description is not None or
            self.contact
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='contactlistType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.locator is not None and 'locator' not in already_processed:
            already_processed.append('locator')
            showIndent(outfile, level)
            outfile.write('locator = "%s",\n' % (self.locator,))
    def exportLiteralChildren(self, outfile, level, name_):
        if self.description is not None:
            showIndent(outfile, level)
            outfile.write('description=%s,\n' % quote_python(self.description).encode(ExternalEncoding))
        showIndent(outfile, level)
        outfile.write('contact=[\n')
        level += 1
        for contact_ in self.contact:
            showIndent(outfile, level)
            outfile.write('model_.contactType(\n')
            contact_.exportLiteral(outfile, level, name_='contactType')
            showIndent(outfile, level)
            outfile.write('),\n')
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('locator', node)
        if value is not None and 'locator' not in already_processed:
            already_processed.append('locator')
            self.locator = value
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False):
        if nodeName_ == 'description':
            description_ = child_.text
            description_ = self.gds_validate_string(description_, node, 'description')
            self.description = description_
        elif nodeName_ == 'contact':
            obj_ = contactType.factory()
            obj_.build(child_)
            self.contact.append(obj_)
# end class contactlistType


class contactType(GeneratedsSuper):
    member_data_items_ = [
        MemberSpec_('priority', 'xs:float', 0),
        MemberSpec_('color-code', 'xs:string', 0),
        MemberSpec_('id', 'xs:integer', 0),
        MemberSpec_('first_name', 'xs:string', 0),
        MemberSpec_('last_name', 'xs:string', 0),
        MemberSpec_('interest', 'xs:string', 1),
        MemberSpec_('category', 'xs:integer', 0),
        ]
    subclass = None
    superclass = None
    def __init__(self, priority=None, color_code=None, id=None, first_name=None, last_name=None, interest=None, category=None):
        self.priority = cast_(float, priority)
        self.color_code = cast_(None, color_code)
        self.id = cast_(int, id)
        self.first_name = first_name
        self.last_name = last_name
        if interest is None:
            self.interest = []
        else:
            self.interest = interest
        self.category = category
    def factory(*args_, **kwargs_):
        if contactType.subclass:
            return contactType.subclass(*args_, **kwargs_)
        else:
            return contactType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_first_name(self): return self.first_name
    def set_first_name(self, first_name): self.first_name = first_name
    def get_last_name(self): return self.last_name
    def set_last_name(self, last_name): self.last_name = last_name
    def get_interest(self): return self.interest
    def set_interest(self, interest): self.interest = interest
    def add_interest(self, value): self.interest.append(value)
    def insert_interest(self, index, value): self.interest[index] = value
    def get_category(self): return self.category
    def set_category(self, category): self.category = category
    def get_priority(self): return self.priority
    def set_priority(self, priority): self.priority = priority
    def get_color_code(self): return self.color_code
    def set_color_code(self, color_code): self.color_code = color_code
    def get_id(self): return self.id
    def set_id(self, id): self.id = id
    def export(self, outfile, level, namespace_='', name_='contactType', namespacedef_=''):
        showIndent(outfile, level)
        outfile.write('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = []
        self.exportAttributes(outfile, level, already_processed, namespace_, name_='contactType')
        if self.hasContent_():
            outfile.write('>\n')
            self.exportChildren(outfile, level + 1, namespace_, name_)
            showIndent(outfile, level)
            outfile.write('</%s%s>\n' % (namespace_, name_))
        else:
            outfile.write('/>\n')
    def exportAttributes(self, outfile, level, already_processed, namespace_='', name_='contactType'):
        if self.priority is not None and 'priority' not in already_processed:
            already_processed.append('priority')
            outfile.write(' priority="%s"' % self.gds_format_float(self.priority, input_name='priority'))
        if self.color_code is not None and 'color_code' not in already_processed:
            already_processed.append('color_code')
            outfile.write(' color-code=%s' % (self.gds_format_string(quote_attrib(self.color_code).encode(ExternalEncoding), input_name='color-code'), ))
        if self.id is not None and 'id' not in already_processed:
            already_processed.append('id')
            outfile.write(' id="%s"' % self.gds_format_integer(self.id, input_name='id'))
    def exportChildren(self, outfile, level, namespace_='', name_='contactType', fromsubclass_=False):
        if self.first_name is not None:
            showIndent(outfile, level)
            outfile.write('<%sfirst-name>%s</%sfirst-name>\n' % (namespace_, self.gds_format_string(quote_xml(self.first_name).encode(ExternalEncoding), input_name='first-name'), namespace_))
        if self.last_name is not None:
            showIndent(outfile, level)
            outfile.write('<%slast-name>%s</%slast-name>\n' % (namespace_, self.gds_format_string(quote_xml(self.last_name).encode(ExternalEncoding), input_name='last-name'), namespace_))
        for interest_ in self.interest:
            showIndent(outfile, level)
            outfile.write('<%sinterest>%s</%sinterest>\n' % (namespace_, self.gds_format_string(quote_xml(interest_).encode(ExternalEncoding), input_name='interest'), namespace_))
        if self.category is not None:
            showIndent(outfile, level)
            outfile.write('<%scategory>%s</%scategory>\n' % (namespace_, self.gds_format_integer(self.category, input_name='category'), namespace_))
    def hasContent_(self):
        if (
            self.first_name is not None or
            self.last_name is not None or
            self.interest or
            self.category is not None
            ):
            return True
        else:
            return False
    def exportLiteral(self, outfile, level, name_='contactType'):
        level += 1
        self.exportLiteralAttributes(outfile, level, [], name_)
        if self.hasContent_():
            self.exportLiteralChildren(outfile, level, name_)
    def exportLiteralAttributes(self, outfile, level, already_processed, name_):
        if self.priority is not None and 'priority' not in already_processed:
            already_processed.append('priority')
            showIndent(outfile, level)
            outfile.write('priority = %f,\n' % (self.priority,))
        if self.color_code is not None and 'color_code' not in already_processed:
            already_processed.append('color_code')
            showIndent(outfile, level)
            outfile.write('color_code = "%s",\n' % (self.color_code,))
        if self.id is not None and 'id' not in already_processed:
            already_processed.append('id')
            showIndent(outfile, level)
            outfile.write('id = %d,\n' % (self.id,))
    def exportLiteralChildren(self, outfile, level, name_):
        if self.first_name is not None:
            showIndent(outfile, level)
            outfile.write('first_name=%s,\n' % quote_python(self.first_name).encode(ExternalEncoding))
        if self.last_name is not None:
            showIndent(outfile, level)
            outfile.write('last_name=%s,\n' % quote_python(self.last_name).encode(ExternalEncoding))
        showIndent(outfile, level)
        outfile.write('interest=[\n')
        level += 1
        for interest_ in self.interest:
            showIndent(outfile, level)
            outfile.write('%s,\n' % quote_python(interest_).encode(ExternalEncoding))
        level -= 1
        showIndent(outfile, level)
        outfile.write('],\n')
        if self.category is not None:
            showIndent(outfile, level)
            outfile.write('category=%d,\n' % self.category)
    def build(self, node):
        self.buildAttributes(node, node.attrib, [])
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('priority', node)
        if value is not None and 'priority' not in already_processed:
            already_processed.append('priority')
            try:
                self.priority = float(value)
            except ValueError as exp:
                raise ValueError('Bad float/double attribute (priority): %s' % exp)
        value = find_attr_value_('color-code', node)
        if value is not None and 'color-code' not in already_processed:
            already_processed.append('color-code')
            self.color_code = value
        value = find_attr_value_('id', node)
        if value is not None and 'id' not in already_processed:
            already_processed.append('id')
            try:
                self.id = int(value)
            except ValueError as exp:
                raise_parse_error(node, 'Bad integer attribute: %s' % exp)
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False):
        if nodeName_ == 'first-name':
            first_name_ = child_.text
            first_name_ = self.gds_validate_string(first_name_, node, 'first_name')
            self.first_name = first_name_
        elif nodeName_ == 'last-name':
            last_name_ = child_.text
            last_name_ = self.gds_validate_string(last_name_, node, 'last_name')
            self.last_name = last_name_
        elif nodeName_ == 'interest':
            interest_ = child_.text
            interest_ = self.gds_validate_string(interest_, node, 'interest')
            self.interest.append(interest_)
        elif nodeName_ == 'category':
            sval_ = child_.text
            try:
                ival_ = int(sval_)
            except (TypeError, ValueError) as exp:
                raise_parse_error(child_, 'requires integer: %s' % exp)
            ival_ = self.gds_validate_integer(ival_, node, 'category')
            self.category = ival_
# end class contactType


USAGE_TEXT = """
Usage: python <Parser>.py [ -s ] <in_xml_file>
"""

def usage():
    print(USAGE_TEXT)
    sys.exit(1)


def get_root_tag(node):
    tag = Tag_pattern_.match(node.tag).groups()[-1]
    rootClass = globals().get(tag)
    return tag, rootClass


def parse(inFileName):
    doc = parsexml_(inFileName)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'contact-list'
        rootClass = contactlistType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('<?xml version="1.0" ?>\n')
    rootObj.export(sys.stdout, 0, name_=rootTag, 
        namespacedef_='')
    return rootObj


def parseString(inString):
    from io import StringIO
    doc = parsexml_(StringIO(inString))
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'contact-list'
        rootClass = contactlistType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('<?xml version="1.0" ?>\n')
    rootObj.export(sys.stdout, 0, name_="contact-list",
        namespacedef_='')
    return rootObj


def parseLiteral(inFileName):
    doc = parsexml_(inFileName)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'contact-list'
        rootClass = contactlistType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('#from member_specs_api import *\n\n')
    sys.stdout.write('import member_specs_api as model_\n\n')
    sys.stdout.write('rootObj = model_.rootTag(\n')
    rootObj.exportLiteral(sys.stdout, 0, name_=rootTag)
    sys.stdout.write(')\n')
    return rootObj


def main():
    args = sys.argv[1:]
    if len(args) == 1:
        parse(args[0])
    else:
        usage()


if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    main()


__all__ = [
    "contactType",
    "contactlistType"
    ]
