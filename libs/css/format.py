class CssFormat:
	def __init__(self, css_str,setting):
		css_str = read_file()

		print css_str

class Paser(object):
	#state 0 '}'
	#state 1 string
	#state 2 '{'
	#state 3 ';'
	strings=''
	def __init__(self, css_str):
		self.strings = css_str.strip()
	def get_css_obj(self):
		length = len(self.strings)
		string = self.string
		brace_stack=[];
		
		state = {
			collector:'',
			state:'1'
		}
		obj = {
			selector:'',

			# child
		}
		for index in range(0,length):
			if string[index]=='{' and state['state']==1:
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