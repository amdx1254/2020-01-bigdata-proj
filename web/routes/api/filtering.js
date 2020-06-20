const express = require('express');
const fs = require("fs");
let router = express.Router();

/* GET users listing. */
router.get('/', function(req, res, next) {
    res.send('respond with a resource');
});


router.get('/cf', async(req, res) => {
    let user_id = req.query.user_id;
    fs.readFile(__dirname + '/../../public/data/users_CF_test.json', 'utf8', (error, data) => {
        if (error) return console.log(error);

        let jsonData = JSON.parse(data);
        let item = jsonData.data;
        let result = item.filter(function(i) {
            return i.user_id === Number(user_id);
        });
        res.send({ item: result });

    });
});

router.get('/cbf', async(req, res) => {
    let user_id = req.query.user_id;
    fs.readFile(__dirname + '/../../public/data/users_CBF_test.json', 'utf8', (error, data) => {
        if (error) return console.log(error);

        let jsonData = JSON.parse(data);
        let item = jsonData.data;
        let result = item.filter(function(i) {
            return i.user_id === Number(user_id);
        });
        res.send({ item: result.reverse() });

    });
});

module.exports = router;