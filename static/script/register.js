document.addEventListener('DOMContentLoaded', function(){
    var password = document.querySelector('#password');
    var username = document.querySelector('#username');
    var submit = document.querySelector('#submit');
    var tp_no = document.querySelector('#tp_no');
    var email = document.querySelector('#email');
    var confirmation = document.querySelector('#confirmation');

    submit.addEventListener('click', function(event){
        if (password.value == "" || confirmation.value == "" || username.value == ''|| tp_no.value == "" || email.value == ""){
            event.preventDefault();
            alert("Empty Fields not allowed")
        }
        else if(password.value.length < 8 || password.value.length > 15 ){
            event.preventDefault();
            alert("Password length must be atleast 8 characters and not exceed 15 characters")
        }
        else if(password.value != confirmation.value){
            event.preventDefault();
            alert("Password Does not Match")
        }
        else if (tp_no.value.length != 10 && tp_no.value.length != 11){
            event.preventDefault();
            alert("Telephone number Must contain 10 or 11 digits")
        }

    });
});