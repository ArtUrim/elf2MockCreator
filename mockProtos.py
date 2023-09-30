##################################
# elf2MockCreator/mockProtos
#
# String destription of TAGs types
#
# Artur Lozinski (lozinski dot artur at gmail dor com)
# This code is the public domain
# #######################################
from elftools.dwarf.die import DIE
from dieByOffset import DieByOffset
import re

class MockProto(object):
    """ String destription of TAGs types. This is an abstract class, not for use in ANY
        instance. Includes two method (one of them static) to define what type is a DIE, and
        similarly what's kind of the type of the DIE (if exists).

        The main idea is that any usable DIE type has its own inherited class, which
        defined __str__ method to print necessary string.

        For more complited cases (like pointer type) the mechanism of the str.format() is
        used, while the more specific type information is put into the basic specification
        as a formattting (compare FunctionProto.__str__ for reference).

        Public methods:
            findMockType -- static method to define DIE type (mostly by the DIE TAG info).

            getType -- returns a tuple (derived from the object itself):
                * reference to DIE
                * reference to objected of inherited class from MockProto
    """

    unknownObjectNum = 1

    def __init__(self,die):
        """ die:
                reference to pyelftool/dwarf/die
        """
        self.die = die
        if isinstance(die,DIE):
            self.kind = die.tag
            self.name = None

            if 'DW_AT_name' in die.attributes:
                self.name = die.attributes['DW_AT_name'].value.decode('utf-8')

            self.dbo = DieByOffset( self.die.cu )

    @staticmethod
    def findMockType(die):
        """ die:
                reference to pyelftool/dwarf/die

            return reference to newly created object inherited from MockProto
        """
        if not isinstance(die,DIE):
            return None
        if ( die.tag == 'DW_TAG_variable' and
                die.attributes['DW_AT_external'] ):
            return GlobalProto(die)
        if ( die.tag == 'DW_TAG_formal_parameter' ):
            retval = GlobalProto(die,1)
            (typeD,mockD) = retval.getType()
            if typeD.tag == 'DW_TAG_pointer_type':
                if mockD.getType()[0].tag == 'DW_TAG_subroutine_type':
                    objName = None
                    if 'DW_AT_name' in die.attributes:
                        objName = die.attributes['DW_AT_name'].value
                    retval = PFuncProto(mockD.getType()[0], objName )
            return retval
        elif ( die.tag == 'DW_TAG_unspecified_parameters' ):
            return VarArgsProto(die)
        elif ( die.tag == 'DW_TAG_subprogram' and
                die.attributes['DW_AT_external'] ):
            return FunctionProto(die)
        elif die.tag == 'DW_TAG_enumeration_type':
            return BasicType(die)
        elif die.tag == 'DW_TAG_union_type':
            return BasicType(die)
        elif die.tag == 'DW_TAG_structure_type':
            return BasicType(die)
        elif die.tag == 'DW_TAG_class_type':
            return BasicType(die)
        elif die.tag == 'DW_TAG_base_type':
            return BasicType(die)
        elif die.tag == 'DW_TAG_typedef':
            return BasicType(die)
        elif die.tag == 'DW_TAG_pointer_type':
            return ModifierType(die)
        elif die.tag == 'DW_TAG_ptr_to_member_type':
            return ModifierType(die)
        elif die.tag == 'DW_TAG_reference_type':
            return ModifierType(die)
        elif die.tag == 'DW_TAG_array_type':
            return ModifierType(die)
        else:
            return None

    def getType(self):
        """ Return a pair (tuple):
                * reference to DIE
                * reference to objected of inherited class from MockProto

            Both are None if type is not found in the attributes
        """
        typeDie = None
        mockDie = None
        if 'DW_AT_type' in self.die.attributes:
            offset = self.die.attributes['DW_AT_type'].value
            typeDie = self.dbo.getDie(offset)
            mockDie = MockProto.findMockType(typeDie)
        return (typeDie,mockDie)


class FinalProto(MockProto):
    """ Abstract class only for logical distinguish of the final DIE (which is not type of
        other DIE).

        Attributes:
            is_external -- set to nonzero if DIE has an attribute external, and it is
                nonzero
    """

    def __init__(self,die):
        super().__init__(die)
        self.is_external = None
        self.isExternal()

    def isExternal(self):
        if 'DW_AT_external' in self.die.attributes:
            self.is_external = self.die.attributes['DW_AT_external']

class GlobalProto(FinalProto):
    """ Used for global variables. 
    """
    def __init__(self,die,is_param=0):
        """ is_param:
                nonzero if the str representation has ';' at its end. 0 by default.
        """
        super().__init__(die)
        self.is_param = is_param
        if self.name is None:
            self.name = 'var' + str(MockProto.unknownObjectNum)
            MockProto.unknownObjectNum += 1

    def __str__(self):
        typeDieInfo = self.getType()
        if typeDieInfo[1]:
            retStr = str(typeDieInfo[1]).format(self.name)
            if 0 == self.is_param:
                retStr += ';'
            return retStr
        else:
            return ""

    def getTypeName(self):
        typeDieInfo = self.getType()
        if typeDieInfo[1]:
            retStr = typeDieInfo[1].getTypeName()
            return retStr
        else:
            return ""

class MockData:

    def __init__(self,name,retval):
        self.name = name
        self.retv = retval
        self.args = []

    def add_arg( self, typ, name ):
        self.args.append( [typ,name])

class FunctionProto(FinalProto):
    """ Used for standalone function
    """
    def __init__(self,die):
        super().__init__(die)

    def mockData(self):
        retv = 'void'
        typeDieInfo = self.getType()
        if typeDieInfo[1]:
            retv = typeDieInfo[1].getTypeName()
        retVal = MockData( self.name, retv )

        for childTag in self.die.iter_children():
            if isinstance(childTag,DIE) and 'DW_TAG_formal_parameter' == childTag.tag:
                mp = MockProto.findMockType(childTag)
                if mp:
                    vmp = mp.getType()[1]
                if isinstance( mp, PFuncProto ):
                    retVal.add_arg( mp.name, mp.getTypeName() )
                else:
                    retVal.add_arg( mp.name, vmp.getTypeName() )

        return retVal

    def __str__(self):
        typeDieInfo = self.getType()
        retStr = ""
        if typeDieInfo[1]:
            retStr = str(typeDieInfo[1]).format(self.name) + '('
        else:
            retStr = "void {}".format(self.name) + '('
        comma = None
        for childTag in self.die.iter_children():
            if isinstance(childTag,DIE) and 'DW_TAG_formal_parameter' == childTag.tag:
                if comma:
                    retStr = retStr + ','
                else:
                    comma = 1
                retStr = retStr + ' ' + str(MockProto.findMockType(childTag)) + ' '

        return retStr + ");"

class PFuncProto(FunctionProto):
    """ Used for pointer to function
    """
    def __init__(self,die,name=None):
        super().__init__(die)
        if name is None:
            self.name = 'pFunc' + str(MockProto.unknownObjectNum)
            MockProto.unknownObjectNum += 1
        elif isinstance(name,bytes):
            self.name = name.decode("utf-8")
        else:
            self.name = name

    def getTypeName(self):
        typeDieInfo = self.getType()
        retStr = ""
        if typeDieInfo[1]:
            retStr = str(typeDieInfo[1]).format('(*)') + '('
        else:
            retStr = "void (*)("
        comma = None
        for childTag in self.die.iter_children():
            if isinstance(childTag,DIE) and 'DW_TAG_formal_parameter' == childTag.tag:
                if comma:
                    retStr = retStr + ','
                else:
                    comma = 1
                retStr = (retStr + ' ' +
                    MockProto.findMockType(childTag).getTypeName() + ' ')
    
        return retStr + ")"

    def __str__(self):
        if self.name:
            return re.sub( '\(\*\)', '(*' + self.name + ')',
                          self.getTypeName() )
        else:
            return self.getTypeName()


class ModifierType(MockProto):
    """ Any kind of modification type (pointer, array, and so on)
    """
    def __init__(self,die):
        super().__init__(die)

    def getTypeName(self):
        ttname = None
        if self.die.tag == 'DW_TAG_pointer_type':
            ttname = "*"
        elif self.die.tag == 'DW_TAG_ptr_to_member_type':
            ttname = "*" # TODO: be more specific for this special case
        elif self.die.tag == 'DW_TAG_reference_type':
            ttname = "&"
        elif self.die.tag == 'DW_TAG_array_type':
            ttname = ""
            for childTag in self.die.iter_children():
                if isinstance(childTag,DIE) and 'DW_TAG_subrange_type' == childTag.tag:
                    if 'DW_AT_upper_bound' in childTag.attributes:
                        uppBound = childTag.attributes['DW_AT_upper_bound'].value + 1
                        ttname = ttname + "[{}]".format(uppBound)
        elif 'DW_AT_name' in self.die.attributes:
            ttname = self.die.attributes['DW_AT_name'].value.decode('ascii')

        if ttname:
            ttname = str(self.getType()[1]).format(ttname)

        return ttname


    def __str__(self):
        if self.die.tag == 'DW_TAG_array_type':
            ttname = "{}"
            for childTag in self.die.iter_children():
                if isinstance(childTag,DIE) and 'DW_TAG_subrange_type' == childTag.tag:
                    if 'DW_AT_upper_bound' in childTag.attributes:
                        uppBound = childTag.attributes['DW_AT_upper_bound'].value + 1
                        ttname = ttname + "[{}]".format(uppBound)
            return str(self.getType()[1]).format(ttname)

        return self.getTypeName() + " {}"

class BasicType(MockProto):
    """ Basic means the last in the type chain. So, this is not only types like 'int' but
        also enum, struct, or typedef, when no more modification of the type is required.
    """
    
    def __init__(self,die):
        super().__init__(die)

    def getTypeName(self):
        ttname = self.die.attributes['DW_AT_name'].value.decode('ascii')
        if self.die.tag == 'DW_TAG_enumeration_type':
            ttname = 'enum ' + ttname
        elif self.die.tag == 'DW_TAG_union_type':
            ttname = 'union ' + ttname
        elif self.die.tag == 'DW_TAG_structure_type':
            ttname = 'struct ' + ttname
        return ttname

    def __str__(self):
        return self.getTypeName() + " {}"

class VarArgsProto(GlobalProto):

    def __init__(self,die):
        super().__init__(die)

    def getTypeName(self):
        pass

    def __str__(self):
        return '...'
