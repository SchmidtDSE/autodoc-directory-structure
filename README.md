# autodoc-directory-structure

Generate an overview of a project's directory structure for inclusion in its docs.


## Install (for developers; this isn't packaged and published yet)

Clone this repository, then:

```bash
uv pip install --editable .
```

## Use

List this extension in your Sphinx configuration (`conf.py`):

```python
extensions = [
    # ...
    "autodoc_directory_structure",
]
```

Use the directive:

```rst
.. autodoc_directory_structure:: ../src
   :gitignore:
```
