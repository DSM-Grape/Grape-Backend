'use strict';
const express = require('express')
const app = express()
const SwaggerExpress = require('swagger-express-mw');
const SwaggerUI = require('swagger-tools/middleware/swagger-ui');
const bodyParser = require('body-parser')
const router = require('./controllers')
const morgan = require('morgan')
const cors = require('cors')

const config = {
    appRoot: __dirname, // required config
    swaggerFile: __dirname + '/swagger/swagger.yaml'
};

const port = process.env.GRAPE_PORT || 3000

app.use(morgan('dev'))
app.use(cors({
    origin: true
}))
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({
    extended: false
}))

app.use(router)

SwaggerExpress.create(config, function (err, swaggerExpress) {
    if (err) {
        throw err;
    }

    // swaggerExpress.runner.swagger.host = host
    app.use(SwaggerUI(swaggerExpress.runner.swagger))

    // install middleware
    swaggerExpress.register(app);

    app.listen(port, () => {
        console.log(`the server running on ${port} port`)
    });

});

module.exports = app
