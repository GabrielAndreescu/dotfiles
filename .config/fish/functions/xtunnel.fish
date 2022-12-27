# simple function to open a xdebug:9003 tunnel via ssh
function xtunnel
    ssh -R 9003:localhost:9003 $argv
end

