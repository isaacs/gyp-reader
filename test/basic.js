var tap = require("tap")
var gr = require("../")

tap.test("basic test", function (t) {
  gr(__dirname + "/node.gyp", function (er, gypData) {
    t.ifError(er)
    t.ok(gypData)
    t.type(gypData, "object")
    if (er) return t.end()

    require("fs").readFile(__dirname + "/node.json", function (er, json) {
      t.ifError(er)
      if (er) return t.end()

      var jsonData = JSON.parse(json)
      t.deepEqual(jsonData, gypData)
      t.end()
    })
  })
})
