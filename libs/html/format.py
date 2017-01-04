class HtmlFormat:
	def __init__(self, html_str):
		parse = Parse(html_str)
		pass;

#todo
#comment should be used as some new html string
class Parse:
	string = ''
	def __init__(self,html):
		self.string = rid_tag_space(html);
		self.split_tag()
		#todo /r/n 
		pass
	def split_tag(self):
		# state 1:tag opened
		# state 2:tag name
		# state 3:tag closed
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
		print state['tag_stack']

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