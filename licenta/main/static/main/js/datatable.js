$(document).ready( function () {
    $('#list-courses-table').DataTable({
        "language": {
            "lengthMenu": "Afiseaza _MENU_ lectii pe pagina",
            "zeroRecords": "Cautarea nu a intors niciun rezultat",
            "info": "Arata _PAGE_ din _PAGES_",
            "infoEmpty": "Nu exista lectii disponibile",
            "infoFiltered": "(filtrat din _MAX_ lectii in total)",
            "search": "Cauta ",
            "paginate": {
                "previous": "Anterior",
                "next": "Urmator"
            }
           
        },
        "lengthMenu": [ 5, 10, 15, 25]
    });
} );

