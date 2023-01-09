document.addEventListener('DOMContentLoaded', function(){
    var project_name = document.querySelector('#project_name');
    var category = document.querySelector('#category');
    var starting = document.querySelector('#colFormLabel1');
    var ending = document.querySelector('#colFormLabel2');
    var description = document.querySelector('#description');
    var submit = document.querySelector('#submit');
    var text = document.querySelector('#warning')
    var Fields = document.getElementsByClassName('notEm')
    submit.addEventListener('click', function(event){
        if (project_name.value=="" || category.value=="" || starting.value=="" || ending.value=="" || description.value==""){
            event.preventDefault();
            text.innerHTML = "Empty Fields Not Allowed";
        }
        else{
            var d1 = new Date(starting.value).getTime();
            var d2 = new Date(ending.value).getTime();
            console.log(d1);
            if (d1 > d2){
                event.preventDefault();
                text.innerHTML = "Dates Can Not be Validated"
            }
        }
    });

    for (var i = 0; i < Fields.length; i+=1){
        Fields[i].addEventListener('click', function(event){
            text.innerHTML = ""
        });
    }


});