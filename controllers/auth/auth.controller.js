const accounts = require('../../models/accounts');
const DEBUG = require('debug');

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
