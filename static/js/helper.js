// Helper function to support the main js code
// to count how many days in a year
export default function getDaysInYear(year) {
    let total = 0;
    const NumOfDaysInMonth = [];
    for (let i = 1; i < 13; i++){
        NumOfDaysInMonth [i] = new Date(year, i, 0).getDate();
        total = total + NumOfDaysInMonth[i];
    }
    return total;
}
    const firstday = new Date(2023, 13, 0);
    const day = firstday.getDay();
    console.log(firstday);
    const totalSunday = 0;

