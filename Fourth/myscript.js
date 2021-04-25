window.onload=function(){

    document.getElementById('buttonSet').addEventListener('click',function(){
   
    chrome.tabs.query({}, function(tabs) {
    for(var i = 0; i < tabs.length; i++) {
     chrome.tabs.sendMessage(tabs[i].id, {user :document.getElementById('username').value,
                                        pass :document.getElementById('pass').value}, function(response) {
           });
    }
    }); 
   
    });
   
    }