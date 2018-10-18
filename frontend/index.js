var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var request = require('request');
var http = require('http');
var exphbs  = require('express-handlebars');


// Create application/x-www-form-urlencoded parser
var urlencodedParser = bodyParser.urlencoded({ extended: false })

app.use(express.static('public'));
app.use(urlencodedParser)
app.engine('handlebars', exphbs({defaultLayout: 'result'}));
app.set('view engine', 'handlebars');

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
   console.log(req.body.password)
   request.post('http://127.0.0.1:5000/signup',
   { json: { "username": req.body.email,"password":req.body.password} },
   function (error, response, body) {
     console.log('error:', error); // Print the error if one occurred
     console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
     console.log('body:', body); // Print the HTML for the Google homepage.
   });
   console.log(statusCode);
   if (statusCode==400){
        res.redirect('/');
   }
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
    request.post('http://127.0.0.1:5000/login',
    { json: { "username": req.body.email,"password":req.body.password} },
    function (error, response, body) {
      console.log('error:', error); // Print the error if one occurred
      console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
      console.log('body:', body); // Print the HTML for the Google homepage.
    });
    console.log(response);
    res.redirect('/predict')
 })

app.get('/prediction', (req, res) => {
    res.sendFile( __dirname + "/" + "prediction.html" );
 })

app.post('/prediction', (req, res)=> {
   console.log(req.body.cast);
    // Prepare output in JSON format
    request.post('http://127.0.0.1:5000/collections',
    { json: { "indicator_id": req.body.cast} },
    function (error, response, body) {
      console.log('error:', error); // Print the error if one occurred
      console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
      console.log('body:', body); // Print the HTML for the Google homepage.
    });
    res.redirect('/result')
 })

 app.get('/result', (req, res) => {
   request.post('http://127.0.0.1:5000/predict',
   function (error, response, body) {
     console.log('error:', error); // Print the error if one occurred
     console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
     console.log('body:', body); // Print the HTML for the Google homepage.
     res.render('result',{user:body})
   });
    //res.sendFile( __dirname + "/" + "result.html" );
 })

// Handle 404
app.use((req, res) =>{
  res.status(404).sendFile(__dirname + "/"+'404.html');
});

// Handle 500
app.use((error, req, res, next)=> {
  res.status(500).sendFile(__dirname + +"/"+'500.html');
});

var server = app.listen(8081, function () {
   var host = server.address().address
   var port = server.address().port

   console.log("Example app listening at http://%s:%s", host, port)

})