$(document).ready(function() {
    $('#registration-form')

    .on('init.field.fv', '[name="id_number"]', function(e, data){
           console.log("initialized"); 
	   if(id_error) {
	       console.log("error present"); 
	   }
    })
    .formValidation({
       framework: 'bootstrap',
	   icon: {
	       valid: 'glyphicon glyphicon-ok', 
	       invalid: 'glyphicon glyphicon-remove',
	       validating: 'glyphicon glyphicon-refresh'
	   },
           fields: {
	       first_name: {
	           validators: {
		       notEmpty: {
		            message: 'Please provide a first name' 
		       }, 
		       regexp: {
		            regexp: /^[A-z]+$/, 
		            message: 'Only alphabetic characters are allowed' 
		       }
		   } 
	       }, 
	       middle_name: {
		   enabled: false,
	           validators: {
		       notEmpty: {
		            message: 'Please provide a first name' 
		       }, 
		       regexp: {
		            regexp: /^[A-z]+$/, 
		            message: 'Only alphabetic characters are allowed' 
		       }
		   } 
	       
	       }, 
	       surname: {
	           validators: {
		       notEmpty: {
		            message: 'Please provide a surname' 
		       }, 
		       regexp: {
		            regexp: /^[A-z]+$/, 
		            message: 'Only alphabetic characters are allowed' 
		       }
		   } 
	       
	       }, 
	       email_address: {
	           validators: {
		       notEmpty: {
		            message: 'An email address is required' 
		       },
		       emailAddress: {
		            message: 'That is not a valid email address' 
		       }
		   } 
	       
	       }, 
	       id_number: {
	           validators: {
		       notEmpty: {
		            message: 'Your ID number is required' 
		       },
		       regexp: {
		            regexp: /^(ENG|ABS|ADS)\d{2}[AB]\d{5}Y/i, 
		            message: 'That is not a valid ID number' 
		       },
		       blank: {
		       }
		   } 
	       }, 
	       phone_number: {
	           validators: {
		       notEmpty: {
		            message: 'Your phone number is required' 
		       },
		       regexp: {
		            regexp: /^(\+233|0)\d{9}\d*$/, 
		            message: 'That is not a valid phone number'
		       },
		   } 
	       }, 
	       password_confirm: {
	           validators: {
		        verbose: false,
		       identical: {
			      field:'password',
		            message: 'Please enter matching passwords' 
		       }
		   } 
	       
	       }, 
	       password: {
	           validators: {
		       verbose: false,
		       notEmpty: {
		            message: 'Please provide a password' 
		       }
		   } 
	       
	       }, 
	       program: {
	           validators: {
		       notEmpty: {
		            message: 'Please choose one program' 
		       }
		   } 
	       }
	   }, 
    
    })
    if(id_error) {
	$('#registration-form').data('formValidation')
	       .updateStatus('id_number', 'INVALID', 'blank')
	       .updateMessage('id_number', 'blank', 'This ID number is already enrolled');
        console.log("error seen again");    
	id_error = false;
    }


    $('#student-login-form')

    .on('init.field.fv', '[name="id_number"]', function(e, data){
           console.log("initialized"); 
	   if(student_login_error) {
	       console.log("error present"); 
	   }
    })
    .formValidation({
       framework: 'bootstrap',
	   icon: {
	       valid: 'glyphicon glyphicon-ok', 
	       invalid: 'glyphicon glyphicon-remove',
	       validating: 'glyphicon glyphicon-refresh'
	   },
           fields: {
	       id_number: {
	           validators: {
		       notEmpty: {
		            message: 'Your ID number is required' 
		       },
		       regexp: {
		            regexp: /^(ENG|ABS|ADS)\d{2}[AB]\d{5}Y/i, 
		            message: 'That is not a valid ID number' 
		       },
		       blank: {
			    message: " "
		       }
		   } 
	       }, 
	       password: {
	           validators: {
		       verbose: false,
		       notEmpty: {
		            message: 'Please provide a password' 
		       },
		       blank: {
			    message: 'Incorrect ID number and/or password'
		       }
		   } 
	       
	       }, 
	   }, 
    
    })
    if(student_login_error) {
	$('#student-login-form').data('formValidation')
	       .updateStatus('id_number', 'INVALID', 'blank')
	       .updateStatus('password', 'INVALID', 'blank');
        console.log("error seen again");    
	login_error = false;
    }

    $('#admin-login-form')
    .formValidation({
       framework: 'bootstrap',
	   icon: {
	       valid: 'glyphicon glyphicon-ok', 
	       invalid: 'glyphicon glyphicon-remove',
	       validating: 'glyphicon glyphicon-refresh'
	   },
           fields: {
	       username: {
	           validators: {
		       notEmpty: {
		            message: 'Your Username is required' 
		       },
		       blank: {
			    message: " "
		       }
		   } 
	       }, 
	       password: {
	           validators: {
		       verbose: false,
		       notEmpty: {
		            message: 'Please provide a password' 
		       },
		       blank: {
			    message: 'Incorrect Username and/or Password'
		       }
		   } 
	       
	       }, 
	   }, 
    })

    if(admin_login_error) {
	$('#admin-login-form').data('formValidation')
	       .updateStatus('username', 'INVALID', 'blank')
	       .updateStatus('password', 'INVALID', 'blank');
        console.log("error seen again");    
	login_error = false;
    }

    $('#password-reset-confirm')
    .formValidation({
       framework: 'bootstrap',
	   icon: {
	       valid: 'glyphicon glyphicon-ok', 
	       invalid: 'glyphicon glyphicon-remove',
	       validating: 'glyphicon glyphicon-refresh'
	   },
           fields: {
	       password: {
	           validators: {
		       verbose: false,
		       notEmpty: {
		            message: 'Please provide a password' 
		       }
		   } 
	       }, 
	       password_confirm: {
	           validators: {
		        verbose: false,
		       identical: {
			      field:'password',
		            message: 'Please enter matching passwords' 
		       }
		   } 
	       }, 
	   }, 
    })

$('#password-reset-form')
    .formValidation({
       framework: 'bootstrap',
	   icon: {
	       valid: 'glyphicon glyphicon-ok', 
	       invalid: 'glyphicon glyphicon-remove',
	       validating: 'glyphicon glyphicon-refresh'
	   },
           fields: {
	       email_address: {
	           validators: {
		       verbose: false,
		       notEmpty: {
		            message: 'Please provide your email address' 
		       },
		       emailAddress: {
		            message: 'That is not a valid email address' 
		       }
		   } 
	       }, 
	   }
    })
    var active_link = $("ul.submenu-wrapper").children(".active");
    $(".bs-sidebar").animate({scrollTop: active_link.offset().top-300}, 200);
    console.log(active_link.offset().top);
})
