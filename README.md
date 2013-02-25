TODO INDICATOR
==============

An Ubuntu app indicator for todo.txt-style todo lists. More info about todo.txt
here: http://todotxt.com/

![Todo Indicator indicating](https://raw.github.com/keithfancher/Todo-Indicator/master/todo_indicator_shot.png)


REQUIREMENTS
------------
* python
* pyinotify
* argparse (standard with Python 2.7+)
* python-gi
* some kind of widget/tray/app/whatever that loves Ubuntu app indicators


INSTALLATION
------------
You can clone the git repo thusly:

    $ git clone git://github.com/keithfancher/Todo-Indicator.git

Then just copy the todo_indicator.py file somewhere in your path and run it!

You can also install with pip:

    $ pip install https://github.com/keithfancher/Todo-Indicator/tarball/master

Note that pip doesn't (and can't) know about the python-gi requirement, so you
may have to install that one by hand if your distro doesn't have you covered.


HOW DO I USE IT?
----------------
Just run it, passing the name of your todo.txt file as an argument, e.g.:

    $ ./todo_indicator.py ~/todo.txt

Click the indicator icon to check out your list of must-do-ables. If you finish
one of your tasks, give yourself a pat on the back and click it! It'll be
marked "done."


BUT I WANT MORE COMPLEX FUNCTIONALITY!
--------------------------------------
You mean you want to change priorities, add "contexts" and "projects," and so
on? Well, the best way to do that isn't with some silly little indicator --
it's with your trusty text editor! That's the whole beauty of the todo.txt
system.

Simply click the "Edit todo.txt" menu item and your todo list will pop open in
your text editor of choice. (Or your OS's text editor of choice, at least -- it
uses xdg-open.) Once you've made your changes and saved the file, you should
see your updates automatically reflected in todo_indicator. (Thanks, inotify!)
If for some reason the indicator doesn't update properly, try clicking the
"Refresh" menu item to hard refresh everything.


BUT I HATE MY OS'S TEXT EDITOR OF CHOICE!
-----------------------------------------
I'm sorry! In that case, pass your favorite editor to todo_indicator on the
command line, like so:

    $ ./todo_indicator.py -e gvim ~/todo.txt


WHAT ELSE?
----------
That's all! Enjoy.
