function sendvalueToPy (Thedata, month){
  var TheLabelValue = Thedata
  var TheMonth = month
  $.ajax({
    url: '/delete_item', // Flask route to handle deletion
    method: 'POST', // You can use POST or GET method as per your requirement
    data: { 
            labelValue: TheLabelValue,
            month : TheMonth
          }, // Pass the label value as data
    success: function(response) {
        console.log('Deleted item:', response); // Log the response from Flask
    },
    error: function(xhr, status, error) {
        console.error('Error:', error); // Log any errors
    }
});
}

function SendNewTaskToPy (NewTask, Month){
  var TheTask = NewTask
  var TheMonth = Month
  $.ajax({
    url: '/new_task',
    method: 'POST',
    data:{
      Task: TheTask,
      month: TheMonth
    },
  success: function(response) {
      console.log('Sended Item:', response); // Log the response from Flask
  },
  error: function(xhr, status, error) {
      console.error('Error:', error); // Log any errors
  }
  });
}


function deleteCheckedInputs() {
  var checkedInputs = $('input[type="checkbox"]:checked');
  // Loop through each checked checkbox
  checkedInputs.each(function() {
    var thelabel = $(this).closest('li').find('label#todo');
    var getLabelValue = thelabel.text();
    var month = document.getElementById('month').value;
    sendvalueToPy(getLabelValue, month);
      // Remove the input element
    $(this).closest('li').remove();
  });
}
