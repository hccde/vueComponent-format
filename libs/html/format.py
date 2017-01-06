class HtmlFormat:
	def __init__(self, html_str):
		parse = Parse(html_str)
		pass;

#todo
#comment should be used as some new html string
class Parse:
	string = ''
	tag_stack = []
	node_stack = []
	def __init__(self,html):
		self.string = rid_tag_space(html);
		self.tag_stack = self.split_tag()
		# self.node_stack = self.create_node()
		self.create_node('div readonly class="test=" value=     111 required readonly "name"==a')
		#todo /r/n 
		pass
	def split_tag(self):
		# state 1:tag opened
		# state 2:tag name
		# state 3:tag closed
		# state 4:text node
		length = len(self.string);
		state = {
			'current_state':3,
			#collect tag name
			'collector':'',
			#store splited tag
			'tag_stack':[]
		}
		for index in range(0,length):
			if self.string[index] =='<' and state['current_state']!=1:
				if(state['current_state'] == 4):
					state['tag_stack'][len(state['tag_stack'])-1]['name'] = state['collector']
					state['collector'] = ''
				
				state['tag_stack'].append({
					'name':'',
					'end':-1,
					'begin':index,
					'type':'tag'
				})
				state['current_state'] = 1
			elif self.string[index] == '>' and state['current_state'] == 2:
				#need to judge if it is a comment node
				name = state['collector'].lower();
				if(name.find('!--') == 0):
					if name[len(name)-1]!='-' or name[len(name)-2]!='-':
						state['collector'] += self.string[index]
						continue;
					else:
						state['tag_stack'][len(state['tag_stack'])-1]['name'] = state['collector']
						state['tag_stack'][len(state['tag_stack'])-1]['tag'] = 'comment'

				state['current_state'] = 3;
				state['tag_stack'][len(state['tag_stack'])-1]['name'] = name;
				state['tag_stack'][len(state['tag_stack'])-1]['end'] = index;
				state['collector'] = ''
			elif state['current_state'] == 3:
				#text node
				state['tag_stack'].append({
						'name':'',
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
		# print state['tag_stack']

	def create_node(self,node_str):
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
			'quotesflag':False
		}
		# we should notice value of attribute containe '=' todo
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
			elif state['current_state']==5 and node_str[index]==' ':
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
			elif state['current_state'] == 3 and node_str[index]==' ':
				state['stack'].append(state['collector'])
				state['collector'] = ''
				state['current_state'] = 2
		state['stack'].append(state['collector'])
		print(state['stack'])

		# create dom object
		# use list in case of attributes out of sort
		dom_ele = {
			'name':state['stack'].pop(0),
			'attribute':[]
		}
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
				work_stack.append(state['stack'][index])
				
			index+=1

		for i in range(0,len(work_stack)):
			work_stack.append(work_stack[i])

		print result_stack
		dom_ele['attribute'] = result_stack











		pass;
	def create_tree(self):
		pass


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