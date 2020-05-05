function CheckAnsForm() 
{
    textbox_data = $(".a-body-div iframe").contents().find("body").text();
    if (textbox_data === '')
    {
      swal("Error", "Answer body cannot be empty", "error");
      return false;
    }
    else{
      return true
    }
}


function getRandomColor() {

  var rcolor = ['#FF1744', '#C51162', '#D50000', '#D500F9', '#6200EA', '#304FFE', '#2979FF', '#00B0FF', '#18FFFF', '#1DE9B6', '#00E676', '#AEEA00', '#FFFF00', '#FF6D00', '#FF3D00'];
  var random = rcolor[Math.floor(Math.random() * rcolor.length)];    
  return random;

}


$('.answers').each(function (index, div) {
  $(div).css('border-left', '5px solid ' + getRandomColor());
});
