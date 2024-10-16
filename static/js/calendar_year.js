const next = document.getElementById('right');
const prev = document.getElementById('left');
const today = document.getElementById('today');
let events = [] //for storing the events that pass by py
let len //the number of the events
let EventDates = []
let EventMonth = []
let EventDate = []
//<i class="fa-solid fa-shield-heart"></i>//heart favicon 
let variant = 0;
next.addEventListener('click',function(event){
  variant +=1;
  updateCalendar(variant);
});
prev.addEventListener('click',function(event){
  variant -=1;
  updateCalendar(variant);
});
today.addEventListener('click',function(event){
  variant = 0;
  updateCalendar(variant);
});

async function SendDateToPy(Date){
  let date = Date;
  return new Promise((resolve, reject) => {
  $.ajax({
    url: '/toPy',
    method: 'POST',
    data:{
      Thedate: date,
    },
  success: function(response) {
    len = parseInt(response.data.len);
    if (!isNaN(len) && len !== 0){
      events = [];
      for(let i = 0; i < len; i++){
        events.push ({
          date: response.data.date[i],
          TheEvent: response.data.event[i],
          Category: response.data.category[i]
        });
      }
    }
    console.log('Sended Item:', response); // Log the response from Flask
    if (!isNaN(len) && len !== 0) {
      for (let k = 0; k < len; k++) {
          EventDates[k] = events[k].date;
          EventMonth[k] = EventDates[k].substring(5, 7);
          EventDate[k] = EventDates[k].substring(8, 10);
      }
      ThereIsEvent = true
    }else{
        ThereIsEvent = false
    }
    resolve(response);
  },
  message: function(response){
    console.log('message: ', response)
  },
  error: function(xhr, status, error) {
      console.error('Error:', error); // Log any errors
      reject(error);
    }
  });
}); 
}

async function updateCalendar(variant){ //using async to make sure it wait the ajax
  let ThereIsEvent = false //to check there is even in the year
    // Get the current date
  const currentDate = new Date();
  currentDate.setMonth(0, 1);
  let calendarHTML = '';
  //displaying the current year header
  const display = document.getElementById('timeh2');
  if (display){
    display.textContent = currentDate.getFullYear() + variant;
    var send = currentDate.getFullYear() + variant;
    let resp = await SendDateToPy(send);
  }
  if (len != 0 ){
    ThereIsEvent = true
    console.log(EventMonth);
  }

  // Define month names and day names
  const monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

  // Loop through 12 months
  for (let i = 0; i < 12; i++) {
    // Get the date for the current month
    const monthDate = new Date(currentDate.getFullYear() + variant, currentDate.getMonth()+i, 1);
    const month = monthDate.getMonth();
    // Start building the table header for the month
    calendarHTML += '<div class="month">';
    calendarHTML += '<table>';
    calendarHTML += `<tr><th colspan="7">${monthNames[month]}`;
    calendarHTML += `</th></tr>`;
    calendarHTML += '<tr>';

    // Add day names as table headers
    for (let j = 0; j < 7; j++) {
      calendarHTML += `<th class="day">${dayNames[j]}</th>`;
    }
    calendarHTML += '</tr><tr>';

    // Get the starting day of the week for the current month
    const startDay = monthDate.getDay();

    // Get the number of days in the current month
    const numDays = new Date(monthDate.getFullYear(), monthDate.getMonth() + 1, 0).getDate();

    // Add empty cells for days before the starting day of the week
    for (let j = 0; j < startDay; j++) {
      calendarHTML += '<td></td>';
    }

    // Loop through the days of the month and add them to the calendar
    for (let j = 1; j <= numDays; j++) {
      // Start a new row every 7 days
      if ((startDay + j - 1) % 7 === 0 && j !== 1) {
        calendarHTML += '</tr><tr>';
      }
      calendarHTML += `<td>${j}`;
      //to add the event 
      for(let e = 0; e < len; e++){
        if(i == EventMonth[e] - 1){
          if (j == EventDate[e]){
            calendarHTML += `<span  id="test${e}" class="material-symbols-outlined" style="font-size: 9px;" >filter_vintage</span>`;
            calendarHTML += '<div class="cardwraper">';
            calendarHTML += `<div class="card${e}" style="display: none;">`;
            calendarHTML += '<div class="card-content">';
            calendarHTML += `<label style="font-weight:bold">${events[e].TheEvent}</label>`;
            calendarHTML += `<p style="font-size: smaller">Category: ${events[e].Category}</p>`;
            calendarHTML += '</div>';
            calendarHTML += '</div>';
            calendarHTML += '</div>';
          }
        }
      }
      calendarHTML += `</td>`;
      //if j == date then we will add it, if month == month and j == date then add the icon. need to make cursor card. 
    }

    // Add empty cells to complete the last row
    const lastDay = new Date(monthDate.getFullYear(), monthDate.getMonth(), numDays).getDay();
    for (let j = lastDay + 1; j < 7; j++) {
      calendarHTML += '<td></td>';
    }
    calendarHTML += '</tr>';
    calendarHTML += '</table>';
    calendarHTML += '</div>';
  }
  document.getElementById('calendaryear').innerHTML = calendarHTML;


for(let b = 0; b < len; b++){
  document.getElementById(`test${b}`).addEventListener("mouseover", function(event){
    $(`.card${b}`).css('display', 'block');
  });
  document.getElementById(`test${b}`).addEventListener("mouseout", function(event){
    $(`.card${b}`).css('display', 'none');
  });
}
}

updateCalendar(variant);


