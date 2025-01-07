# jinja2-mermaid-extension

[![Release](https://img.shields.io/github/v/release/AdamGagorik/jinja2-mermaid-extension)](https://img.shields.io/github/v/release/AdamGagorik/jinja2-mermaid-extension)
[![Build status](https://img.shields.io/github/actions/workflow/status/AdamGagorik/jinja2-mermaid-extension/main.yml?branch=main)](https://github.com/AdamGagorik/jinja2-mermaid-extension/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/AdamGagorik/jinja2-mermaid-extension/branch/main/graph/badge.svg)](https://codecov.io/gh/AdamGagorik/jinja2-mermaid-extension)
[![Commit activity](https://img.shields.io/github/commit-activity/m/AdamGagorik/jinja2-mermaid-extension)](https://img.shields.io/github/commit-activity/m/AdamGagorik/jinja2-mermaid-extension)
[![License](https://img.shields.io/github/license/AdamGagorik/jinja2-mermaid-extension)](https://img.shields.io/github/license/AdamGagorik/jinja2-mermaid-extension)

A jinja2 block to render a mermaid or tikz diagram.

1. Mermaid diagrams are rendered using the `mermaid-cli` tool in a `Docker` container.
2. TikZ diagrams are rendered using the `tectonic` tool on your host machine.
3. The diagram is saved to the current directory or `mermaid_output_root` or `tikz_output_root` (if defined).
4. The block is then replaced with a configurable string (markdown, etc).

## Setup

- `Docker` must be installed to run the `mermaid` command line tool.
- The extension should be installed in your `Python` environment.
- `tectonic` must be installed to render `tikz` diagrams.

```bash
pip install jinja2-mermaid-extension
```

- The extension should be added to the `jinja2` environment.

```python
from jinja2 import Environment
from jinja2_mermaid_extension import MermaidExtension

env = Environment(extensions=[MermaidExtension])
```

- You should pass the `mermaid_output_root` to the render method.

```python
out_path = Path().cwd() / "example.md"
template = env.get_template("example.md.jinja2")
rendered = template.render(mermaid_input_root=Path.cwd(), mermaid_output_root=out_path.parent)
out_path.write_text(rendered)
```

## Usage : mermaid

The following `jinaj2` block will render a mermaid diagram.

```jinja2
{% mermaid -%}
ext: .png
name: test
mode: myst
scale: 3
width: 75
align: center
caption: |
    An example mermaid diagram!
diagram: |
    graph TD
        A --> B
        B --> C
        A --> C
{% endmermaid %}
```

The output will be replaced with a `MyST` formatted markdown image.

```markdown
:::{figure} test.png
:align: center
:witdh: 75

An example mermaid diagram!
:::
```

The following arguments are available:

| Argument                   | Kind               | Description                                                                         | Default                |
| -------------------------- | ------------------ | ----------------------------------------------------------------------------------- | ---------------------- |
| **diagram** or **inp**     | Input              | The raw mermaid diagram code or the path to an `mmd` file.                          | `None`                 |
| **ext**                    | Output             | The file extension of the generated diagram.                                        | `".png"`               |
| **mode**                   | Replacement Option | How to render the output after processing.                                          | `"path"`               |
| **alt_text**               | Replacement Option | The alt text of the diagram.                                                        | `None`                 |
| **align**                  | Replacement Option | The alignment of the diagram only valid for MyST output)                            | `"center"`             |
| **caption**                | Replacement Option | A caption to add to the diagram only valid for MyST output).                        | `None`                 |
| **just_name**              | Replacement Option | Whether to only output the name of the generated diagram.                           | `False`                |
| **full_path**              | Replacement Option | Whether to output the full path of the generated diagram.                           | `False`                |
| **use_cached**             | Processing Option  | Whether to use a cached version of the diagram.                                     | `True`                 |
| **parallel**               | Processing Option  | Whether to render the diagram in parallel.                                          | `False`                |
| **temp_dir**               | Processing Option  | A temporary directory to use for intermediate files.                                | `None`                 |
| **delete_temp_dir**        | Processing Option  | Whether to delete the temporary directory after execution.                          | `True`                 |
| **mermaid_docker_image**   | Processing Option  | The docker image containing the mermaid-cli tool.                                   | `"minlag/mermaid-cli"` |
| **mermaid_volume_mount**   | Processing Option  | The directory in the docker container to mount the temporary directory to.          | `"/data"`              |
| **use_local_mmdc_instead** | Processing Option  | Whether to use the docker image or a locally installed mermaid-cli tool named mmdc. | `False`                |

The following mermaid specific arguments are available:

| Argument       | Kind               | Description                                    | Default     |
| -------------- | ------------------ | ---------------------------------------------- | ----------- |
| **theme**      | Mermaid CLI Option | The theme to use for the diagram.              | `"default"` |
| **scale**      | Mermaid CLI Option | A scaling factor for the diagram.              | `3`         |
| **width**      | Mermaid CLI Option | The width of the diagram in pixels.            | `800 `      |
| **height**     | Mermaid CLI Option | The height of the diagram in pixels.           | `None`      |
| **background** | Mermaid CLI Option | The background color of the generated diagram. | `"white"`   |

The block will be replaced by a string based on the `mode` argument.

- `path`: Output the path to the generated image.
- `markdown`: Output a simple markdown image link.
- `restructured`: Output a restructured text image link.
- `myst_markdown`: Output a MyST formatted markdown image.

For example, when using `mode: markdown`, the example above will be replaced with:

```markdown
![An example mermaid diagram!](./test.png)
```

## Usage : tikz

The following `jinaj2` block will render a `tikz` diagram (any LaTeX document really).

```jinja2
{% tikz -%}
ext: .pdf
name: test
mode: path
diagram: |
    \documentclass[margin=0pt]{standalone}
    \usepackage{tikz}
    \begin{document}
    \begin{tikzpicture}[remember picture]
    \coordinate (SE) at (0,0) {};
    \coordinate (NW) at (5,5) {};
    \draw (SE) rectangle (NW);
    \node[draw, rectangle, anchor=south west] at (SE) {SE};
    \node[draw, rectangle, anchor=north east] at (NW) {NW};
    \end{tikzpicture}
    \end{document}
{% endtikz %}
```

The following tikz specific arguments are available:

| Argument                    | Kind        | Description                                        | Default                                |
| --------------------------- | ----------- | -------------------------------------------------- | -------------------------------------- |
| **allow_missing**           | TikZ Option | Allow commands to be missing?                      | `False`                                |
| **latex_command**           | TikZ Option | The command to use to compile tikz diagrams.       | `"tectonic {inp_tex}"`                 |
| **pdf2svg_command**         | TikZ Option | The command to use to convert pdf to svg diagrams. | `"pdf2svg {inp_pdf} {out_svg}"`        |
| **convert_command**         | TikZ Option | The command to use to convert pdf to png diagrams. | `"magick convert {inp_pdf} {out_png}"` |
| **convert_command_density** | TikZ Option | The density of the png diagram.                    | `300`                                  |
| **packages**                | TikZ Option | The LaTeX package to use for the diagram.          | `(xcolor, tikz)`                       |
| **preamble**                | TikZ Option | The LaTeX preable to use for the diagram.          | ``                                     |
| **libraries**               | TikZ Option | The TikZ libraries to use for the diagram.         | `(shapes, arrows, etc)`                |
| **tikz_options**            | TikZ Option | The TikZ picture options to use for the diagram.   | `(scale=1, remember picture)`          |

---

- **Github repository**: <https://github.com/AdamGagorik/jinja2-mermaid-extension/>
- **Documentation** <https://AdamGagorik.github.io/jinja2-mermaid-extension/>
