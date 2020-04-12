$(document).ready( function () {
    
	rut = {
		rut: document.querySelectorAll('.rut'),
		init: function(){
			for(var i = 0 ; i < rut.rut.length ;i++){
				rut.rut[i].addEventListener('keyup', function(e){
					rut.formatearRut(e.target);
				}, false);
			}
		},
		formatearRut: function(input_rut){
			var rut = input_rut.value;
			var numero_verificador = '';
		
			if(rut.length > 1 && rut[rut.length-1].match(/[0-9kK]/)){
				numero_verificador = rut[rut.length-1];
				rut_temporal = rut.substring(0,rut.length-1);
				rut_temporal = rut_temporal.replace(/[^0-9]+/g,'');
				rut = '';

				for(i = rut_temporal.length-1 ; i >= 0; i = i - 3){
					punto = '';
					a = '';b = '';c = '';
					if(rut_temporal[i-3])punto = '.';
					if(rut_temporal[i-2])a = rut_temporal[i-2];
					if(rut_temporal[i-1])b = rut_temporal[i-1];
					if(rut_temporal[i])c = rut_temporal[i];
						
					rut = punto + a + b + c + rut;
				}
				rut += "-" + numero_verificador;
			}else{
				rut = rut.replace(/[^0-9k]+/g,'');
			}

			//console.log(rut);
			
			input_rut.value = rut;
			
		}
	};

	rut.init();

} );
