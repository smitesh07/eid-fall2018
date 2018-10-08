//import libraries
var fs = require('fs');
var sensor = require('./node-dht-sensor/build/Release/node_dht_sensor');

//Sensor type and GPIO pin definition
var sensorType = 22;
var gpioPin = 4;

//Arrays for Temperature and Humidity values
var temp=[];
var hum=[];


var temp_avg = 0;	//temperature average
var hum_avg = 0;	//humidity average
var i=0;		//loop count

var iid = setInterval(function() 
  {
   sensor.read(sensorType, gpioPin, function(err, temperature, humidity) 
   {
    if(i<10)
    { 
   	if (err)
		{
		console.warn('' + err);
		}
	else
		{
		temperature = temperature*1.8 + 32;
		temp[i] = temperature.toFixed(1);
		hum[i] = humidity.toFixed(1);
		temp_avg=temp_avg + (Number.parseFloat(temperature)-temp_avg)/(i+1);
		hum_avg=hum_avg + (Number.parseFloat(humidity)-hum_avg)/(i+1);
    		console.log("%d - Temp %s degF,%s%% Hum",i+1,temp[i],hum[i]);
		i+=1;
		}
    }
    else 
    {
	console.log("Lowest Temp %d degF",Math.min(...temp));
	console.log("Lowest Hum %d%",Math.min(...hum));
	console.log("Highest Temp %d degF",Math.max(...temp));
	console.log("Highest Hum %d%",Math.max(...hum));
	console.log("Average Temp %d degF",temp_avg.toFixed(1));
	console.log("Average Hum %d%",hum_avg.toFixed(1));
	i=0;
	return;
    }
   });
 }, 1000);
