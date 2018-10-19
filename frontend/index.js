var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var request = require('request');
var exphbs  = require('express-handlebars');
var session = require('express-session');
var flash = require('connect-flash')

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
  next();
})

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

    // if (ssn.token){
      res.render('prediction');
    // }else{
    //   res.status(400).render('400')
    // }
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
      uri: 'http://127.0.0.1:5000/predict?budget='+req.body.budget+'&release_month='+req.body.month+'&english='+isEnglish+'&runtime='+req.body.length,
      method: 'POST'
    }, function (error, response, body) {
        console.log('error:', error); // Print the error if one occurred
        console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
        console.log('body:', body); // Print the HTML for the Google homepage.
        let revenueObj=JSON.parse(body);
        ssn.result=revenueObj['revenue'];
        if(!error){
          resolve('resolved');
        }

      })
    }).then(()=>{
    res.redirect('result');

  });
    // request.post('http://127.0.0.1:5000/prediction',{
    //   json: {
    //     "Budget": req.body.budget,
    //     "Cast1": req.body.cast1,
    //     "Cast2": req.body.cast2,
    //     "Cast3": req.body.cast3,
    //     "Cast4": req.body.cast4,
    //     "Cast5": req.body.cast5,
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
    ssn = req.session;
    result=ssn.result;
    var promise= new Promise(resolve => {
      request.post('http://127.0.0.1:5000/movies',
        { json: { "revenue":result} },
        function (error, response, body) {
          console.log('statusCode:', response && response.statusCode); // Print the response status code if a response was received
          console.log('body:', body); // Print the HTML for the Google homepage.
          resolve(body);
      })
    }).then((list)=>{
      console.log(list);
      res.render('result',{revenue:result,movie1:list['movieList'][0]['movie'],revenue1:list['movieList'][0]['revenue'],poster1:list['movieList'][0]['poster'],movie2:list['movieList'][1]['movie'],revenue2:list['movieList'][1]['revenue'],poster2:list['movieList'][1]['poster'],movie3:list['movieList'][2]['movie'],revenue3:list['movieList'][2]['revenue'],poster3:list['movieList'][2]['poster']});
    })

 })

 app.get('/logout', (req, res) => {
  req.session.destroy((err)=>{
    res.redirect('/')
  })
})

// Handle 404
app.use((req, res) =>{
  res.status(404).render('404')
});




var server = app.listen(8081, function () {
   var port = server.address().port
   console.log(`Example app listening at http://127.0.0.1:${port}`)

})