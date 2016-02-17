

class MockProto(object):
	def __init__(self,die):
		self.die = die
		self.kind = die.tag
		self.name = None
		if die.attributes['name']:
			self.name = die.attributes['name']

	@staticmethod
	def findMockType(die):
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

class FunctionProto(FinalProto):
	def __init__(self,die):
		super().__init__(self,die)

class ModifierType(MockProto):
	def __init__(self,die):
		super().__init__(self,die)

	def __str__(self):
		ttname = self.die.attributes['DW_AT_name'].value.decode('ascii')
		if die.tag == 'DW_TAG_pointer_type':
			ttname = 'enum ' + ttname
		elif die.tag == 'DW_TAG_ptr_to_member_type':
			ttname = 'union ' + ttname
		elif die.tag == 'DW_TAG_reference_type':
			ttname = 'struct ' + ttname
		elif die.tag == 'DW_TAG_array_type':
			ttname = 'struct ' + ttname
		return ttname

class BasicType(MockProto):
	def __init__(self,die):
		super().__init__(self,die)

	def __str__(self):
		ttname = self.die.attributes['DW_AT_name'].value.decode('ascii')
		if die.tag == 'DW_TAG_enumeration_type':
			ttname = 'enum ' + ttname
		elif die.tag == 'DW_TAG_union_type':
			ttname = 'union ' + ttname
		elif die.tag == 'DW_TAG_structure_type':
			ttname = 'struct ' + ttname
		return ttname + ' {}'
