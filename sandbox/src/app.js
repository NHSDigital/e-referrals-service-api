const Hapi = require('@hapi/hapi')
const Path = require('path')
const Inert = require('@hapi/inert')
const process = require('process')
const routes = require('./routes')

/*
The purpose of this logic is to mirror the transformations the API proxy currently applies to responses.
This allows the sandbox to have the same behaviour locally.
*/
const addCommonHeaders = function (request, response) {
  // if a response doesn't include any headers provide an empty object to allow for the common headers to be appended.
  if (!response.headers) {
    response.headers = {}
  }

  // API proxy always adds x-correlation-id to responses.
  if (request.headers["x-correlation-id"]) {
    response.headers["X-Correlation-ID"] = request.headers["x-correlation-id"]
  }

  if (!request.path.includes("/ObjectStore")) {
    response.headers["X-Request-ID"] = '58621d65-d5ad-4c3a-959f-0438e355990e-1'
  }
}

const preResponse = function (request, h) {
  addCommonHeaders(request, request.response)
  return h.continue
}

const init = async () => {
  const server = Hapi.server({
    port: 9000,
    host: '0.0.0.0',
    routes: {
      cors: {
        origin: ["*"],
        headers: ['origin', 'x-requested-with', 'x-correlation-id', 'accept', 'content-type', 'nhsd-session-urid', 'nhsd-end-user-organisation-ods', 'nhsd-ers-business-function', 'authorization', 'nhsd-ers-comm-rule-org', 'nhsd-ers-file-name', 'nhsd-ers-referral-id', 'if-match', 'nhsd-ers-on-behalf-of-user-id'],
        exposedHeaders: ['x-correlation-id', 'x-request-id', 'content-type', 'Location', 'ETag', 'Content-Disposition', 'Content-Length', 'Cache-Control'],
        maxAge: 3628800,
        credentials: false
      }, // Won't run as Apigee hosted target without this
      files: {
        relativeTo: Path.join(__dirname, 'mocks'),
      },
    },
  });

  server.ext('onPreResponse', preResponse);

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
  console.log(err)
  process.exit(1)
})

init()
