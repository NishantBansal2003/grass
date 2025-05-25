## DESCRIPTION

*r.what.color* outputs the color associated with user-specified category
values in a raster input map.

Values may be specified either using the **value=** option, or by
specifying the **-i** flag and passing the values on `stdin`, one per
line.

For each specified value, an output will be generated consisting of the
category value along with the color, e.g.:

```sh
# Print color associated with user-specified category value in plain format:
r.what.color input=elevation.dem value=1500
1500: 223:127:31

# Print color associated with user-specified category value in JSON format using the triplet color format:
r.what.color input=elevation.dem value=1500 output_format=json color_format=triplet
[
    {
        "value": 1500,
        "color": "223:127:31"
    }
]
```

Similarly, other `color_format` options available with `output_format=json` are
`hex`, `hsv`, `triplet`, and `rgb`, with `hex` being the default color format
for JSON output.

If the input map is an integer (CELL) map, the category will be written
as an integer (no decimal point), otherwise it will be written in
floating point format (*printf("%.15g")* format).

If the lookup fails for a value, the color will be output as an
asterisk, e.g.:

```sh
# In plain format:
r.what.color input=elevation.dem value=9999
9999: *

# In JSON format:
r.what.color input=elevation.dem value=9999 output_format=json
[
    {
        "value": 9999,
        "color": "*"
    }
]
```

If a value cannot be parsed, both the value and the color will be output
as an asterisk, e.g.:

```sh
# In plain format:
r.what.color input=elevation.dem value=bogus
*: *

# In JSON format:
r.what.color input=elevation.dem value=bogus output_format=json
[
    {
        "value": "*",
        "color": "*"
    }
]
```

The format can be changed using the **format=** option (not applicable when
`output_format=json` is used). The value should be a *printf()*-style format
string containing three conversion specifiers for the red, green and blue
values respectively, e.g.:

```sh
r.what.color input=elevation.dem value=1500 format='%02x:%02x:%02x'
1500: df:7f:1f
```

If your system supports the *%m\$* syntax, you can change the ordering
of the components, e.g.:

```sh
r.what.color input=elevation.dem value=1500 format='%3$02x:%2$02x:%1$02x'
1500: 1f:7f:df
```

Common formats:  

- Tcl/Tk: `format="#%02x%02x%02x"`
- WxPython: `format='"#%02x%02x%02x"'` or `format='"(%d,%d,%d)"'`

## Using r.what.color JSON output with python

Print color associated with user-specified category value in JSON format using
Python:

```python
import grass.script as gs
import json

# Run the r.what.color command with rgb option for JSON output format
items = gs.read_command(
    "r.what.color",
    input="elevation",
    value=[100, 135, 156],
    output_format="json",
    color_format="rgb",
)

items = json.loads(items)
for item in items:
    print(f"{item['value']}: {item['color']}")
```

```sh
100: rgb(255, 229, 0)
135: rgb(195, 127, 59)
156: rgb(23, 22, 21)
```

## SEE ALSO

*[r.what](r.what.md)*

## AUTHOR

Glynn Clements
