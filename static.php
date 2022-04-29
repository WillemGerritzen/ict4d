<?php
header("Content-type: text/xml");
ehco("<?xml version=\"1.0\"?>\n");

 
$weather .= " The temperature is 20 degrees Fahrenheit.";

?>

<vxml version="2.0">
	<form>
    	<block>
      		<var name="myweather" expr="'<?php echo($weather)?>'"/>
      		<return namelist="myweather"/>
    	</block>
 	</form>
</vxml>


