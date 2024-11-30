const express = require('express');
const { uploadVideo, scanVideos, make_query } = require('../controllers/videoController');
const router = express.Router();

router.post('/upload', uploadVideo);
router.post('/scan', scanVideos);
router.post('/make_query', make_query);


module.exports = router;
