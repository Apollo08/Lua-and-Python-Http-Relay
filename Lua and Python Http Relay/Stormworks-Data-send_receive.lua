local last_result = 0
local last_error = 0

function onTick()
    local in1 = input.getNumber(1)
    local send = input.getBool(1)
    if send then
        async.httpGet(5000, "/" .. tostring(in1))
        last_error = 4001 -- Send triggered
    else
        async.httpGet(5000, "/")
    end
    output.setNumber(1, last_result)
    output.setNumber(2, last_error)
end

function httpReply(port, request_body, response_body)
    if port == 5000 then
        -- Simulate HTTP error subcodes (Stormworks doesn't provide status, so you may need to infer)
        if response_body == nil then
            last_error = 1001 -- Timeout or no response
            return
        elseif response_body == "" then
            last_error = 3 -- Empty response
            return
        end
        -- Remove all characters except digits, minus, and dot
        local clean = string.gsub(response_body, "[^%d%.%-]", "")
        local num = tonumber(clean)
        if num then
            last_result = num
            last_error = 0 -- OK
            if string.sub(request_body, 1, 1) == "/" and #request_body > 1 then
                last_error = 4002 -- Send success
            end
        else
            last_error = 2 -- Invalid number
            if string.sub(request_body, 1, 1) == "/" and #request_body > 1 then
                last_error = 4003 -- Send failed (invalid number in response)
            end
        end
    end
end