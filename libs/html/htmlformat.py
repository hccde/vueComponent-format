setting ={}
class HtmlFormat:
	def __init__(self, html_str,settings,tab_before):
		global setting
		setting = settings;
		html_str = html_str.replace('\r\n','\n').replace('\r','\n').replace('\t',settings['tab_size']*' ')
		parse = Parse(html_str)
		html_format =  Format(parse.node_stack,tab_before)
		self.formated_str = html_format.formated_str
		pass;

#todo
#comment should be used as some new html string
class Parse:
	def __init__(self,html):
		self.string = rid_tag_space(html)
		self.tag_stack = self.split_tag()
		self.node_stack = self.create_node_stack();
		
	def split_tag(self):
		# state 1:tag opened
		# state 2:tag name
		# state 3:tag closed
		# state 4:text node
		# state 5:comment node
		state = {
			'current_state':3,
			#collect tag name
			'collector':'',
			#store splited tag
			'tag_stack':[]
		}

		length = len(self.string);
		for index in range(0,length):
			if self.string[index] =='<':
				if(state['current_state'] == 4):
					state['tag_stack'][len(state['tag_stack'])-1]['value'] = state['collector']
					state['collector'] = ''

				if state['current_state'] != 2:
					state['tag_stack'].append({
						'value':'',
						'end':-1,
						'begin':index,
						'type':'tag'
					})
					state['current_state'] = 1
				else:
					state['collector'] += self.string[index]

			elif self.string[index] == '>' and state['current_state'] == 2:
				#need to judge if it is a comment node
				name = state['collector'].lower();
				if(name.find('!--') == 0):
					if name[len(name)-1]!='-' or name[len(name)-2]!='-':
						state['collector'] += self.string[index]
						continue;
					else:
						state['tag_stack'][len(state['tag_stack'])-1]['value'] = state['collector']
						state['tag_stack'][len(state['tag_stack'])-1]['type'] = 'comment'

				state['current_state'] = 3;
				state['tag_stack'][len(state['tag_stack'])-1]['value'] = name;
				state['tag_stack'][len(state['tag_stack'])-1]['end'] = index;
				state['collector'] = ''

			elif state['current_state'] == 3:
				#text node
				state['tag_stack'].append({
						'value':'',
						'end':-1,
						'begin':index,
						'type':'text'
					})	
				state['collector'] += self.string[index]
				state['current_state'] = 4

			elif state['current_state'] == 4:
				state['collector'] += self.string[index]

			elif state['current_state']==1 or state['current_state']==2:
				state['collector'] += self.string[index]
				state['current_state'] = 2;

		return state['tag_stack']

	def create_node_stack(self):
		result_stack = []
		length = len(self.tag_stack)
		for index in range(0,length):
			result_stack.append(self.create_node(self.tag_stack[index]))
		return result_stack

	def create_node(self,obj):
		if obj['type'] == 'tag':
			node = self.create_ele_node(obj['value'])
		elif obj['type'] == 'text':
			node = self.create_text_node(obj['value'])
		else:
			# comments not 
			node = {
				'name':obj['value'],
				'attribute':[],
				'value':obj['value'],
				'type':'comment',
				'closeTag':False
				}
		return node



	def create_text_node(self,text_str):
		text_ele = {
			'type':'text',
			'name':'',
			'attribute':[],
			'value':text_str
		}
		return text_ele

	def create_ele_node(self,node_str):
		#attribute
		#state 1 tag_name
		#state 2 space
		#state 3 string
		#state 4 equal
		#state 5 begin
		state = {
			'current_state':5,
			'collector':'',
			'stack':[],
			'quotesflag':False,
			'isVoidEle':False
		}
		#auto closed void element
		if len(node_str) > 0 and node_str[len(node_str)-1] == '/':
			state['isVoidEle'] = True
			node_str = node_str[0:len(node_str)-1]
		# we should notice value of attribute containe '='
		length = len(node_str)
		for index in range(0,length):
			if node_str[index] == '"' or node_str[index] == "'":
				state['quotesflag'] = not state['quotesflag']
			if node_str[index] == '=' and state['current_state'] != 2:
				if not state['quotesflag']:
					state['stack'].append(state['collector'])
					state['collector'] = ''
					state['stack'].append('=')
					state['current_state'] = 2;
					continue
				else:
					state['collector'] += node_str[index]
			elif state['current_state']==5 and node_str[index]==' ' and (not state['quotesflag']):
				state['stack'].append(state['collector'])
				state['collector'] = ''
				state['current_state'] = 2
				continue
			elif(state['current_state'] == 5):
				state['collector'] += node_str[index]
			elif state['current_state'] == 2 and node_str[index]!=' ':
				state['collector'] += node_str[index]
				state['current_state'] = 3
			elif state['current_state']== 3 and node_str[index]!=' ':
				state['collector'] += node_str[index]
			elif state['current_state'] == 3 and node_str[index]==' ' and (not state['quotesflag']):
				state['stack'].append(state['collector'])
				state['collector'] = ''
				state['current_state'] = 2
			else:
				state['collector'] += node_str[index]
		state['stack'].append(state['collector'])

		# create dom object
		# use list in case of attributes out of sort
		dom_ele = {
			'type':'tag',
			'name':state['stack'].pop(0),
			'attribute':[],
			'isVoidEle':state['isVoidEle'],
			'value':''
		}
		dom_ele['closeTag'] = dom_ele['name'][0] == '/'
		work_stack = []
		result_stack=[]
		index = 0;
		length = len(state['stack'])
		while index < length:
			if state['stack'][index] == '=' and length >= index+1:
				obj = {
					work_stack.pop():state['stack'][index+1]
				}
				for i in range(0,len(work_stack)):
					result_stack.append(work_stack[i])
				result_stack.append(obj)
				work_stack = []
				index += 1
			else:
				if len(state['stack'][index].strip())>0:
					work_stack.append(state['stack'][index])
				
			index+=1

		for i in range(0,len(work_stack)):
			result_stack.append(work_stack[i])

		dom_ele['attribute'] = result_stack
		return dom_ele;

def rid_tag_space(raw_str):
		index = 0;
		while True:
			index = raw_str.find('<',index)
			if index == -1:
				break

			space_len = 0;
			while raw_str[space_len+index+1] == ' ':
				space_len+=1

			if space_len > 0:
				raw_str = raw_str[:index+1]+raw_str[index+1+space_len:]
			index += 1;
		index = 0

		while True:
			index = raw_str.find('>',index)
			if index == -1:
				break
			space_len = 0;

			while raw_str[index-space_len-1] == ' ':
				space_len+=1

			if space_len > 0:
				raw_str = raw_str[:index-space_len]+raw_str[index:]
			index+=1

		return raw_str

class Format:
	def __init__(self, stack,tab_before):
		#remove '/n' '/space' between tags
		self.node_stack = []
		for index in range(0,len(stack)):
			stack[index]['value'] = stack[index]['value'].strip();
			if(stack[index]['type'] !='tag'):
				if len(stack[index]['value']):
					self.node_stack.append(stack[index])
			else:
				self.node_stack.append(stack[index])
		self.formated_str = self.format(tab_before)

	def make_tag_pair(self):
		pass
	#we dont consider unclosed tag at first
	def format(self,tab_before):
		formated_str = ''
		is_void_ele = False;
		index_tab = tab_before;
		size = setting['tab_size']
		self.html_setting = html_setting = setting['html']
		work_stack = []
		last_node_type='text'
		sigle_line=False
		self.node_stack.insert(0, {'attribute': [], 
			'closeTag': False, 
			'name': '', 
			'isVoidEle': False,
			'type':'text',
			'value':''
			})
		for index in range(1,len(self.node_stack)):
			node_obj = self.node_stack[index]
			if node_obj['type'] != 'tag':
				#not tag,in fact,we should control indent by text length
				index_tab-=1;
			elif self.is_in_list(node_obj['name'],html_setting['blacklist']):
				#todo  tag name in blacklist 
				if( not node_obj['closeTag']):
					work_stack.append(node_obj['name'])
				pass;
			elif self.is_in_list(node_obj['name'],html_setting['noindent']):
				#should not be indent
				index_tab-=1;
				index_tab = (index_tab if index_tab>=0 else 0)
				if( not node_obj['closeTag'] and node_obj['name'] !='!doctype'):
					work_stack.append(node_obj['name'])
			elif self.is_in_list(node_obj['name'],html_setting['void_ele']) or node_obj['isVoidEle']:
				#has no content
				is_void_ele = True;
				pass
			else:
				if( not node_obj['closeTag']):
					work_stack.append(node_obj['name'])


			if node_obj['type'] == 'text':
				if last_node_type == 'openTag':
					if (len(node_obj['value']) > html_setting['max_text_length']):
						value_list =  node_obj['value'].split('\n');
						for count in range(0,len(value_list)):
							value_list[count] = '\n'+(index_tab+1)*size*' '+value_list[count].strip()
						formated_str+='\n'.join(value_list)
					else:
						sigle_line = self.node_stack[index+1]['closeTag'] and self.node_stack[index+1]['name']=='/'+self.node_stack[index-1]['name'];
						if sigle_line:
							formated_str+=node_obj['value']
						else:
							formated_str+='\n'+(index_tab+1)*size*' '+node_obj['value']
				else:
					formated_str+='\n'+(index_tab+1)*size*' '+node_obj['value']
				last_node_type='text'
			else:
				if node_obj['closeTag']:
					#no content element
					if '/'+self.node_stack[index-1]['name'] == node_obj['name']:
						sigle_line = True;
					if len(work_stack)-1 >= 0 and '/'+ work_stack[len(work_stack)-1] == node_obj['name']:
						work_stack.pop()
						index_tab-=1
						if not sigle_line:
							formated_str+='\n'+index_tab*size*' '+self.node_to_str(node_obj,(index_tab+1)*size)
							index_tab-=1
						else:
							formated_str+=self.node_to_str(node_obj,(index_tab+1)*size)
							index_tab-=1;
							#whether should be a sigle line
						sigle_line = False
					else:
						#cant match
						formated_str+=self.node_to_str(node_obj,(index_tab+1)*size)
						index_tab-=1;
					last_node_type = 'closeTag'
				else:
					#if forbid Nesting,then should help coders close this tag
					formated_str+='\n'+index_tab*size*' '+self.node_to_str(node_obj,(index_tab+1)*size)
					last_node_type = 'openTag'
					if is_void_ele:
						index_tab-=1;
			index_tab+=1
			#work_stack

			#reset 
			is_void_ele = False
		formated_str = formated_str.strip();
		return formated_str

	def is_in_list(self,node_name,arr):
		for index in range(0,len(arr)):
			if arr[index] == node_name:
				return True
		return False

		#turn node obj to string
	def node_to_str(self,node,space_count):
		#for void element , like <br/>,turn into <br>
		length = len(node['attribute'])
		long_attribute = length >= self.html_setting['max_attribute_count'];

		if node['name'] == '!doctype':
			node['name'] = '!Doctype'
		html_node_string = '<'+node['name']+' ';
		if length>0:
			if type(node['attribute'][0]) == dict:
				html_node_string += self.attribute_dict_tostr(node['attribute'][0])
			else:
				html_node_string += node['attribute'][0]+' '

			for index in range(1,length):
				if type(node['attribute'][index]) == dict:
					#attribute is keyValue form
					if long_attribute:
						html_node_string +='\n'+(space_count+1)*' '+self.attribute_dict_tostr(node['attribute'][index])
					else:
						html_node_string += self.attribute_dict_tostr(node['attribute'][index])
				else:
					if long_attribute:
						html_node_string += '\n'+(space_count+1)*' '+node['attribute'][index].strip()+' '
					else:
						html_node_string += node['attribute'][index].strip()+' '

		return html_node_string.rstrip()+'>'

	def attribute_dict_tostr(self,dict_obj):
		#todo long vue attribute
		key_list = list(dict.keys(dict_obj))
		return key_list[0].strip()+' = ' +dict_obj[key_list[0]].strip()+' ';
