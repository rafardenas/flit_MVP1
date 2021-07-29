
function Trial() {
    var data_json = JSON.stringify({'trial':'trial'});
    $.ajax({
        url: "/API_FB_login",
        type: "POST",
        data: data_json,
        dataType: "json"
    })
}
