(function () {
    const config = {
        apiKey: "AIzaSyBFpk2n34wvReaeKeZ7KKIp2r9f9fCAr7c",
        authDomain: "groupproject-712e1.firebaseapp.com",
        databaseURL: "https://groupproject-712e1.firebaseio.com",
        projectId: "groupproject-712e1",
        storageBucket: "groupproject-712e1.appspot.com",
        messagingSenderId: "785543171942"
    };
    firebase.initializeApp(config);

    const txtEmail = document.getElementById('txtEmail');
    const txtPassword = document.getElementById('txtPassword');
    const txtName = document.getElementById('txtName');
    const txtStudentId = document.getElementById('txtStudentId');
    const btnSignUp = document.getElementById('btnSignUp');

    //SignUp event

    btnSignUp.addEventListener('click', e => {
        console.log('signing up');
        //Sign In
        var emailVal = txtEmail.value;
        var passVal = txtPassword.value;
        var auth = firebase.auth();

        //Sign Up - store information
        var studentId = txtStudentId.value;
        var nameVal = txtName.value;
        signUp(emailVal, studentId, nameVal);

        
        //Sign up - auth
        const promise = auth.createUserWithEmailAndPassword(emailVal, passVal);
        promise.catch(e => console.log(e.massage));
    })

    //Logout Event
    btnLogout.addEventListener('click', e => {
        firebase.auth().signOut();
        window.location = 'index.html';
    })

    var loginBtn = document.getElementById("btnLogin");
    var logoutBtn = document.getElementById("btnLogout");

    //realtime listener
    firebase.auth().onAuthStateChanged(firebaseUser => {
        if(firebaseUser) {
            window.location = 'index.html';
        } else {
            console.log('not logged in');
            btnLogout.style.display = "none";
        }
    })
}());


function signUp(email, studentId, name) {
    var value = {
        name : name,
        email : email,
        studentId : studentId
    }
    console.log(name);
    console.log(email);
    console.log(studentId);
    
    var dbRef = firebase.database().ref('All/StudentList');
    dbRef.push().set(value, error => {
        if(error) {
            console.log('Sign up failed, please try again');
        } else {
            console.log("Sign up successful!");
        }
    })
}