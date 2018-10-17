var check = function() {
    if (document.getElementById('Password1').value ==
        document.getElementById('Password2').value) {
        document.getElementById('Help').className="form-text text-success"
        document.getElementById('Help').innerHTML = 'matching';
        document.getElementById('submit').disabled=false;
    } else {
        document.getElementById('Help').className="form-text text-danger"
        document.getElementById('Help').innerHTML = 'Password Not Match';
        document.getElementById('submit').disabled=true;
    }
}
