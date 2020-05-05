function valid() {

    let username = document.getElementById('uname').value.trim()
    let password = document.getElementById('pass').value.trim()
    let email = document.getElementById('email').value.trim()
    let cpassword = document.getElementById('cpass').value.trim()
    let pimage = document.getElementById('file-2')
    const ch = document.getElementById('check')
    
    

    if (username === '' || password === '' || email === '' || cpassword === '') {
        swal("Empty fields", "Fields cannot be empty", "error");
        return false;
    }
    else if (pimage.files.length == 0) {
        swal("No profile image", "Please select a profile image", "error");
        return false;
    }
    else if (username.length > 10) {
        swal("Lenght error", "Username can't be more than 10 characters", "error");
        return false;
    }
    else if (password.length < 4) {
        swal("Lenght error", "Password can't be less than 4 characters", "error");
        return false;
    }
    else if (password != cpassword) {
        swal("Match error", "Passwords doesn't match", "error");
        return false;
    }
    else if(ch.checked == false){
        swal("Terms & Conditions", "Accept T&C to continue", "error");
        return false;
    }
    else if (pimage.files.length > 0){

        for (const i = 0; i <= pimage.files.length - 1; i++) { 

            const fsize = pimage.files.item(i).size; 
            const file = Math.round((fsize / 1024)); 
            // The size of the file. 
            if (file > 2048) { 
                swal("Image too large", "Maximum upload limit is 2mb", "error");
                return false;
            }
            else { 
                gsap.to(".pro-overlay", {
                    opacity: 1,
                    display: "block",
                    duration: .2
                });
                gsap.to(".processing", {
                    opacity: 1,
                    display: "block",
                    duration: .2
                });
                return true;
            } 
        } 
    }

    else{
        gsap.to(".pro-overlay", {
            opacity: 1,
            display: "block",
            duration: .2
        })
        gsap.to(".processing", {
            opacity: 1,
            display: "block",
            duration: .2
        })
        return true   
    }
}



function validLog() {

    let username = document.getElementById('uname').value.trim();
    let password = document.getElementById('pass').value.trim();


    if (username === '' || password === '') {
        swal("Empty fields", "Fields cannot be empty", "error");
        return false;
    }

    return true;
}


function image(){
    let ki = document.getElementById('file-2');

    console.log('working')
    if (ki.files.length > 0){

        for (const i = 0; i <= ki.files.length - 1; i++) { 

            const fsize = ki.files.item(i).size; 
            const file = Math.round((fsize / 1024)); 
            // The size of the file. 
            if (file >= 3072) { 
                swal("Image too large", "Select an image not more than 3mb", "error");
                return false;
            }
            else { 
                return true;
            } 
        } 
    }
    else{

        return true   

    }
}