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
    const btnLogin = document.getElementById('btnLogin');

    //Login event
    btnLogin.addEventListener('click', e => {
        var email = txtEmail.value;
        var pass = txtPassword.value;
        var auth = firebase.auth();

        //Sign in
        const promise = auth.signInWithEmailAndPassword(email, pass);
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