const app = require('../../app')
const should = require('should')
const request = require('supertest')

describe('auth module check', () => {
  it('status 200과 함께 \'hello\'가 리턴되는가?', (done) => {
    request(app)
      .get('/')
      .end((err, res) => {
        should(res.status).be.equal(200)
        should(res.body.msg).be.equal('hello')
        done()
      })
  })
})