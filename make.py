import os, sys, shutil
import re
import lesscpy
from six import StringIO
import lib
import markdown

called_path = os.getcwd()

pags_path = called_path +'/src/pags'
css_path = called_path +'/src/css'
out_path = called_path +'/out'

supported_extensions = set()
supported_extensions.add("html")
supported_extensions.add("php")
supported_extensions.add("md")

registries = dict()

parsed_contents = {}

if not os.path.isdir(called_path + '/src'):
	print("No project found, creating...")
	print(called_path + '/src')
	print(pags_path)
	print(css_path)
	print(out_path)
	os.mkdir(called_path + '/src')
	os.mkdir(pags_path)
	os.mkdir(css_path)
	os.mkdir(out_path)
	print("Project created")
	sys.exit(0)

if not os.path.isdir(pags_path):
	os.mkdir(pags_path)

if not os.path.isdir(css_path):
	os.mkdir(css_path)

if not os.path.isdir(out_path):
	os.mkdir(out_path)


# create pages

print("Generating Pages")
def makePage( base_dir, page_path ):
	full_path = lib.getAbsPath( base_dir + '/' + page_path )

	if full_path in parsed_contents.keys():
		return parsed_contents[full_path]
	
	file_template = open( full_path, 'r', encoding="utf8" )
	file_content = file_template.read()
	file_template.close()

	file_extension = page_path.split('.')[-1]
	if file_extension == "md":
		file_content = markdown.markdown(file_content)

	regex_prefix = r"(?:(?:{{)|(?:<!--)) *"
	regex_suffix = r" *(?:(?:-->)|(?:}}))"
	for func, val in re.findall( regex_prefix + r"(.*?) (.*?)" + regex_suffix, file_content ):
		replace_with = ""
		if func == "import":
			import_full_path = lib.getAbsPath( base_dir + '/' + val )
			replace_with = makePage( base_dir, val )
		
		if re.match( r"^s_(.*?)$", func ):
			varname = re.findall(r"^s_(.*?)$", func)[0]
			registries[varname] = val

		if re.match( r"^l_(.*?)$", func ):
			varname = re.findall(r"^l_(.*?)$", func)[0]
			if varname in registries:
				replace_with = registries[varname]

		file_content = re.sub(regex_prefix + func + r" " + re.escape(val) + regex_suffix, replace_with, file_content, count=1 )
	
	parsed_contents[ base_dir + '/' + page_path ] = file_content

	return file_content


def addPages( pags_path, out_path ):
	for filename in os.listdir( pags_path ):
		splitted_filename = filename.split('.')
		basename = splitted_filename[0]
		file_extension = splitted_filename[-1]

		if basename[0] == '_':
			continue

		elif( file_extension in supported_extensions ):
			print( pags_path + "/" + filename )
			file_content = makePage( pags_path, filename )
			if file_extension == "md":
				file_extension = "html"
			
			file_out = open( out_path + '/' + basename + "." + file_extension, 'w', encoding="utf8" )
			file_out.write( file_content )
			file_out.close()
		
		elif os.path.isdir(pags_path + '/' + filename):
			new_out_path = out_path + '/' + filename
			if not os.path.isdir(new_out_path):
				os.mkdir(new_out_path)
			
			addPages( pags_path + '/' + filename, new_out_path )
		
		elif( file_extension != "" ):
			print( pags_path + "/" + filename )
			shutil.copyfile(pags_path + "/" + filename, out_path + '/' + filename )


addPages( pags_path, out_path )



# css
def remove_borders(match_obj):
	return match_obj.group(2)

print("")
print("Generating CSS")
out_css_path = out_path + '/' + 'css'
for filename in os.listdir( css_path ):
	print(out_css_path + "/" + filename)

	style_file = open( css_path + '/' + filename, 'r' )

	splitted_filename = filename.split('.')
	basename = splitted_filename[0]
	file_extension = splitted_filename[-1]
	file_content = style_file.read()

	if file_extension == "less":
		file_content = lesscpy.compile( StringIO(file_content) )
		file_content = re.sub(r"(\"\~)(.*)(\")", remove_borders, file_content)
	
	style_file.close()

	file_out = open( out_css_path + '/' + basename + '.css', 'w' )
	file_out.write( file_content )
	file_out.close()
