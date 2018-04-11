
exports.hello = (req, res) => {
    res.status(200).json({
        'msg': 'hello'
    })
}