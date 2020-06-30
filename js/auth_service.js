const config = require('./config.js')

class AuthService{
  static check_app_auth(req, res, next){
    if(config.app_id != req.query.app_id) res.send({success: false, message: "Incorrect app ID."})
    else next()
  }
}

module.exports = AuthService
