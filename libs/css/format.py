#if css string is not vaild ,we will not format it 
class CssFormat:
	def __init__(self, css_str,setting):
		css_str = read_file()
		parse = Paser(css_str)
		# print css_str

class Paser:
	#state 0 '{'
	#state 1 string
	#state 2 '}'
	#state 3 ';'
	strings=''
	def __init__(self, css_str):
		self.strings = css_str.strip()
		self.get_css_obj()
	def get_css_obj(self):
		length = len(self.strings)
		string = self.strings
		# brace_stack=[];
		# save the current nestting deepth
		nest_stack=[]
		work_stack=[]
		current_style_obj = ''
		state = {
			'collector':'',
			'state':1
		}
		for index in range(0,length):
			if string[index]=='{' :
				# is a styleList,should new a styleList obj and push into nest_stack
				new_style_obj = {
						"name":state['collector'],
						"classList":[],
						"children":[]
					}
				if current_style_obj == '':
					#if it is nested
					current_style_obj = new_style_obj
					nest_stack.append(current_style_obj)
				else:
					current_style_obj['children'].append(new_style_obj)
					current_style_obj = new_style_obj

				work_stack.append(current_style_obj)
				state['collector'] = '';
				state['state'] = 0;
			elif state['state'] == 1 and string[index] == ';':
				if current_style_obj != '':
					current_style_obj['classList'].append(state['collector'])
				else:
					nest_stack.append(state['collector'])
				state['collector'] = '';
				#one csslist is found
			elif string[index] == '}':
				if(state['collector'].strip() != ''):
					





					current_style_obj["classList"].append(state['collector'])
				state['collector'] = ''
				work_stack.pop()
				if len(work_stack)>0:
					current_style_obj = work_stack[len(work_stack)-1]
				else:
					current_style_obj = ''
				state['state'] = 2
				pass
			else:
				state['collector']+=string[index];
				state['state'] = 1;
				pass;

		print nest_stack;

class Format:
	def __init__(self,token_stack):
		pass
		


def read_file():
	#current running script is index.py
	fs = open('vue-example')
	html_str = fs.read();
	fs.close( )
	return html_str
	
def write_file(string):
	fs = open('vue-example','r+')
	fs.write(string)
	fs.close()