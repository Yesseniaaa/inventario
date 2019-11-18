
	sumador = {
		objetoSumaPrecio: document.querySelector('#TotalVenta'),
		objetoInputPrecio: null,
		objetoInputCantidad: null,
		init: function(){

			sumador.objetoInputPrecio = document.querySelectorAll('.productos_precio');
			sumador.objetoInputCantidad =  document.querySelectorAll('.productos_cantidad');

			for(var i = 0 ; i < sumador.objetoInputPrecio.length ; i++){
				sumador.objetoInputPrecio[i].addEventListener('change', function(){
					sumador.suma();
					
				}, false);
				sumador.objetoInputCantidad[i].addEventListener('change', function(){
					sumador.suma();
				}, false);
			}

			sumador.suma();
		},
		suma: function(){
			var sumaPrecio = 0;
			var sumaCantidad = 0;
			for(var i = 0 ; i < sumador.objetoInputPrecio.length ;i++){
				if(sumador.objetoInputPrecio[i].value != '' && sumador.objetoInputCantidad[i] != ''){
					sumaPrecio += parseInt(sumador.objetoInputPrecio[i].value)*parseInt(sumador.objetoInputCantidad[i].value);
					sumaCantidad += parseInt(sumador.objetoInputCantidad[i].value);
				}
			}

			sumador.setSuma(sumaPrecio);
		},
		setSuma: function(suma){
			sumador.objetoSumaPrecio.value = suma;
		},
	};

	sumador.init();
