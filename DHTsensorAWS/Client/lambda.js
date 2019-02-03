//Include AWS SDK
var AWS = require("aws-sdk");

//URL for SQS Queue
var QUEUE_URL1 = queue_url;

//Creating instance of the queue
var sqs = new AWS.SQS();


var maxTemp = 0;
var minTemp = 0;
var maxHum = 0;
var minHum = 0;
var avgTemp = 0;
var avgHum = 0;
var sampleCount = 0;



exports.handler = function(event, context) {
    //Logging the data for the event
    console.log('timestamp =', event.timestamp);
    console.log('temperature =', event.temperature);
    console.log('humidity =', event.humidity); 
    
    //calculating average temperature
    avgTemp = ((parseFloat(avgTemp)*sampleCount)+parseFloat(event.temperature))/(sampleCount+1);
    avgTemp = avgTemp.toFixed(2);
    console.log("avg Temp ",avgTemp);
    
    //calculating average humidity
    avgHum = ((parseFloat(avgHum)*sampleCount)+parseFloat(event.humidity))/(sampleCount+1);
    avgHum = avgHum.toFixed(2);
    console.log("avg Hum ",avgHum);
    
    //calculating maximum temperature
    maxTemp = Math.max(event.temperature,maxTemp);
    
    //calculating minimum temperature
    minTemp = Math.min(event.temperature,minTemp);
    
    //calculating maximum humidity
    maxHum = Math.max(event.humidity,maxHum);
        
    //calculating maximum humidity
    minHum = Math.min(event.humidity,minHum);
    
  
    if(sampleCount==0){
        minTemp = event.temperature;  
        minHum = event.humidity;
    }
    
    sampleCount = sampleCount+1;
    
    //Parameter to add to queue
    var sendParams = {
        MessageBody: event.timestamp + "," + event.temperature + "," +avgTemp+ "," +maxTemp+ "," +minTemp+ "," +event.humidity+ "," +avgHum+ "," +maxHum+ "," +minHum,
        MessageGroupId: 'sensordata',
        QueueUrl: QUEUE_URL1
    };
    
    //Adding message to the queue
    sqs.sendMessage(sendParams, function(err,data){
        if(err) {
            console.log("Error in SendMessage to 1st Queue");
            context.done('error', "ERROR Put SQS");  // ERROR with message
        }else{
            console.log("Message Sent to 1st Queue");
            context.done(null,'');  // SUCCESS
        }
    });
}; 
