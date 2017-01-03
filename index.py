import sublime
import sublime_plugin
import sys

#main class
class FormatCommand(sublime_plugin.TextCommand):
    def run(self, edit):
    	#get the first selection
    	selection = self.view.sel()[0];
    	selection_str = self.view.substr(selection)
    	code_set = SplitCode(selection_str)
    	selection_str = code_set.get_html()
    	#replace string 
    	self.view.replace(edit,selection,selection_str)


class SplitCode:
	string = '';
	string_len = 0;
	def __init__(self, raw_str):
		# self.string = self.rid_tag_space(raw_str.strip())
		self.string = raw_str;
		self.string_len = len(self.string)
		pass

#TODO : if code has string contain'</script>',like 
	#console.log('</script>')
#we will get error position,must consider this problem
#for this problem,we can solve it by always get the last its closed tag which is the outer tag
	def get_html(self):
		Pos = self.get_tag_byname('template')
		return self.string[Pos['begin']:Pos['end']]

	def get_css(self):
		Pos = self.get_tag_byname('style')
		return self.string[Pos['begin']:Pos['end']]

	def get_js(self):
		Pos = self.get_tag_byname('script')
		return self.string[Pos['begin']:Pos['end']]

	def rid_tag_space(self,raw_str):
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
				print(raw_str)
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
		print(raw_str)
		return raw_str

		#just for <script> <template> <style>
		""" 
			state 0:Null
			state 1:tag opened
			state 2:tag name
			state 3:tag closed
			if has a space in tag,we will ignore it;
		"""
	def get_tag_byname(self,name):
		length = len(self.string);
		state = {
			'current_state':3,
			#collect tag name
			'collector':'',
			#store splited tag
			'tag_stack':[] 
		}
		for index in range(0,length):
			if self.string[index] =='<':
				state['current_state'] = 1
			elif self.string[index] == '>':
				state['current_state'] = 3;
				state['tag_stack'].append({
						'name':state['collector'].lower(),
						'position':index
					})
				state['collector'] = ''
			elif state['current_state'] < 3:
				state['collector'] = self.string[index] != ' ' and state['collector']+self.string[index]
				state['current_state'] = 2;
		print(state['tag_stack'])
			#find special tag
		res = {
			'begin':-1,
			'end':-1
		}
		temIndex = -1;
		for index in range(0,len(state['tag_stack'])):
			if state['tag_stack'] == name:
				res['begin'] = index
			if state['tag_stack'] == '/'+name and res['begin'] != -1:
				temIndex = index
		res['end'] = temIndex

		return res;

		