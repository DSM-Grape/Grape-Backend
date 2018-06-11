const router = require('express').Router();
const {
  hello,
  emailDuplicationCheck,
} = require('./auth.controller');

router.route('/').get(hello);
router.route('/check/email/:email').get(emailDuplicationCheck);

module.exports = router;
