A function may not be bellow 2 rows, unless its a method.

A function may not be above 30 rows.

Any piece of code may not have indentations above 3.

```
0 indent
	1 indent
		2 indent
			3 indent!
				4 indent!!!
```

This is prevented with early returns and function simplification

A class may exist if and only if it stores at least 2 pieces of data.

If you cant come up with a rational, sane-sounding name for something, dont do it.

If you cant come up with a sane unit test for something, dont do it.

Where possible, functions with (important) side effects should not be parts of an expression. Or at least not a complex one.

Ex:
```
# Dont
if object.execute_child() == True:
	# stuff
-----------------------------------
# Do
success = object.execute_child()
if success:
	# stuff
```
