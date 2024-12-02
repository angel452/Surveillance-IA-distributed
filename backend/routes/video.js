const express = require('express');
const { uploadVideo, scanVideos, make_query, getScanResults, getVideosList } = require('../controllers/videoController');
const router = express.Router();

router.post('/upload', uploadVideo);
router.post('/scan', scanVideos);
router.post('/make_query', make_query);
router.get('/results/:videoName', getScanResults); // Obtener info de videos
router.get('/videos', getVideosList); // Obtener una lista videos

module.exports = router;
