chrome.runtime.onMessage.addListener(function(request, sender,   sendResponse) { 
    //Take the fields of user and password from the DOM of facebook log-in page 
    document.getElementById('rcmloginuser').value=request.user;
    document.getElementById('rcmloginpwd').value=request.pass;
});