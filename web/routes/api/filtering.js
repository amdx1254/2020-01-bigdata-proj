const express = require('express');
const csv = require("csvtojson");
var router = express.Router();

/* GET users listing. */
router.get('/', function(req, res, next) {
    res.send('respond with a resource');
});


router.get('/cf', function(req, res, next) {
    var user_id = req.query.user_id;
    var item = [{ id: 1, name: "테스트1", satisfaction: 30 }, { id: 2, name: "테스트2", satisfaction: 10 }]
    res.send({
        item: item
    });
});

router.get('/cbf', function(req, res, next) {
    var user_id = req.query.user_id;
    var item = [{ id: 1, name: "테스트1", satisfaction: 70 }, { id: 3, name: "테스트3", satisfaction: 60 }]
    res.send({
        item: item
    });
});

module.exports = router;