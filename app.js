const express = require('express')
const app = express()
const bodyParser = require('body-parser')
const router = require('./routes')

app.use(bodyParser.json())
app.use(bodyParser.urlencoded({
    extended: false
}))

app.use(router)

app.listen(8080, () => {
    console.log('open')
})