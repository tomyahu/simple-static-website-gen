# Simple Static Website Generator

I was just looking for a simple thing that would let me import html files from within html files.
Couldn't find anything I was satisfied with, so I made it myself.

## Installation

This software was made and tested using python 3.9.2, but it should also work with python 3.7 - 3.11

Clone the repository, and install its dependencies with:
```
$ pip install -r requirements.txt
```

That's it!

# How to use this

To create an empty project first do 
```
$ python make.py
```

This should create the following folders:
* A `src` folder with two folders inside:
	* A `pags` folder to put your `html` files in
	* A `css` folder to put your `css` files in
* An `out` folder, where the final website will be exported

The `src` folder is where all your code should go, and after you're done editing, run `make.py` again to generate the website in the `out` folder.
This process only affects the files you created in the `src` folder.
This means that if you create additional files and folders in the `out` folder, these will not be deleted or affected, unless a file from the `src` folder has the same name, in which case it would replace it.

Also, inside the `src/pags` folder you can create subfolders with `html` files.
This directory structure will be preserved when generating the website in the `out` folder.

## Features

### Imports

The reason I made this in the first place.
You can paste contents from another html file in your current html file.
This is great for making websites with consistent layouts or reusable html stuff you want to put in many pages.

All you need to do to harness this power is to make a comment in your html file like this one:
```
<!-- import hello.html -->
```

This will copy the contents of the hello.html from the same directory of your current html file.
You can also access html files in other directories like this:

```
<!-- import ../file_from_upper_directory.html -->
```

And that's all, an example of how I use this in my website is I have a `_head.html` that imports all the css and navigation bar, and a `_foot.html` that imports the footer.
So when I want to make a new page, the code looks like this:

```
<!-- import _head.html -->

<h1>Hiya!<h1>

<!-- import _foot.html -->
```

Also, if your html files in the `src/pags` folder has an underscore `_` at the beginning, it will not be copied to the out directory.
This is so you don't have a random `_head.html` file that is broken by itself in your final website.

###  css and lesscss support

In the `src/css` folder is where you put your css files, and these will be copied to a css folder inside the `out` directory.
You can also write your stylesheets in `.less` files and the project will parse them to `css` files when generating the website.
It uses [lesscpy](https://github.com/lesscpy/lesscpy) to parse the files, which doesn't support every feature of the `less` format.

I also added an extra feature to the parsing process.
If you create a string in your `.less` file like this
```
"~sample sequence of characters"
```

After the parsing process, it will be replaced with this
```
sample sequence of characters
```

I use this when using the `calc` css function, to preserve the calculation I'm making inside the function (`less` has trouble with the `-` character sometimes).
So yeah, you can do that if you want.
