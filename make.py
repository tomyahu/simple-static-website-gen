import os, shutil
import sass

pags_path = 'pags'
css_path = 'css'
out_path = 'out'

ignore = set()
ignore.add("guestbook.php")
ignore.add("head.html")
ignore.add("foot.html")


# manage out dir
try:
	os.mkdir( out_path )

except FileExistsError:
	print( 'out directory already exists' )


def addPages( pags_path, out_path ):
	# get head and foot
	print(pags_path)
	head = open( pags_path + '/head.html', 'r', encoding="utf8" )
	foot = open( pags_path + '/foot.html', 'r', encoding="utf8" )

	head_str = head.read()
	foot_str = foot.read()

	head.close()
	foot.close()

	for filename in os.listdir( pags_path ):
		if( filename in ignore ):
			continue
		
		if os.path.isdir(pags_path + '/' + filename):
			print("dir", filename)
			new_out_path = out_path + '/' + filename
			try:
				os.mkdir( new_out_path )

			except FileExistsError:
				print( new_out_path + ' directory already exists' )
			
			addPages( pags_path + '/' + filename, new_out_path )
			
			continue

		print(filename)
		file_template = open( pags_path + '/' + filename, 'r', encoding="utf8" )
		file_content = head_str + '\n' + file_template.read() + '\n' + foot_str
		file_template.close()

		file_out = open( out_path + '/' + filename, 'w', encoding="utf8" )
		file_out.write( file_content )
		file_out.close()

# add pages
addPages( pags_path, out_path )

# css
out_css_path = out_path + '/' + 'css'
for filename in os.listdir( css_path ):
	print(filename)

	sass_file = open( css_path + '/' + filename, 'r' )
	file_content = sass_file.read()
	sass_file.close()

	filename = filename.replace( '.scss', '.css' )

	file_out = open( out_css_path + '/' + filename, 'w' )
	file_out.write( sass.compile( string = file_content ) )
	file_out.close()
