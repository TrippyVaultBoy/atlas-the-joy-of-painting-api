const express = require('express');
const episodesController = require('../controllers/episodesController.js');

const router = express.Router();

router.get('/episodes', episodesController.getEpisode);

module.exports = router;