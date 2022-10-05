# Screenshots

Here are screenshots of your application in the different virtual machines used to build and test it.

{% if cookiecutter.windows -%}
## Windows

This is how you application looks on Windows 10.

```{eval-rst}
.. image:: static/img/windows.png
   :width: 400
   :align: center
```
{%- endif %}
{% if cookiecutter.macos -%}
## MacOS

This is how your application looks on MacOS *"Big Sur"*.

```{eval-rst}
.. image:: static/img/macos.png
   :width: 400
   :align: center
```
{%- endif %}
{% if cookiecutter.linux -%}
## Linux

This is how your application looks on Ubuntu *"Xenial"*.

```{eval-rst}
.. image:: static/img/linux.png
   :width: 400
   :align: center
```
{%- endif %}