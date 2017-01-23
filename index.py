import sublime
import sublime_plugin
import sys
import os
import json
from .libs.html import htmlformat
from .libs.css import cssformat
from .libs.js import jsformat
css_html_js = []
class FormatCommand(sublime_plugin.TextCommand):
    def run(self, edit):
    	print(111)
    	# get the first selection
    	global css_html_js
    	setting = json.load(open(os.path.dirname(os.path.realpath(__file__))+'/setting','r'))
    	selection = self.view.sel()[0];
    	selection_str = self.view.substr(selection)
    	code_set = SplitCode(selection_str)
    	html_str = code_set.get_html()
    	print(css_html_js)
    	# print(htmlformat.HtmlFormat(html_str,setting))
    	# Html.HtmlFormat(codeset.get_html(),setting)
		# Css.CssFormat(codeset.get_css(),setting)
		# Js.JsFormat('',setting);

    	# replace string 
    	# self.view.replace(edit,selection,selection_str)
class FormatEvent(sublime_plugin.EventListener):
	def run(self,view):
		pass
	def on_post_save(self,view):
		pass
	def on_modified(self,view):
		global css_html_js
		size = view.size()
		selection =  sublime.Region(0,size);
		selection_str =  view.substr(selection)
		code_set = SplitCode(selection_str)
		css_html_js.append(code_set.get_css())
		css_html_js.append(code_set.get_html())
		css_html_js.append(code_set.get_js())
	def on_activated(self,view):
		global css_html_js
		size = view.size()
		selection =  sublime.Region(0,size);
		selection_str =  view.substr(selection)
		code_set = SplitCode(selection_str)
		css_html_js.append(code_set.get_css())
		css_html_js.append(code_set.get_html())
		css_html_js.append(code_set.get_js())
		
class SplitCode:
	string = '';
	string_len = 0;
	def __init__(self, raw_str):
		# self.string = self.rid_tag_space(raw_str.strip())
		self.string = raw_str;
		self.string_len = len(self.string)
		pass
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
				# if self.string[index] != ' ' :
				state['collector'] += self.string[index]
				state['current_state'] = 2;
			#find special tag
		res = {
			'begin':-1,
			'end':-1
		}
		temIndex = -1;
		for index in range(0,len(state['tag_stack'])):
			raw_name = state['tag_stack'][index]['name']
			split_name_space = raw_name.split(' ')[0]
			split_name_enter = raw_name.split('\n')[0]
			names = raw_name
			if(split_name_space != raw_name):
				names = split_name_space
			if(split_name_enter != raw_name):
				names = split_name_enter
			if names == name:
				res['begin'] = state['tag_stack'][index]['begin']
			if names == '/'+name and res['begin'] != -1:
				temIndex = state['tag_stack'][index]['end']
				# include '>'
		res['end'] = temIndex+1;
		return res;

		


#test
# setting = json.load(open(os.path.dirname(os.path.realpath(__file__))+'/setting','r'))

# codeset = SplitCode('aaaa< template ><input type="mail" readonly required :v-mode="mail"></input><br /><div>\r\n</div><i class="title">hello </i><!-- <div>--></Div></Template>'+
	# '<script>console.log("</script>")</script><style type="text">.title{color:red;}</styLe>rrr')

#todo different input need to be pointed out

# print codeset.get_html()
# print codeset.get_css()
# print codeset.get_js()
# Html.HtmlFormat(codeset.get_html(),setting)
# Css.CssFormat(codeset.get_css(),setting)
# Js.JsFormat('',setting)

