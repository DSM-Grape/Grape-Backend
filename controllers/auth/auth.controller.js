const accounts = require('../../models/accounts');
const DEBUG = require('debug');
const nodemailer = require('nodemailer');
const smtpPool = require('nodemailer-smtp-pool');
const uuid = require('uuid/v4');
const redis = require('redis');

const smtpTransport = nodemailer.createTransport(smtpPool({  
  service: 'Gmail',
  auth: {
    user: process.env.SMTP_ID,
    pass: process.env.SMTP_PW
  }
}));

const redisClient = redis.createClient();

exports.hello = (req, res) => {
  res.status(200).json({
    msg: 'hello',
  });
};

exports.emailDuplicationCheck = async (req, res) => {
  const debug = DEBUG('api:email-duplication-check');
  const { email } = req.params;

  try {
    const account = await accounts.findOne({ email });

    if (account) res.sendStatus(409);
    else res.sendStatus(200);
  } catch (e) {
    debug(e.message);
    res.sendStatus(500);
  }
};

exports.sendEmail = async (req, res) => {
  const debug = DEBUG('api:send-email');
  const { email } = req.params;

  try {
    if (await accounts.findOne({ email })) {
      res.sendStatus(409);
    } else {
      const code = uuid().substring(0, 5).toUpperCase();

      redisClient.set(email, code, 'EX', 3600);

      const mailOptions = {  
        from: `Grape <${process.env.SMTP_ID}@gmail.com>`,
        to: email,
        subject: 'Grape 회원가입 인증 코드입니다.',
        html: `인증 코드 : ${code}`
      };

      smtpTransport.sendMail(mailOptions, (error) => {
        smtpTransport.close();

        if (error){
          res.sendStatus(204);
        } else {
          res.sendStatus(200);
        }
      });
    }
  } catch (e) {
    debug(e.message);
    res.sendStatus(500);
  }
}
