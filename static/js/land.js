let passCheck = () => {
    let signupButton = document.getElementById("signupButton");
    let pass = document.getElementById("pass").value;
    let cPass = document.getElementById("cPass").value;
    signupButton.disabled = pass == cPass ? false : true;
    if (!signupButton.disabled) {
        signupButton.disabled = pass.length == 0 && cPass.length == 0 ? true : false;
    }
}