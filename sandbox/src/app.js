const Hapi = require('@hapi/hapi')
const Path = require('path')
const Inert = require('inert')
const process = require('process')
const routes = require('./routes')

const init = async () => {
  const server = Hapi.server({
    port: 9000,
    host: '0.0.0.0',
    routes: {
      cors: true, // Won't run as Apigee hosted target without this
      files: {
        relativeTo: Path.join(__dirname, 'mocks'),
      },
    },
  });

  server.route({
    method: '*',
    path: '/{any*}',
    handler: function (request, h) {
        const errorResponse = {
          error: 'File not found'
        }
        return h.response(errorResponse).code(404);
    }
  });

  // Binding some variables to allow for persistence on the server.
  server.bind({
    messages: {}
  })

  await server.register(Inert)
  server.route(routes)

  await server.start()
  console.log('Server running on %s', server.info.uri)
}

process.on('unhandledRejection', (err) => {
  console.log(err);
  process.exit(1);
})

init()
