#script (lua)
function matches(s, pattern)
    ss = s.string
    if ss == nil then
        ss = s.name
    end
    if ss:match(pattern.string) ~= nil then
        return 1
    else
        return 0
    end
end
#end.

