chrome.runtime.onMessage.addListener(function(request, sender,   sendResponse) { 
    //Take the fields of user and password from the DOM of facebook log-in page 
    //console.log("HI");
    document.getElementsByClassName('form-control')[0].value=request.user;
    document.getElementsByClassName('form-control')[1].value=request.pass;
});