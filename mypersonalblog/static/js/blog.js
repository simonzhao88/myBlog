function init() {
    var user =;

    alert(user)
    if (user == "null") {
        var center = document.getElementById("img");
        // var exit = document.getElementById("exit");
        center.style.display = 'none';
        exit.style.display = 'none';
    } else {
        var login = document.getElementById("login");
        register.style.display = 'none';
        login.style.display = 'none';
    }
}