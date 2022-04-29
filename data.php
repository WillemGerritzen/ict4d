<?php
header("Content-type: text/xml");
ehco("<?xml version=\"1.0\"?>\n");

if ($_GET['location']) {
         
    $urlContents = file_get_contents("https://api.openweathermap.org/data/2.5/weather?q=".urlencode($_GET['city'])."&appid=ab75fb5cfed8a375955e5dc6a951438c");
         
        $weatherArray = json_decode($urlContents, true);
         
        if ($weatherArray['cod'] == 200) {
         
            $weather = "The weather in ".$_GET['city']." is currently '".$weatherArray['weather'][0]['description']."'. ";
 
            $tempInCelcius = intval($weatherArray['main']['temp']);
 
            $weather .= " The temperature is ".$tempInCelcius."degrees Fahrenheit, the wind speed is ".$weatherArray['wind']['speed']."m/s, the air pressure is ".$weatherArray['main']['pressure']."hPa, and the humidity is ".$weatherArray['main']['humidity']."percent.";
             
        } else {
             
            $error = "Sorry, could not find city - please try again.";
             
        }     
    }
?>

<vxml version="2.0">
	<form>
    	<block>
      		<var name="myweather" expr="'<?php echo($weather)?>'"/>
      		<var name="err" expr="'<?php echo($error)?>'"/>
      		<return namelist="myweather err"/>
    	</block>
 	</form>
</vxml>


