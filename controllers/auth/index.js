const router = require('express').Router();
const {
  hello,
  emailDuplicationCheck,
  sendEmail,
} = require('./auth.controller');

router.route('/').get(hello);
router.route('/check/email/:email').get(emailDuplicationCheck);
router.route('/email/certify/:email').get(sendEmail);

module.exports = router;
