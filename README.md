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


RUNNING THE INDICATOR DIRECTLY
------------------------------
You can clone the git repo thusly:

    $ git clone git://github.com/keithfancher/Todo-Indicator.git

Then just run the `todo_indicator.py` script within that directory:

    $ ./todo_indicator.py ~/todo.txt


INSTALLING THE SCRIPT WITH PIP
------------------------------
You can also install with pip:

    $ sudo pip install https://github.com/keithfancher/Todo-Indicator/tarball/master

This will install the required files in the default prefix (usually
`/usr/local/lib` and `/usr/local/bin`). You should then find the
`todo_indicator.py` script in your path, and can run it like so:

    $ todo_indicator.py ~/todo.txt

Note that pip doesn't (and can't) know about the python-gi requirement, so you
may have to install that one by hand if your distro doesn't have you covered:

    $ sudo apt-get install python-gi


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
on? Well, the best way to do that isn't with some silly indicator -- it's with
your trusty text editor! That's the whole beauty of the todo.txt system.

Click "Edit todo.txt" and your todo list will pop open in your text editor of
choice. (Or your OS's text editor of choice, at least -- it uses `xdg-open`.)
Once you've made your changes and saved the file, you should see your updates
automatically reflected in `todo_indicator.py`. (Thanks, inotify!)

If for some reason the indicator doesn't update properly, try (sternly)
clicking "Refresh".


BUT I HATE MY OS'S TEXT EDITOR OF CHOICE!
-----------------------------------------
I'm sorry! In that case, pass your favorite editor to `todo_indicator.py` on the
command line, like so:

    $ ./todo_indicator.py -e gvim ~/todo.txt


WHAT ELSE?
----------
That's all! Enjoy.
