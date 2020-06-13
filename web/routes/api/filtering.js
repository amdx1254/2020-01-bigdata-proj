const express = require('express');
const csv = require("csvtojson");
var router = express.Router();

/* GET users listing. */
router.get('/', function(req, res, next) {
    res.send('respond with a resource');
});


router.get('/cf', function(req, res, next) {
    var user_id = req.query.user_id;
    var item = [{ name: "테스트", satisfaction: 30 }]
    res.send({
        item: item
    });
});

router.get('/cbf', function(req, res, next) {
    var user_id = req.query.user_id;
    var item = [{ name: "테스트", satisfaction: 70 }]
    res.send({
        item: item
    });
});

module.exports = router;