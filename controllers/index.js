const router = require('express').Router();
const auth = require('./auth');

router.use('/', auth);

module.exports = router;
