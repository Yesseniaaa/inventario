$(document).ready(function (){
    $.ajax({
        method: "GET",
        url: "/persona",
        dataType: 'json',
        beforeSend: function(){
            swal({
                title:"Cargando",
                showConfirmButton: false,
                imageUrl: "static/img/ajax.gif",
                imageHeight: 80
            });
        },
        success: function (data) {
            swal.close()
            //console.log(data)
            labelsa = data.labels
            var ctx = document.getElementById("myChart").getContext('2d');
            $("#grafico").show();
                var myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labelsa,
                    datasets: data.datos,
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero:true
                            }
                        }]
                    }
                }
            });
            alertify.success('Carga completa AJAX');
        },
        error: function (error_data) {
            console.log("ERROR")
        }
    });
});

