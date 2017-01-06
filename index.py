# import sublime
# import sublime_plugin
# import sys

#import html-format module
import libs.html.format as Html

#main class
# class FormatCommand(sublime_plugin.TextCommand):
    # def run(self, edit):
    	#get the first selection
    	# selection = self.view.sel()[0];
    	# selection_str = self.view.substr(selection)
    	# code_set = SplitCode(selection_str)
    	# selection_str = code_set.get_html()
    	#replace string 
    	# self.view.replace(edit,selection,selection_str)


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
			if self.string[index] =='<' and state['current_state']==3:
				state['current_state'] = 1
				state['tag_stack'].append({
						'name':'',
						'end':-1,
						'begin':index
					})
			elif self.string[index] == '>' and state['current_state'] == 2:
				state['current_state'] = 3;
				state['tag_stack'][len(state['tag_stack'])-1]['name'] = state['collector'].lower();
				state['tag_stack'][len(state['tag_stack'])-1]['end'] = index;
				state['collector'] = ''
			elif state['current_state']==1 or state['current_state']==2:
				if self.string[index] != ' ' :
					state['collector'] += self.string[index]
				state['current_state'] = 2;
			#find special tag
		res = {
			'begin':-1,
			'end':-1
		}
		temIndex = -1;
		for index in range(0,len(state['tag_stack'])):
			if state['tag_stack'][index]['name'] == name:
				res['begin'] = state['tag_stack'][index]['begin']
			if state['tag_stack'][index]['name'] == '/'+name and res['begin'] != -1:
				temIndex = state['tag_stack'][index]['end']
				# include '>'
		res['end'] = temIndex+1;
		# print state['tag_stack']
		return res;

		


#test

codeset = SplitCode('aaaa< template ><input type="mail" readonly required :v-mode="mail"></input<div>\r\n<i class="title">hello </i><!-- <div>--></Div></Template>'+
	'<script>console.log("</script>")</script><style></styLe>rrr')
# print codeset.get_html()
# print codeset.get_css()
# print codeset.get_js()
Html.HtmlFormat(codeset.get_html())
