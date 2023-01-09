document.addEventListener('DOMContentLoaded', function(){
    var deleteLinks = document.querySelectorAll('.delete');

    for (var i = 0; i < deleteLinks.length; i++) {
        deleteLinks[i].addEventListener('click', function(event) {
            var choice = confirm(this.getAttribute('data-confirm'));

            if (!choice) {
                event.preventDefault();
            }
            else {
                pass
            }

        });
    }
});