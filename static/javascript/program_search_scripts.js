// JavaScript functions used to interact with program_search.html


//JavaScript function to search through the table by table row <tr><td>
function program_search() {
    var input, filter, table, tr, td, i, txtValue;

    // returning the input from the searchbar
    input = document.getElementById("searchbar");
    filter = input.value.toUpperCase();
    table = document.getElementById("program-table");
    tr = table.getElementsByTagName("tr");

    for(i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[0]; //<--- Change this to set index of table column to be read
        if(td) {
            txtValue = td.textContent || td.innserText;
            if(txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}


function delete_mode() {
    var column = document.createElement('td');
    column.id = 'cancel-check';
    document.getElementById('program-table').insertAdjacentElement('beforeend', column);
    document.getElementById('cancel-check').innerHTML = '<input type="checkbox"></input>';
}