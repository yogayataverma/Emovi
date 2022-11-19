<html>
<head>

<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.12.9/dist/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>

<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.4/Chart.js"></script>
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>

</head>
<body>


<?php
    include("navbar.php");
?>


<?php
$file_count=0;
$filename1;
$j=0;
foreach (glob("*.txt") as $filename) { 
$filename1[$j] = str_replace("","","$filename");

echo $filename1[0];
$file_count++;
$j++;
}

?>

<?php

STATIC $k=0;
for($i=0 ; $i<$file_count ; $i++)
{

STATIC $happy=0;
STATIC $angry=0;
STATIC $fear=0;
STATIC $sad=0;
STATIC $surprise=0;
STATIC $neutral=0;
STATIC $disgust=0;
STATIC $count=0;

$file_handle = fopen( "$filename1[$k]", "r");

$k++;

while (!feof($file_handle) ) {

  $line_of_text = fgets($file_handle);
  $parts = explode(',', trim($line_of_text) );
  if (strcmp($parts[0], "Happy")==0)
      $Happy = trim($parts[1]);
  if (strcmp($parts[0], "Sad")==0)
     $Sad = trim($parts[1]);
  if (strcmp($parts[0], "Fear")==0)
     $Fear = trim($parts[1]);
  if (strcmp($parts[0], "Neutral")==0)
     $Neutral = trim($parts[1]);
  if (strcmp($parts[0], "Angry")==0)
     $Angry = trim($parts[1]);
  if (strcmp($parts[0], "Disgust")==0)
     $Disgust = trim($parts[1]);
  if (strcmp($parts[0], "Surprise")==0)
     $Surprise = trim($parts[1]);
}

foreach ($parts as $value) 
{
if($value =="Happy")
{
  $happy++;
}
else if($value =="Sad")
{
  $sad++;
}
else if($value =="Surprise")
{
  $surprise++;
}
else if($value =="Fear")
{
  $fear++;
}
else if($value =="Disgust")
{
 $disgust++;
}
else if($value =="Angry")
{
 $angry++;
}
else if($value =="Neutral")
{
 $neutral++;
}

}


foreach($parts as $v)
{
   $count++;
}

fclose($file_handle);

}
?>


<?php
echo "<div style='display:flex;'><p style='margin-top:5%;margin-left:35%' >Number Of Times The Student Showed Particular Emotion.</p>
</div>


<div style='display:flex;'>

<canvas id='myChart' style='width:100%;max-width:600px;max-length:50px;margin-left:29%'></canvas>

<script>
var yValues = [".$happy.", ".$surprise.", ".$disgust.", ".$sad.", ".$fear." , ".$neutral." , ".$angry."];
var xValues = ['Happy','Surprise','Disgust','Sad','Fear' , 'Neutral' , 'Angry'];
var barColors = [
  '#b91d47',
  '#00aba9',
  '#2b5797',
  '#e8c3b9',
  '#1e7145',
  '#8d6fd1',
  '#fe6db6'
];

new Chart('myChart', {
  type: 'pie',
  data: {
    labels: xValues,
    datasets: [{
      backgroundColor: barColors,
      data: yValues
    }]
  },
  options: {
    title: {
      display: true,
      text: 'Emotions'
    }
  }
});
</script>";

?>


</div>

</body>

</html>