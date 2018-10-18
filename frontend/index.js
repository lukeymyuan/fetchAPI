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
app.engine('handlebars', exphbs({defaultLayout: 'main'}));
app.set('view engine', 'handlebars');

app.get('/', (req, res) => {
   res.render('signup')
})

app.post('/', (req, res)=> {
   // Prepare output in JSON format
   request.post('http://127.0.0.1:5000/signup',{ 
     json: {
     "username": req.body.username,
     "password":req.body.password
    } 
    },
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
    // Prepare output in JSON format
    return new Promise(resolve => {
      request.post('http://127.0.0.1:5000/login',{
         json: { 
          "username": req.body.username,
          "password":req.body.password
          }
        },
        function (error, response, body) {
          console.log('error:', error); // Print the error if one occurred
          console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
          console.log('body:', body); // Print the HTML for the Google homepage.
          if(!error){
            resolve(response.statusCode);
          } else{
            reject("failure");
          }
        })
    }).then((statusCode)=>{
      if (statusCode==400){
        res.redirect(req.originalUrl)
      }
      res.redirect('prediction');
    })
    ;

 })

app.get('/prediction', (req, res) => {
    res.render('prediction')
 })

app.post('/prediction', (req, res)=> {
    
  let IsEnglish = false;
  
  if (req.body.english){
    IsEnglish = true;
  }
  
  console.log(req.body)
  res.end()
    // request.post('http://127.0.0.1:5000/prediction',{
    //   json: { 
    //     "Budget": req.body.budget,
    //     "Cast1": req.body.cast1,
    //     "Cast2": req.body.cast2,
    //     "Cast3": req.body.cast3,
    //     "Cast4": req.body.cast4,
    //     "Length": req.body.length,
    //     "Month": req.body.month,
    //     "IsEnglish": IsEnglish,  
    //     } 
    //   },
    //   function (error, response, body) {
    //     console.log('error:', error); // Print the error if one occurred
    //     console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
    //     console.log('body:', body); // Print the HTML for the Google homepage.

    // });
    // res.redirect('result')
 })

 app.get('/result', (req, res) => {
   request.post('prediction',
   function (error, response, body) {
     console.log('error:', error); // Print the error if one occurred
     console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
     console.log('body:', body); // Print the HTML for the Google homepage.
     res.render('result',{user:body})
   });
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