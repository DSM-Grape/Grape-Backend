const app = require('../../app');
const should = require('should');
const request = require('supertest');

describe('auth module check', () => {

  it('status 200과 함께 \'hello\'가 리턴되는가?', done => {
    request(app)
      .get('/')
      .end((err, res) => {
        should(res.status).be.equal(200);
        should(res.body.msg).be.equal('hello');
        done();
      });
  });

  it('accounts 컬럼 추가 테스트', done => {
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

  describe('email duplication check', () => {
    const accounts = require('../../models/accounts');
    const email = 'test@test.com';


    it('이메일이 중복될 때 409를 반환하는가?', done => {
      new accounts({
        id: 'asv',
        password: 'asd',
        plan: 'FREE',
        email,
        nickname: 'asdads'
      }).save()
        .then(() => {
          request(app)
            .get(`/check/email/${email}`)
            .end((err, res) => {
              should(res.status).be.equal(409);
              done();
            });
        });
    });

    it('이메일이 중복되지 않을 때 200을 반환하는가?', done => {
      accounts.remove({email}).then(() => {
        request(app)
          .get(`/check/email/${email}`)
          .end((err, res) => {
            should(res.status).be.equal(200);
            done();
          });
      });
    });
  });
});
