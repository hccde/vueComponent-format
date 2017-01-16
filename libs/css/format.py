#if css string is not vaild ,we will not format it 
class CssFormat:
	def __init__(self, css_str,setting):
		css_str = read_file()

		print css_str

class Paser(object):
	#state 0 '{'
	#state 1 string
	#state 2 '}'
	#state 3 ';'
	strings=''
	def __init__(self, css_str):
		self.strings = css_str.strip()
	def get_css_obj(self):
		length = len(self.strings)
		string = self.string
		# brace_stack=[];
		# save the current nestting deepth
		nest_stack=[];
		current_style_obj = {}
		state = {
			collector:'',
			state:1
		}
		for index in range(0,length):
			if string[index]=='{' and state['state']==1:
				# is a classList,should new a classList obj and push into nest_stack
				current_style_obj = {
					"name":state['collector'],
					classList:[]
					}
				nest_stack.append(current_style_obj)
				state['collector'] = '';
				state['state'] = 0;
			elif state['state'] == 1 and string[index] != ';':
				state['collector']+=string[index];
				state['state'] = 1;
			elif state['state'] == 1 and string[index] == ';':
				current_style_obj['classList'].append(state['collector'])
				state['collector'] = '';
				#one csslist is found
				# obj[]
				pass
			elif state['state'] == 1 and string[index] == '}':
				pass
				# current classList is over
			else:
				pass;


		
		


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