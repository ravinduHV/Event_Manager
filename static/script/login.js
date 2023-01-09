document.addEventListener('DOMContentLoaded', function(){
    var submit_button = document.querySelector('#submit');
    var username = document.querySelector('#username');
    var password = document.querySelector('#password')
    submit_button.addEventListener('click', function(event){
        if (username.value == ""){
            event.preventDefault();
            username.style.backgroundColor = "orange"
        }
        else if (password.value == ""){
            event.preventDefault();
            password.style.backgroundColor = "orange"
        }
        if (username.value != "" && password.value != ""){
            username.type = "password"
        }

    });
});