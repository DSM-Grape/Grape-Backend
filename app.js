const express = require('express')
const app = express()
const bodyParser = require('body-parser')
const router = require('./routes')
const morgan = require('morgan')

app.set('port', process.env.GRAPE_PORT || 3000)
app.use(morgan('dev'))
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({
    extended: false
}))

app.use(router)

app.listen(app.get('port'), () => {
    console.log(`Server is listening on ${app.get('port')} port\n\n`)
})

module.exports = app