# todo-indicator

An Ubuntu app indicator for [todo.txt](http://todotxt.org/)-style todo lists.

![todo-indicator indicating](https://raw.github.com/keithfancher/todo-indicator/master/todo-indicator-shot.png)


## Installation

Install `todo-indicator` with `pip`:

```bash
pip install todo-indicator
```

If you're using `pipx` (for example on Ubuntu 23.04 or greater), the simplest
option is to install with the `--system-site-packages` argument:

```bash
pipx install --system-site-packages todo-indicator
```

In either case, note that **todo-indicator has some system dependencies which
`pip` can't easily satisfy**. The following should ensure you have everything
you need:

```bash
sudo apt install python3-pyinotify python3-gi gir1.2-appindicator3-0.1
```

(The above is verified working on Ubuntu 20.04 and 22.04. I can't speak for
other versions or distros, but it will likely be something similar.)

If you prefer to run `todo-indicator` in a virtual env (or if you're required
to do so by `pipx`) and you do *not* want to use the `--system-site-packages`
option, you'll need to `pip install` (or `pipx inject`) the required
dependencies in your virtual env. Unfortunately, because of the `PyGObject`
dependency, there are some extra steps involved with this. For more details,
see the [Contributing](#contributing) section -- this is the same process
you'd go through for local development.

Note that you can also simply clone the repo and run the provided
`todo-indicator` binary directly, without installing it. You'll still need to
install the required dependencies as described above, however.


## Requirements

* Python 3
* The above-mentioned system dependencies
* An app-indicator-aware system tray of some kind (you might need a plugin if
  you're running a non-Ubuntu distro)


## Usage

Just run `todo-indicator`, passing the name of your `todo.txt` file as an
argument, e.g.:

```bash
todo-indicator ~/todo.txt
```

Click the indicator icon to see your list. If you finish one of your tasks,
give yourself a pat on the back and click it! It'll be marked "done."


### Editing your list

`todo-indicator`'s goal is to show you your list and let you check items off.
Anything more complex than that, you'll want to use your trusty text editor.

Click "Edit todo.txt" and your todo list will open in your text editor of
choice. (Or your OS's text editor of choice, at least -- it uses `xdg-open`.)
Once you've made your changes and saved the file, you should see your updates
automatically reflected in the `todo-indicator` UI. (Thanks, `inotify`!)

If for some reason the indicator doesn't update, click "Refresh".


### Command-line options

Use `-e`/`--editor` to specify a text editor other than your default:

```bash
todo-indicator -e gvim ~/todo.txt
```

`todo-indicator` assumes a dark-colored panel by default. If you use a
light-colored panel, you can pass the `-i`/`--invert` option to invert the
icon color:

```bash
todo-indicator -i ~/todo.txt
```


## Contributing

Check the `Makefile` for some common operations like code formatting, linting,
and running unit tests.

If you install/run `todo-indicator` inside a virtual env (usually recommended
for development), you'll need to install the dependencies from the
`requirements.txt` file:

```bash
pip install -r requirements.txt
```

This includes `PyGObject`, which itself needs some extra development
dependencies to be installed on your system. See [the PyGObject
docs](https://gnome.pages.gitlab.gnome.org/pygobject/getting_started.html#ubuntu-logo-ubuntu-debian-logo-debian)
for more info.

Alternatively, you can skip this step, install the "normal" system-level
dependencies from the [Installation](#installation) section, and create your
virtual env with the `--system-site-packages` option:

```bash
python -m venv --system-site-packages .venv
```

This will allow your local, virtual env version of `todo-indicator` to import
your system-level python libraries (in particular the `gi` package).
