request = function()
    headers = {}
    headers["Host"] = "localhost:8080"
    headers["Content-Type"] = "application/json"
    path = "/cart/"
    return wrk.format("POST", path, headers)
end