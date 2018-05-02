const router = require('express').Router()
const controller = require('./auth.controller')

router.route('/').get(controller.hello)

module.exports = router
