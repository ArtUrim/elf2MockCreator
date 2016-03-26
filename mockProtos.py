from elftools.dwarf.die import DIE
from dieByOffset import DieByOffset

class MockProto(object):

    def __init__(self,die):
        self.die = die
        if isinstance(die,DIE):
            self.kind = die.tag
            self.name = None

            if 'DW_AT_name' in die.attributes:
                self.name = die.attributes['DW_AT_name'].value.decode('utf-8')

            self.dbo = DieByOffset( self.die.cu )

    @staticmethod
    def findMockType(die):
        if not isinstance(die,DIE):
            return None
        if ( die.tag == 'DW_TAG_variable' and
                die.attributes['DW_AT_external'] ):
            return GlobalProto(die)
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
        typeDie = None
        mockDie = None
        if 'DW_AT_type' in self.die.attributes:
            offset = self.die.attributes['DW_AT_type'].value
            typeDie = self.dbo.getDie(offset)
            mockDie = MockProto.findMockType(typeDie)
        return (typeDie,mockDie)


class FinalProto(MockProto):
    def __init__(self,die):
        super().__init__(self,die)
        self.is_external = 0
        self.type = None

        if die.attributes['external']:
            self.is_external = die.attributes['external']
        if die.attributes['type']:
            self.type = die.attributes['type']

class GlobalProto(FinalProto):
    def __init__(self,die):
        super().__init__(self,die)

    def __str__(self):
        typeDieInfo = self.getType()
        if typeDieInfo[1]:
            return str(typeDieInfo[1]).format(self.name) + ";"

class FunctionProto(FinalProto):
    def __init__(self,die):
        super().__init__(self,die)

    def __str__(self):
        typeDieInfo = self.getType()
        if typeDieInfo[1]:
            return str(typeDieInfo[1]).format(self.name)  

class ModifierType(MockProto):
    def __init__(self,die):
        super().__init__(self,die)

    def __str__(self):
        ttname = None
        if self.die.tag == 'DW_TAG_pointer_type':
            ttname = "* {}"
        elif self.die.tag == 'DW_TAG_ptr_to_member_type':
            ttname = "* {}" # TODO: be more specific for this special case
        elif self.die.tag == 'DW_TAG_reference_type':
            ttname = "& {}"
        elif self.die.tag == 'DW_TAG_array_type':
            ttname = "{}"
            for childTags in self.die.iter_children():
                if isinstance(childTags,DIE) and 'DW_TAG_subrange_type' == childTags.tag:
                    if 'DW_AT_upper_bound' in childTags.attributes:
                        uppBound = childTags.attributes['DW_AT_upper_bound'].value + 1
                        ttname = ttname + "[{}]".format(uppBound)
        elif 'DW_AT_name' in self.die.attributes:
            ttname = self.die.attributes['DW_AT_name'].value.decode('ascii') + " {}"

        if ttname:
            ttname = str(self.getType()[1]).format(ttname)

        return ttname

class BasicType(MockProto):
    def __init__(self,die):
        super().__init__(self,die)

    def __str__(self):
        ttname = self.die.attributes['DW_AT_name'].value.decode('ascii')
        if self.die.tag == 'DW_TAG_enumeration_type':
            ttname = 'enum ' + ttname
        elif self.die.tag == 'DW_TAG_union_type':
            ttname = 'union ' + ttname
        elif self.die.tag == 'DW_TAG_structure_type':
            ttname = 'struct ' + ttname
        return ttname + " {}"
