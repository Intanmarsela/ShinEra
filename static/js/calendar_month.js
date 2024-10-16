const next = document.getElementById('right');
const prev = document.getElementById('left');
const today = document.getElementById('today');
let events = [] //for storing the events that pass by py
let len //the number of the events
let EventDates = []
let EventMonth = []
let EventDate = []

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

async function updateCalendar (variant){
    //Get the current date
    const currentdates = new Date();
    const month = currentdates.getMonth() + variant;
    var send = currentdates.getFullYear() + variant;
    let resp = await SendDateToPy(send);
    //Define the days and months name
    const dayNames_m = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
    const monthNames_m = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    const display = document.getElementById('timeh2');

    if (display) {
        display.textContent = monthNames_m[month];
    }

    let calendarHTML_m = '';

    //Getting the current month
    calendarHTML_m += '<table class="month_calmonth">';
    calendarHTML_m += '<tr>';

    // Add day names as table headers
    for (let j = 0; j < 7; j++){
        calendarHTML_m += `<th class="day">${dayNames_m[j]}</th>`;
    }
    calendarHTML_m += '</tr><tr>';

    //Getting the start day of the month
    const firstday = new Date(currentdates.getFullYear(),currentdates.getMonth() + variant, 1 );
    const startday = firstday.getDay();

    //Getting the number of the days in that month
    const numdays = new Date(currentdates.getFullYear(),currentdates.getMonth()+ variant + 1 , 0).getDate();

    for (let i = 0; i < startday; i++){
        calendarHTML_m += '<td></td>';
    }

    // Loop through the days of the month and add them to the calendar
    for (let j = 1; j <= numdays; j++){
    // Start a new row every 7 days
        if ((startday + j - 1) % 7 === 0 && j !== 1) {
            calendarHTML_m += '</tr><tr>';
        }
        calendarHTML_m += `<td>${j}`;
        for(let m = 0; m < len; m++){
          if(EventMonth[m] == month+1){
            if(j == EventDate[m]){
              calendarHTML_m += `<span id="test${m}" class="material-symbols-outlined" style="font-size: 9px;" >filter_vintage</span>`;
              calendarHTML_m += '<div class="cardwraper">';
              calendarHTML_m += `<div class="card${m}" style="display: none;">`;
              calendarHTML_m += '<div class="card-content">';
              calendarHTML_m += `<label style="font-weight:bold">${events[m].TheEvent}</label>`;
              calendarHTML_m += `<p style="font-size: smaller">Category: ${events[m].Category}</p>`;
              calendarHTML_m += '</div>';
              calendarHTML_m += '</div>';
              calendarHTML_m += '</div>';
            }
          }
        }
        calendarHTML_m += `</td>`;
    }

    const lastDay = new Date(currentdates.getFullYear(), currentdates.getMonth() + variant, numdays).getDay();
    for (let j = lastDay + 1; j < 7; j++){
    calendarHTML_m += '<td></td>';
    }

    calendarHTML_m += '</tr>';
    calendarHTML_m += '</table>';
    calendarHTML_m += '</div>';

    document.getElementById('calendarmonthly').innerHTML = calendarHTML_m; 
    for(let b = 0; b < len; b++){
      document.getElementById(`test${b}`).addEventListener("mouseover", function(event){
        $(`.card${b}`).css('display', 'block');
      });
      document.getElementById(`test${b}`).addEventListener("mouseout", function(event){
        $(`.card${b}`).css('display', 'none');
      });
    }
}
updateCalendar(variant)


