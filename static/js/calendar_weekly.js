const next = document.getElementById('right');
const prev = document.getElementById('left');
const today = document.getElementById('today');
let variant = 0;
next.addEventListener('click',function(event){
  variant +=7;
  updateCalendar(variant);
});
prev.addEventListener('click',function(event){
  variant -=7;
  updateCalendar(variant);
});
today.addEventListener('click',function(event){
  variant = 0;
  updateCalendar(variant);
});

function updateCalendar (variant){
    //Getting current date
    var today = new Date(); 

    const day = today.getDay();
    //Getting the current week date. 
    const sunday = new Date(); 
    if(day != 0){
        sunday.setDate(today.getDate() + variant - day);
    }

    //Define the days and months name
    const dayNames_w = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
    const monthNames_w = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    const time_w = ['12 AM','1 AM','2 AM','3 AM','4 AM','5 AM','6 AM','7 AM','8 AM','9 AM','10 AM','11 AM','12 PM','1 PM','2 PM','3 PM','4 PM','5 PM','6 PM','7 PM','8 PM','9 PM','10 PM','11 PM'];
    const display = document.getElementById('timeh2');
    if (display) {
        display.textContent = monthNames_w[sunday.getMonth()];
    }
    let calendarHTML_w = '';

    //Getting the current month
    calendarHTML_w += '<table class="weekly">';
    calendarHTML_w += '<tr>';
    calendarHTML_w += '<th>GMT+11</th>';

    // Add day names as table headers
    for (let j = 0; j < 7; j++){
        calendarHTML_w += `<th class="day">${dayNames_w[j]}`;
        calendarHTML_w += `</th>`;
    }
    calendarHTML_w += '</tr><tr>';
    const daterange = new Date(sunday);
    calendarHTML_w += '<td></td>';

    //getting the date
    for (let i = 0; i < 7; i++){
        daterange.setDate(sunday.getDate() + i);
        const date = daterange.getDate();
        calendarHTML_w += `<td>${date}</td>`;
    }
    for(let t = 0; t < 24; t++){
        calendarHTML_w += `<tr>`;
        calendarHTML_w += `<td>${time_w[t]}</td>`;
        for(let d = 0; d < 7; d++){
            calendarHTML_w += `<td>`;
            calendarHTML_w += `</td>`;

        }
        calendarHTML_w += '</tr>';
    }
    //Output the calendarHTML_w to HTML page
    document.getElementById('weekly').innerHTML = calendarHTML_w;

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
