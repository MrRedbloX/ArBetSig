const express = require('express')
const pug = require('pug')
const favicon = require('serve-favicon')
const path = require('path')

const AuthService = require('./js/auth_service.js')
const Utils = require('./js/utils.js')

port = process.env.PORT || 8000
app = express()
router = express.Router()

var bets = {
  headers: ['Event', 'Details', 'Home', 'Home Bookie', 'Away', 'Away Bookie', 'Draw', 'Draw Bookie', 'Missing Odds (%)', 'Stake Repartition'],
  body: []
}

router.get('/', (req, res) => {
  res.render('index')
})

router.get('/get_bets', (req, res) => {
  res.send(bets)
})

router.get('/update_bets', AuthService.check_app_auth, (req, res) => {
  if(req.query.bets){
    bets.body = Utils.chunks(req.query.bets, 10)
    res.send({success: true, message: "Bets updated."})
  }
  else res.send({success: false, message: "You have to provide a list of bets."})
})

app.use(favicon(path.join(__dirname,'favicon.ico')))
app.use('/', router)
app.set('view engine', 'pug')
app.listen(port, () => console.log(`Express server listening on port ${port}`))
