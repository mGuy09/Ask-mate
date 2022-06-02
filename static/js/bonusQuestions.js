// you receive an array of objects which you must sort in the by the key "sortField" in the "sortDirection"
// function getSortedItems(items, sortField, sortDirection) {
//     console.log(items)
//     console.log(sortField)
//     console.log(sortDirection)
//
//     // === SAMPLE CODE ===
//     // if you have not changed the original html uncomment the code below to have an idea of the
//     // effect this function has on the table
//     //
//     if (sortDirection === "asc") {
//         const firstItem = items.shift()
//         if (firstItem) {
//             items.push(firstItem)
//         }
//     } else {
//         const lastItem = items.pop()
//         if (lastItem) {
//             items.push(lastItem)
//         }
//     }
//
//     return items
// }

// you receive an array of objects which you must filter by all it's keys to have a value matching "filterValue"
function getFilteredItems(items, filterValue) {
    // console.log(items)
    // console.log(filterValue)

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    //
    let mylist = []
    items.forEach( item => {
        if(filterValue.startsWith('!Description:')){
          let ceva=  filterValue.substring('!Description:'.length)
            if (!item['Description'].includes(ceva)){
                mylist.push(item)
            }
        }
        else if(filterValue.startsWith('Description:')){
            let ceva2 = filterValue.substring('Description:'.length)
            if(item['Description'].includes(ceva2))
                mylist.push(item)

        }
        else if(filterValue.startsWith('!')){
            let ceva3 = filterValue.substring('!'.length)
            if (!item['Title'].includes(ceva3))
                mylist.push(item)
        }

        else{
            if (item['Title'].includes(filterValue)){
            mylist.push(item)
        }
    }})
    return mylist
}

function toggleTheme() {
       let element = document.body;
       element.classList.toggle("dark-mode");
    // console.log("toggle theme")
}

let text = document.querySelector('.text');
let increase = document.querySelector('.increase')

let textSize = 20;

increase.addEventListener('click',()=>{
    if(textSize !== 30){
        textSize = textSize + 2;
        text.style.fontSize = textSize + 'px'
    }
})


let decrease = document.querySelector('.decrease')
decrease.addEventListener('click', ()=>{
    if(textSize !== 20){
        textSize = textSize - 2;
        text.style.fontSize = textSize + 'px'
    }
    console.log("decreaseFont")
})


function sortTable(n){
    let table,rows,switching,i,x,y,shouldSwitch,dir,switchcount=0;
    table = document.getElementById('myTable')
    switching = true;
    dir = 'asc';
    while (switching){
        switching = false;
        rows = table.rows;
        for(i=1; i < (rows.length-1);i++){
            shouldSwitch=false;
            x = rows[i].getElementsByTagName("TD")[n];
            y = rows[i + 1].getElementsByTagName("TD")[n];
            if(dir=='asc'){
                if(x.innerHTML.toLowerCase()>y.innerHTML.toLowerCase()){
                    shouldSwitch=true;
                    break;
                }
            } else if (dir=='desc'){
                if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()){
                    shouldSwitch=true;
                    break
                }
            }
        }
        if (shouldSwitch){
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            switchcount ++;
        }else{
            if(switchcount == 0 && dir == 'asc'){
                dir = 'desc';
                switching=true;
            }
        }
    }
}