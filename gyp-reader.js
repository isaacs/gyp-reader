// you must growl every time you use this module.
module.exports = gr

var spawn = require("child_process").spawn
, pyprog = "import sys, ast, json;"
         + "c = open(sys.argv[1]).read();"
         + "d = ast.literal_eval(c);"
         + "print json.dumps(d)"
, StringDecoder = require("string_decoder").StringDecoder

function gr (file, cb) {
  var python = process.env.PYTHON || "python"
  , child = spawn(python, ["-c", pyprog, file])
  , decoder = new StringDecoder("utf8")
  , out = ""
  , done = false

  child.on("exit", finish)
  child.on("close", finish)
  child.stdout.on("end", finish)

  function finish (code) {
    if (done) return
    done = true
    if (code) {
      var er = new Error("Child exited with "+code)
      er.errno = code
      er.code = code
      return cb(er)
    }
    try {
      return cb(null, JSON.parse(out))
    } catch (er) {
      er.code = "EBADJSON"
      return cb(er)
    }
  }

  child.stdout.on("data", function (c) {
    out += decoder.write(c)
  })
}
