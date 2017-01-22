import jsbeautifier
options = jsbeautifier.default_options()
options.indent_size = 4
options.indent_char = ' '
options.preserve_newlines = True
options.jslint_happy = False
options.keep_array_indentation = False
options.brace_style = 'collapse'
options.indent_level = 0
print jsbeautifier.beautify('    var foo = function(){ bar() }();   ', options)