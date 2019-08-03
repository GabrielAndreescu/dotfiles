var noBorder = false;

var removeBorders = function(client) {
    if (client.caption.indexOf('Latte Dock') === -1) {
        client.noBorder = noBorder;
    }
}

registerShortcut('Workaholic: Toggle Borders', 'Workaholic: Toggle Borders', 'Meta+D', function() {
    workspace.activeClient.noBorder = !workspace.activeClient.noBorder;
    
    return 0;
});

registerShortcut('Workaholic: Toggle Borders All', 'Workaholic: Toggle Borders All', 'Meta+Shift+D', function() {
    noBorder = !noBorder;
    
    var clients = workspace.clientList();
    for (var i=0; i<clients.length; i++) {
        removeBorders(clients[i]);
    }
    
    return 0;
});
