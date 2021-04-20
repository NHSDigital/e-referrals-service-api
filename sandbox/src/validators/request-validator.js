
module.exports = {


    verifyContentTypeHeader: function (request, header) {
        return request.headers["content-type"] && (
            request.headers["content-type"].toLowerCase() === header 
        )
    },


    verifyRequestHasProperties: function(request, arr) {
        return request != null && request.payload != null &&  arr.every(item => request.payload.hasOwnProperty(item));
    }

    
}
