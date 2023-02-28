import $ from 'jquery';
import DataTable from 'datatables.net-bs5';


export default async function enableDataTable() {

    $(document).ready(function () {
        const tags = Array.from(document.getElementsByTagName('table'))

        tags.forEach(tag => {
            if (tag.id) {
                const pageLength = tag.id[tag.id.length - 2] + tag.id[tag.id.length - 1]
                $(`#${tag.id}`).DataTable({
                    responsive: true,
                    "aaSorting": [],
                    "pageLength": Number(pageLength),
                    "language": {
                        "decimal": "",
                        "emptyTable": "Sem dados disponíveis",
                        "info": "Mostrando de _START_ até _END_ de _TOTAL_ registros",
                        "infoEmpty": "Mostrando de 0 até 0 de 0 registros",
                        "infoFiltered": "(filtrado de _MAX_ registros no total)",
                        "infoPostFix": "",
                        "thousands": ",",
                        "lengthMenu": "Mostrar _MENU_ Registros",
                        "loadingRecords": "A carregar dados...",
                        "processing": "A processar...",
                        "search": "Procurar:",
                        "zeroRecords": "Não foram encontrados resultados",
                        "paginate": {
                            "first": "Primeiro",
                            "last": "Último",
                            "next": "",
                            "previous": ""
                        },
                        "aria": {
                            "sortAscending": ": ordem crescente",
                            "sortDescending": ": ordem decrescente"
                        }
                    }
                });
            }
        })

    });
}