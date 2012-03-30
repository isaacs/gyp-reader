{
  '//': 'This is a comment!',
  'variables': {
    'v8_use_snapshot%': 'true',
    # Turn off -Werror in V8
    # See http://codereview.chromium.org/8159015
    'werror': '',
    'node_use_dtrace': 'false',
    'node_shared_v8%': 'false',
    'node_shared_zlib%': 'false',
    'node_use_openssl%': 'true',
    'node_use_system_openssl%': 'false',
    'library_files': [
      'src/node.js',
      'lib/_debugger.js',
      'lib/_linklist.js',
      'lib/assert.js',
      'lib/buffer.js',
      'lib/buffer_ieee754.js',
      'lib/child_process.js',
      'lib/console.js',
      'lib/constants.js',
      'lib/crypto.js',
      'lib/cluster.js',
      'lib/dgram.js',
      'lib/dns.js',
      'lib/events.js',
      'lib/freelist.js',
      'lib/fs.js',
      'lib/http.js',
      'lib/https.js',
      'lib/module.js',
      'lib/net.js',
      'lib/os.js',
      'lib/path.js',
      'lib/punycode.js',
      'lib/querystring.js',
      'lib/readline.js',
      'lib/repl.js',
      'lib/stream.js',
      'lib/string_decoder.js',
      'lib/sys.js',
      'lib/timers.js',
      'lib/tls.js',
      'lib/tty.js',
      'lib/url.js',
      'lib/util.js',
      'lib/vm.js',
      'lib/zlib.js',
    ],
  },

  'targets': [
    {
      'target_name': 'node',
      'type': 'executable',

      'dependencies': [
        'deps/http_parser/http_parser.gyp:http_parser',
        'deps/uv/uv.gyp:uv',
        'node_js2c#host',
      ],

      'include_dirs': [
        'src',
        'deps/uv/src/ares',
        '<(SHARED_INTERMEDIATE_DIR)' # for node_natives.h
      ],

      'sources': [
        'src/fs_event_wrap.cc',
        'src/cares_wrap.cc',
        'src/handle_wrap.cc',
        'src/node.cc',
        'src/node_buffer.cc',
        'src/node_constants.cc',
        'src/node_extensions.cc',
        'src/node_file.cc',
        'src/node_http_parser.cc',
        'src/node_javascript.cc',
        'src/node_main.cc',
        'src/node_os.cc',
        'src/node_script.cc',
        'src/node_string.cc',
        'src/node_zlib.cc',
        'src/pipe_wrap.cc',
        'src/stream_wrap.cc',
        'src/tcp_wrap.cc',
        'src/timer_wrap.cc',
        'src/tty_wrap.cc',
        'src/process_wrap.cc',
        'src/v8_typed_array.cc',
        'src/udp_wrap.cc',
        # headers to make for a more pleasant IDE experience
        'src/handle_wrap.h',
        'src/node.h',
        'src/node_buffer.h',
        'src/node_constants.h',
        'src/node_crypto.h',
        'src/node_extensions.h',
        'src/node_file.h',
        'src/node_http_parser.h',
        'src/node_javascript.h',
        'src/node_os.h',
        'src/node_root_certs.h',
        'src/node_script.h',
        'src/node_string.h',
        'src/node_version.h',
        'src/pipe_wrap.h',
        'src/req_wrap.h',
        'src/stream_wrap.h',
        'src/v8_typed_array.h',
        'deps/http_parser/http_parser.h',
        '<(SHARED_INTERMEDIATE_DIR)/node_natives.h',
        # javascript files to make for an even more pleasant IDE experience
        '<@(library_files)',
        # node.gyp is added to the project by default.
        'common.gypi',
      ],

      'defines': [
        'NODE_WANT_INTERNALS=1',
        'ARCH="<(target_arch)"',
        'PLATFORM="<(OS)"',
      ],

      'conditions': [
        [ 'node_use_openssl=="true"', {
          'defines': [ 'HAVE_OPENSSL=1' ],
          'sources': [ 'src/node_crypto.cc' ],
          'conditions': [
            [ 'node_use_system_openssl=="false"', {
              'dependencies': [ './deps/openssl/openssl.gyp:openssl' ],
            }]]
        }, {
          'defines': [ 'HAVE_OPENSSL=0' ]
        }],

        [ 'node_use_dtrace=="true"', {
          'sources': [
            'src/node_dtrace.cc',
            'src/node_dtrace.h',
            # why does node_provider.h get generated into src and not
            # SHARED_INTERMEDIATE_DIR?
            'src/node_provider.h',
          ],
        }],

        [ 'node_shared_v8=="true"', {
          'sources': [
            '<(node_shared_v8_includes)/v8.h',
            '<(node_shared_v8_includes)/v8-debug.h',
          ],
        }, {
          'sources': [
            'deps/v8/include/v8.h',
            'deps/v8/include/v8-debug.h',
          ],
          'dependencies': [ 'deps/v8/tools/gyp/v8.gyp:v8' ],
        }],

        [ 'node_shared_zlib=="false"', {
          'dependencies': [ 'deps/zlib/zlib.gyp:zlib' ],
        }],

        [ 'OS=="win"', {
          'sources': [
            'tools/msvs/res/node.rc',
          ],
          'defines': [
            'FD_SETSIZE=1024',
            # we need to use node's preferred "win32" rather than gyp's preferred "win"
            'PLATFORM="win32"',
            '_UNICODE=1',
          ],
          'libraries': [ '-lpsapi.lib' ]
        },{ # POSIX
          'defines': [ '__POSIX__' ],
          'sources': [
            'src/node_signal_watcher.cc',
            'src/node_stat_watcher.cc',
            'src/node_io_watcher.cc',
          ]
        }],
        [ 'OS=="mac"', {
          'libraries': [ '-framework Carbon' ],
          'defines!': [
            'PLATFORM="mac"',
          ],
          'defines': [
            # we need to use node's preferred "darwin" rather than gyp's preferred "mac"
            'PLATFORM="darwin"',
          ],
        }],
        [ 'OS=="freebsd"', {
          'libraries': [
            '-lutil',
            '-lkvm',
          ],
        }],
        [ 'OS=="solaris"', {
          'libraries': [
            '-lkstat',
          ],
        }],
      ],
      'msvs-settings': {
        'VCLinkerTool': {
          'SubSystem': 1, # /subsystem:console
        },
      },
    },

    {
      'target_name': 'node_js2c',
      'type': 'none',
      'toolsets': ['host'],
      'actions': [
        {
          'action_name': 'node_js2c',

          'inputs': [
            '<@(library_files)',
            './config.gypi',
          ],

          'outputs': [
            '<(SHARED_INTERMEDIATE_DIR)/node_natives.h',
          ],

          # FIXME can the following conditions be shorted by just setting
          # macros.py into some variable which then gets included in the
          # action?

          'conditions': [
            [ 'node_use_dtrace=="true"', {
              'action': [
                'python',
                'tools/js2c.py',
                '<@(_outputs)',
                '<@(_inputs)',
              ],
            }, { # No Dtrace
              'action': [
                'python',
                'tools/js2c.py',
                '<@(_outputs)',
                '<@(_inputs)',
                'src/macros.py'
              ],
            }]
          ],
        },
      ],
    }, # end node_js2c
  ] # end targets
}

