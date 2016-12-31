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
		self.string = self.rid_tag_space(raw_str.strip())
		self.string_len = len(self.string)
		pass

	def get_html(self):
		return self.string
		pass

	def get_css(self):
		pass

	def get_js(self):
		pass

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
		