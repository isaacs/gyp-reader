This is a module for reading gyp files in node.

Gyp files are Python literals.  When the happy day comes that a build
system uses JSON like the gods intended, awful kludgey modules like this
one won't be necessary.

Python must be installed to use this.  If you point the `PYTHON` environ
to something different, it'll use that instead.

## Usage

```javascript
var gr = require("gyp-reader")
gr("binding.gyp", function (er, data) {
  // data is an object
})
```

## Warning

The gyp file is evaled in a python subprocess.  Do not run this on gyp
files that you are not sure of.  This module should only be used if
you're probably going to run `gyp` on them anyway, and presumably
they're trustworthy.

## Thanks

Trent Mick (@trentm) wrote the python for this module.
