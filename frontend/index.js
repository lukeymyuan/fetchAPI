var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var request = require('request');
var http = require('http');
var exphbs  = require('express-handlebars');
var session = require('express-session');
app.use(session({
    secret: 'frontend',
    proxy: true,
    resave: true,
    saveUninitialized: true
}));
var ssn;
// Create application/x-www-form-urlencoded parser
var urlencodedParser = bodyParser.urlencoded({ extended: false })

app.use(express.static('public'));
app.use(urlencodedParser)
app.engine('handlebars', exphbs({defaultLayout: 'main'}));
app.set('view engine', 'handlebars');

app.get('/', (req, res) => {
   res.render('signup')
})

app.post('/', (req, res)=> {
   // Prepare output in JSON format
   request.post('http://127.0.0.1:5000/signup',
   { json: { "username": req.body.username,"password":req.body.password} },
   function (error, response, body) {
     console.log('error:', error); // Print the error if one occurred
     console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
     console.log('body:', body); // Print the HTML for the Google homepage.
   });
   res.redirect('login')
})

app.get('/login', (req, res) => {
    res.render('login')
 })

app.post('/login', (req, res)=> {
    ssn = req.session;
    // Prepare output in JSON format
    var promise= new Promise(resolve => {
      request.post('http://127.0.0.1:5000/login',
        { json: { "username": req.body.username,"password":req.body.password} },
        function (error, response, body) {
          console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
          console.log('body:', body); // Print the HTML for the Google homepage.
          if(!error){
            resolve([response.statusCode,body['api-key']]);
          } else{
            reject("failure");
          }
        })
    }).then((response)=>{
      if (response[0]==400){
        res.redirect(req.originalUrl);
      }
      ssn.token=response[1];
      res.redirect('prediction');
    })
    ;

 })

app.get('/prediction', (req, res) => {

    res.render('prediction');
 })

app.post('/prediction', (req, res)=> {
  ssn = req.session;
  console.log(ssn.token);
    // Prepare output in JSON format
  var promise= new Promise(resolve => {
    request({
      headers: {
        'API-KEY': ssn.token
      },
      uri: 'http://127.0.0.1:5000/predict',
      method: 'POST'
    }, function (error, response, body) {
        console.log('error:', error); // Print the error if one occurred
        console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
        console.log('body:', body); // Print the HTML for the Google homepage.
        ssn.result=body;
        resolve('resolved');
      })
    }).then(()=>{
    res.redirect('result');
  }
  );


 })

 app.get('/result', (req, res) => {
    ssn = req.session;
    result=ssn.result;
    console.log(result);
    res.render('result',{revenue:result});
 })

// Handle 404
app.use((req, res) =>{
  res.status(404).render('404')
});


var server = app.listen(8081, function () {
   var host = server.address().address
   var port = server.address().port

   console.log("Example app listening at http://%s:%s", host, port)

})