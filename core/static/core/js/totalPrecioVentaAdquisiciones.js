
	sumador = {
		objetoSumaPrecio: document.querySelector('#totalPrecio'),
		objetoSumaCantidad: document.querySelector('#totalCantidad'),
		objetoInputPrecio: null,
		objetoInputCantidad: null,
		init: function(){

			sumador.objetoInputPrecio = document.querySelectorAll('.productos_precio'); 
			sumador.objetoInputCantidad = document.querySelectorAll('.productos_cantidad');
			sumador.suma();

			for(var i = 0 ; i < sumador.objetoInputPrecio.length ;i++){
				sumador.objetoInputPrecio[i].addEventListener('change', function(){
					sumador.suma();
				}, false);
				sumador.objetoInputCantidad[i].addEventListener('change', function(){
					sumador.suma();
				}, false);
			}

			/*
			for(var i = 0 ; i < sumador.objetoInputCantidad.length ;i++){
				sumador.objetoInputCantidad[i].addEventListener('keyup', function(){
					sumador.suma2();
				}, false);
			}*/
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
			sumador.setSuma2(sumaCantidad);
		},
		suma2: function(){
			var suma = 0;
			for(var i = 0 ; i < sumador.objetoInputCantidad.length ;i++){
				if(sumador.objetoInputCantidad[i].value != ''){
					suma += parseInt(sumador.objetoInputCantidad[i].value)
				}	
			}

			sumador.setSuma2(suma);
		},
		setSuma: function(suma){
			sumador.objetoSumaPrecio.value = suma;
		},
		setSuma2: function(suma){
			sumador.objetoSumaCantidad.value = suma;
		}
	};


