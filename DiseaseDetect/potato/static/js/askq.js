function CheckForm() 
{
    textbox_data = $(".q-body-div iframe").contents().find("body").text();
    if (textbox_data === '')
    {
      swal("Error", "Question body cannot be empty", "error");
      return false;
    }
    else{
      return true
    }
}
