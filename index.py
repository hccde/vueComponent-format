import sublime
import sublime_plugin
import sys
import os
import json
from .libs.html import htmlformat
from .libs.css import cssformat
from .libs.js import jsformat
css_html_js = [{'begin':0,'end':0},{'begin':0,'end':0},{'begin':0,'end':0}]
class FormatCommand(sublime_plugin.TextCommand):
    def run(self, edit):
    	# get the first selection
    	global css_html_js
    	selection = list(self.view.sel())[0];
    	# selection_str = self.view.substr(selection)
    	# print(css_html_js)
    	self.dispatch(selection)
    	# self.view.sel().clear()
    	# replace string 
    	# self.view.replace(edit,selection,selection_str)
    def dispatch(self,reg):
    	global css_html_js
    	setting = json.load(open(os.path.dirname(os.path.realpath(__file__))+'/setting','r'))
    	begin = reg.begin()
    	end = reg.end()

    	def in_which_seg(point):
    		if(css_html_js[0]['end']>point):
    			return 0
    		elif(css_html_js[1]['end']>point):
    			return 1
    		else:
    			return 2

    	def format_str(segment_number,begin,end):
    		region_str = css_html_js[3][begin:end+1]
    		if segment_number == 0:
    			css = cssformat.CssFormat(region_str,setting)
    			return css.formated_str
    		elif segment_number == 1:
    			html = htmlformat.HtmlFormat(region_str,setting)
    			# print(html.formated_str)
    			return html.formated_str
    		else:
    			js = jsformat.JsFormat(region_str,setting)
    			return js.formated_str

    	segment_number = in_which_seg(begin)
    	formated_str = ''
    	if css_html_js[segment_number]['end'] >= begin:
    		formated_str+=format_str(segment_number,begin,end)
    	else:
    		formated_str+=format_str(segment_number,begin,css_html_js[segment_number]['end'])
    		begin = css_html_js[segment_number]['end']+1
    		if(css_html_js[segment_number+1]['end'] >= end):
    			formated_str+=format_str(segment_number+1,begin,end)
    		else:
    			formated_str+=format_str(segment_number+1,begin,css_html_js[segment_number+1]['end'])
    			begin = css_html_js[segment_number+1]['end']+1
    			if(css_html_js[segment_number+1]['end'] >= end):
    				formated_str+=format_str(segment_number+2,begin,end)
    			else:
    				#something error
    				pass
    	print(formated_str)
    	return formated_str;


class FormatEvent(sublime_plugin.EventListener):
	def run(self,view):
		pass
	def on_post_save(self,view):
		pass
	def on_modified(self,view):
		global css_html_js
		css_html_js = []
		size = view.size()
		selection =  sublime.Region(0,size);
		selection_str =  view.substr(selection)
		code_set = SplitCode(selection_str)
		css_html_js.append(code_set.get_css())
		css_html_js.append(code_set.get_html())
		css_html_js.append(code_set.get_js())
		css_html_js.append(selection_str)
	def on_activated(self,view):
		global css_html_js
		css_html_js = []
		size = view.size()
		selection =  sublime.Region(0,size);
		selection_str =  view.substr(selection)
		code_set = SplitCode(selection_str)
		css_html_js.append(code_set.get_css())
		css_html_js.append(code_set.get_html())
		css_html_js.append(code_set.get_js())
		css_html_js.append(selection_str)

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
		# return self.string[Pos['begin']:Pos['end']]
		return Pos

	def get_css(self):
		Pos = self.get_tag_byname('style')
		# return self.string[Pos['begin']:Pos['end']]
		return Pos

	def get_js(self):
		Pos = self.get_tag_byname('script')
		# return self.string[Pos['begin']:Pos['end']]
		return Pos
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
			split_name_table = raw_name.split('	')[0]
			split_name_enter = raw_name.split('\n')[0]
			names = raw_name
			if(split_name_space != raw_name):
				names = split_name_space
			if(split_name_enter != raw_name):
				names = split_name_enter
			if(split_name_table != raw_name):
				names = split_name_table
			if names == name:
				res['begin'] = state['tag_stack'][index]['begin']
			if names == '/'+name and res['begin'] != -1:
				temIndex = state['tag_stack'][index]['end']
				# include '>'
		res['end'] = temIndex+1;
		return res;
