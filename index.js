var express = require('express');
var app = express();
var bodyParser = require('body-parser');

// Create application/x-www-form-urlencoded parser
var urlencodedParser = bodyParser.urlencoded({ extended: false })

app.use(express.static('public'));
app.use(urlencodedParser)

app.get('/', (req, res) => {
   res.sendFile( __dirname + "/" + "signup.html" );
})

app.post('/', (req, res)=> {
   // Prepare output in JSON format
   response = {
      email:req.body.email,
      password:req.body.password,
      confirm_password: req.body.cpassword
   };
   console.log(response);
   res.redirect('/login')
})

app.get('/login', (req, res) => {
    res.sendFile( __dirname + "/" + "login.html" );
 })
 
 app.post('/login', (req, res)=> {
    // Prepare output in JSON format
    response = {
       email:req.body.email,
       password:req.body.password
    };
    console.log(response);
    res.redirect('/predict')
 })

 app.get('/prediction', (req, res) => {
    res.sendFile( __dirname + "/" + "prediction.html" );
 })
 
 app.post('/prediction', (req, res)=> {
    // Prepare output in JSON format
    response = {
       budget: req.body.budget,
       cast:req.body.cast
    };
    console.log(response);
    res.redirect('/result')
 })

 app.get('/result', (req, res) => {
    res.sendFile( __dirname + "/" + "result.html" );
 })


 
var server = app.listen(8081, function () {
   var host = server.address().address
   var port = server.address().port

   console.log("Example app listening at http://%s:%s", host, port)

})