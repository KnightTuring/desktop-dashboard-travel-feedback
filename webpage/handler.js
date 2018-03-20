var URL='http://192.168.1.37:8000';

function cityClicked()
{
    var cityValue = document.getElementById("cityDropdownList");
    var strCity = cityValue.options[cityValue.selectedIndex].value;
    var serverStatus = document.getElementById("serverStatus");
    serverStatus.innerHTML = "Connecting..."
    $.ajax({
        url:(URL+'/init'),
        dataType: 'json',
        type:'get' ,
        success:function(response){
            console.log(response)
            resp = JSON.parse(JSON.stringify(response))
            console.log(resp['status'])
            if(resp['status'] == "OK")
            {
                console.log("OK INIT")
                serverStatus.innerHTML = "Connected."

            }
            else {
              console.log("Failed")
            }
        },
        error:function(response){
        }
    });

    var posCountDisplay = document.getElementById("positiveCountDisplay")
    posCountDisplay.innerHTML = 0

    $.ajax({
        url:(URL+'/get_positive_feed_count/'+strCity),
        dataType: 'json',
        type:'get' ,
        success:function(response){
            console.log(response)
            resp = JSON.parse(JSON.stringify(response))
            console.log(resp['count'])
            if(resp['status'] == "OK")
            {
                console.log("OK CITY POSITIVE FEED")
                posCountDisplay.innerHTML = resp['count']

            }
            else {
              console.log("Failed")
            }
        },
        error:function(response){
        }
    });

    var totalCountDisplay = document.getElementById("totalCountDisplay")
    totalCountDisplay.innerHTML = 0
    $.ajax({
        url:(URL+'/get_total_feed_count/'+strCity),
        dataType: 'json',
        type:'get' ,
        success:function(response){
            console.log(response)
            resp = JSON.parse(JSON.stringify(response))
            console.log(resp['count'])
            if(resp['status'] == "OK")
            {
                console.log("OK CITY TOTAL FEED")
                totalCountDisplay.innerHTML = resp['count']

            }
            else {
              console.log("Failed")
            }
        },
        error:function(response){
        }
    });

    var negCountDisplay = document.getElementById("negativeCountDisplay")
    negCountDisplay.innerHTML = 0
    $.ajax({
        url:(URL+'/get_negative_feed_count/'+strCity),
        dataType: 'json',
        type:'get' ,
        success:function(response){
            console.log(response)
            resp = JSON.parse(JSON.stringify(response))
            console.log(resp['count'])
            if(resp['status'] == "OK")
            {
                console.log("OK CITY NEGATIVE FEED")
                negCountDisplay.innerHTML = resp['count']

            }
            else {
              console.log("Failed")
            }
        },
        error:function(response){
        }
    });
}