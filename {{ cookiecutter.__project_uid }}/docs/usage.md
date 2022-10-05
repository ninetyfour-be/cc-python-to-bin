# Usage

The binaries are relatively straightforward to use on all the target operating systems. Still, there are some specificities that are worse mentionning.

Before I talk about each platform separately, I would like to state that such single file executables can take some time on startup. Indeed, they are not *per se* single files, but rather compressed archives. Those archives are first uncompressed when you launch the program, this process is what takes some time.

{% if cookiecutter.windows -%}
## Windows

Using the Windows build is very easy. Simply place the `.exe` file somewhere on your computer and double click on it. If you want to make it even easier, you can create a shortcut to it on your desktop.

If you want to run it from the command line, you can either type the whole path to the `.exe` or add it to the path so you do not have to remember where it is.

{%- endif %}
{% if cookiecutter.macos -%}
## MacOS

The MacOS build contains two files. To install the application on your computer, simply drag and drop the `.app` file into your `Applications/` folder. This should make it available through the launcher. You can also double click on it to run the applicaion directly.

The second file is the bare executable. If you want to run your application from the terminal, you should consider adding the path to this file in your `PATH` environment variable.

{%- endif %}
{% if cookiecutter.linux -%}
## Linux

To install and use the application on Linux, you can simply double click on the executable. If you want to run it from the terminal, make sure to add it to your `PATH` environment variable.

If you want to make it available from the launcher, you can create a menu item pointing to it.

{%- endif %}