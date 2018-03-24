var URL='http://localhost:5000';
var valueOfNegCount;
var valueOfPosCount = 0;
var valueOfTotalCount = 0;
var strCity;
function cityClicked()
{
    var cityValue = document.getElementById("cityDropdownList");
    strCity = cityValue.options[cityValue.selectedIndex].value;
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
                serverStatus.innerHTML = "Connected to remote database"

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
                valueOfPosCount = resp['count']

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
                valueOfTotalCount = resp['count']
                console.log(valueOfTotalCount)

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
                valueOfNegCount = resp['count']

            }
            else {
              console.log("Failed")
            }
        },
        error:function(response){
        }
    });

    var dispAcc = document.getElementById("classifierAccuracy")
    $.ajax({
        url:(URL+'/get_classifier_accuracy'),
        dataType: 'json',
        type:'get' ,
        success:function(response){
            console.log(response)
            resp = JSON.parse(JSON.stringify(response))
            console.log(resp['count'])
            if(resp['status'] == "OK")
            {
                //console.log("OK CITY NEGATIVE FEED")
                var percent = resp['accuracy'] * 100;
                dispAcc.innerHTML = percent + '%'

            }
            else {
              console.log("Failed")
            }
        },
        error:function(response){
        }
    });


}

function displayChart() {
    var percentPositive = (valueOfPosCount/valueOfTotalCount) * 100;
    var percentNegative = (valueOfNegCount/valueOfTotalCount) * 100;
    var chart = new CanvasJS.Chart("chartContainer", {
	animationEnabled: true,
	title: {
		text: ""
	},
	data: [{
		type: "pie",
		startAngle: 240,
		yValueFormatString: "##0.00\"%\"",
		indexLabel: "{label} {y}",
		dataPoints: [
			{y: percentPositive, label: "Positive"},
			{y: percentNegative, label: "Negative"}
		]
	}]
    });
    chart.render();
}

function displayPositiveFeed()
{

    var userFeedbackList;
    var col = [];
    var displayData = document.getElementById("showData");
    var userFeed = ''
    $.ajax({
        url:(URL+'/get_positive_user_feed/'+strCity),
        dataType: 'json',
        type:'get' ,
        success:function(response){
            console.log(response)
            resp = JSON.parse(JSON.stringify(response))
            //console.log(resp['count'])
            if(resp['status'] == "OK")
            {
                //print user feedback

                for(var key in resp)
                {
                    console.log("Key is"+key);
                    if(resp[key]!='OK')
                    {
                        userFeed = userFeed + '<h5>' + key + '</h5>' + '<h6><i>' + resp[key] + '</i></h6>'
                    }

                }
                displayData.innerHTML = userFeed
            }
            else {
              console.log("Failed")
            }
        },
        error:function(response){
        }
    });

}