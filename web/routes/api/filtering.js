const express = require('express');
const csv = require("csvtojson");
var router = express.Router();

/* GET users listing. */
router.get('/', function(req, res, next) {
    res.send('respond with a resource');
});


router.get('/cf', function(req, res, next) {
    var user_id = req.query.user_id;
    var item = [{ id: 1, name: "테스트1", summary: "testsummary1", category: "testcategory1", makerName: "testmakerName1", score: 95 },
        { id: 2, name: "테스트2", summary: "testsummary2", category: "testcategory2", makerName: "testmakerName2", score: 90 },
        { id: 5, name: "테스트5", summary: "testsummary5", category: "testcategory1", makerName: "testmakerName1", score: 80 },
        { id: 6, name: "테스트6", summary: "testsummary6", category: "testcategory1", makerName: "testmakerName2", score: 80 },
        { id: 9, name: "테스트9", summary: "testsummary9", category: "testcategory3", makerName: "testmakerName3", score: 80 },
        { id: 10, name: "테스트10", summary: "testsummary10", category: "testcategory4", makerName: "testmakerName4", score: 75 },
        { id: 11, name: "테스트11", summary: "testsummary11", category: "testcategory1", makerName: "testmakerName1", score: 70 },
        { id: 12, name: "테스트12", summary: "testsummary12", category: "testcategory5", makerName: "testmakerName5", score: 60 }
    ];
    res.send({
        item: item
    });
});

router.get('/cbf', function(req, res, next) {
    var user_id = req.query.user_id;
    var item = [{ id: 3, name: "테스트3", summary: "testsummary3", category: "testcategory3", makerName: "testmakerName3", score: 90 },
        { id: 1, name: "테스트1", summary: "testsummary1", category: "testcategory1", makerName: "testmakerName1", score: 80 },
        { id: 4, name: "테스트4", summary: "testsummary4", category: "testcategory2", makerName: "testmakerName2", score: 70 },
        { id: 6, name: "테스트6", summary: "testsummary6", category: "testcategory1", makerName: "testmakerName2", score: 70 },
        { id: 7, name: "테스트7", summary: "testsummary7", category: "testcategory5", makerName: "testmakerName5", score: 70 },
        { id: 8, name: "테스트8", summary: "testsummary8", category: "testcategory5", makerName: "testmakerName5", score: 70 },
        { id: 11, name: "테스트11", summary: "testsummary11", category: "testcategory1", makerName: "testmakerName1", score: 70 },
        { id: 12, name: "테스트12", summary: "testsummary12", category: "testcategory5", makerName: "testmakerName5", score: 60 }
    ]
    res.send({
        item: item
    });
});

module.exports = router;