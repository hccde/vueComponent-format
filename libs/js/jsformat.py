import jsbeautifier

#format js string 
class JsFormat:
    def __init__(self, js_str,settings):
        self.js_str = js_str
        options = jsbeautifier.default_options()
        options.indent_size = 4
        options.indent_char = ' '
        options.preserve_newlines = True
        options.jslint_happy = False
        options.keep_array_indentation = False
        options.brace_style = 'collapse'
        options.indent_level = 0
        self.options = options
        self.formated_str = self.format()
    def format(self):
        return jsbeautifier.beautify(self.js_str, self.options)
