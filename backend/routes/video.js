const express = require('express');
const { uploadVideo, scanVideos } = require('../controllers/videoController');
const router = express.Router();

router.post('/upload', uploadVideo);
router.post('/scan', scanVideos);

module.exports = router;
