var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var request = require('request');
var exphbs  = require('express-handlebars');
var session = require('express-session');
var flash = require('connect-flash')
var currencyFormatter = require("currency-formatter")

app.use(session({
    secret: 'frontend',
    proxy: true,
    resave: true,
    saveUninitialized: true
}));
var ssn;
// Create application/x-www-form-urlencoded parser
var urlencodedParser = bodyParser.urlencoded({ extended: false })
app.use(session({
  secret:"fetchAPI",
  resave: true,
  saveUninitialized:true
}))
app.use(flash())
app.use(express.static('public'));
app.use(urlencodedParser)
app.engine('handlebars', exphbs({defaultLayout: 'main'}));
app.set('view engine', 'handlebars');

app.use((req,res,next)=>{
  res.locals.error_message = req.flash('error_message')
  res.locals.user = req.user || null;
  next();
})

app.get('/', (req, res) => {
   path = 'Signup'
   res.render('signup',{path:path})
})

app.post('/', (req, res)=> {
   // Prepare output in JSON format
   var promise= new Promise(resolve => {
     request.post('http://127.0.0.1:5000/signup',{
       json: {
       "username": req.body.username,
       "password":req.body.password
        }
      },
     function (error, response, body) {
       console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
       console.log('body:', body); // Print the HTML for the Google homepage.
       if(!error){
         resolve(response.statusCode);
       }
     })
     }).then((statusCode)=>{
       if (statusCode==400){
         req.flash('error_message','Username already exists')
         res.redirect(req.originalUrl)
       }
       res.redirect('login')
     });

})

app.get('/login', (req, res) => {
    path = 'Login'
    res.render('login',{path:path})
 })

app.post('/login', (req, res)=> {
    ssn = req.session;
    // Prepare output in JSON format
    var promise= new Promise(resolve => {
      request.post('http://127.0.0.1:5000/login',
        { json: {
          "username": req.body.username,
          "password":req.body.password
          }
        },
        function (error, response, body) {
          console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
          console.log('body:', body); // Print the HTML for the Google homepage.
          if(!error){
            resolve([response.statusCode,body['api-key']]);
          } else{
            req.flash('error_message','Server Error, Please Contact to Admin fetchAPI@unsw.edu.au')
            res.redirect(req.originalUrl)
          }
        })
    }).then((response)=>{
      if (response[0]==400){
        req.flash('error_message','Incorrect username or password')
        res.redirect(req.originalUrl)
      }
      ssn.token=response[1];
      console.log(`token is ${ssn.token}`)
      res.redirect('prediction');
    })
    ;

 })

app.get('/prediction', (req, res) => {
    ssn = req.session
    path = 'Prediction'
    if (ssn.token){
      res.render('prediction',{path:path});
    }else{
      res.status(400).render('400')
    }
 })

app.post('/prediction', (req, res)=> {

  let isEnglish = 'false';

  if (req.body.english){
    isEnglish = 'true';
  }

  console.log(req.body)
  ssn = req.session;
    // Prepare output in JSON format
  var promise= new Promise(resolve => {
    request({
      headers: {
        'API-KEY': ssn.token
      },
      uri: 'http://127.0.0.1:5000/predict',
      method: 'POST',
      json: {
        "director":req.body.director,
        "budget":req.body.budget,
        "english":isEnglish,
        "runtime":req.body.length,
        "release_month":req.body.month,
        "cast1":req.body.cast1,
        "cast2":req.body.cast2,
        "cast3":req.body.cast3,
        "cast4":req.body.cast4,
        "cast5":req.body.cast5
      }
    }, function (error, response, body) {
        console.log('error:', error); // Print the error if one occurred
        console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
        console.log('body:', body); // Print the HTML for the Google homepage.
        if(response.statusCode===401){
          req.flash('error_message','No access since you are not logged in')
          res.redirect(req.originalUrl)
        }
        ssn.result=body['revenue'];
        if(!error){
          resolve('resolved');
        }else{
          req.flash('error_message','Server Error, Please Contact to Admin fetchAPI@unsw.edu.au')
          res.redirect(req.originalUrl)
        }

      })
    }).then(()=>{
    res.redirect('result');

  });

 })

 app.get('/result', (req, res) => {
    ssn = req.session;
    result=ssn.result;
    var promise= new Promise(resolve => {
      request({
        headers: {
          'API-KEY': ssn.token
        },
        uri:'http://127.0.0.1:5000/movies/'+result,
        method:'GET',
        json: { "revenue":result} },
        function (error, response, body) {
          console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
          console.log('body:', body); // Print the HTML for the Google homepage.
          resolve(body);
          if(response.statusCode===401){
            req.flash('error_message','No access since you are not logged in')
            res.redirect('prediction')
          }
      })
    }).then((list)=>{
      console.log(list);
      //format the number as currency in USD
      let revenue = currencyFormatter.format(result, { code: 'USD' });
      let revenue1 = currencyFormatter.format(list['movieList'][0]['revenue'], { code: 'USD' });
      let revenue2 = currencyFormatter.format(list['movieList'][1]['revenue'], { code: 'USD' });
      let revenue3 = currencyFormatter.format(list['movieList'][2]['revenue'], { code: 'USD' });
      path = 'Result'
      res.render('result',{
        revenue:revenue,
        movie1:list['movieList'][0]['movie'],
        revenue1:revenue1,
        poster1:list['movieList'][0]['poster'],
        movie2:list['movieList'][1]['movie'],
        revenue2:revenue2,
        poster2:list['movieList'][1]['poster'],
        movie3:list['movieList'][2]['movie'],
        revenue3:revenue3,
        poster3:list['movieList'][2]['poster'],
        path:path
      });
    }).catch(error=>{
      console.log(error)
    })

 })

 app.get('/logout', (req, res) => {
  req.session.destroy((err)=>{
    res.redirect('/')
  })
})

// Handle 404
app.use((req, res) =>{
  path = '404'
  res.status(404).render('404',{path:path})
});

var server = app.listen(8081, function () {
   var port = server.address().port
   console.log(`Example app listening at http://127.0.0.1:${port}`)

})