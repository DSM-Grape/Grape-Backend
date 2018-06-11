const app = require('../../app');
const should = require('should');
const request = require('supertest');

describe('auth module check', () => {
  // before(done => {
  //   require('../../models').then(done);
  // });

  it('status 200과 함께 \'hello\'가 리턴되는가?', (done) => {
    request(app)
      .get('/')
      .end((err, res) => {
        should(res.status).be.equal(200);
        should(res.body.msg).be.equal('hello');
        done();
      });
  });

  it('accounts 컬럼 추가 테스트', (done) => {
    const accounts = require('../../models/accounts');
    accounts.remove().then(() => {
      new accounts({
        id: 'asv',
        password: 'asd',
        plan: 'FREE',
        email: 'asdasd',
        nickname: 'asdads'
      }).save().then(saved => {
        accounts.remove().then(() => done());
      });
    });
  });
});
