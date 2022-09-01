# Usage

The binaries are relatively straightforward to use on all the target operating systems. Still, there are some specificities that are worse mentionning.

Before I talk about each platform separately, I would like to state that such single file executables can take some time on startup. Indeed, they are not *per se* single files, but rather compressed archives. Those archives are first uncompressed when you launch the program, this process is what takes some time.

{% if cookiecutter.windows -%}
## Windows

### Creating a shortcut

### Adding the application to your PATH

{%- endif %}
{% if cookiecutter.macos -%}
## MacOS

{%- endif %}
{% if cookiecutter.linux -%}
## Linux

{%- endif %}