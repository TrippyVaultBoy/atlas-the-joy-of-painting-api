const express = require('express');
const {dbClient, ObjectId} = require('../utils/db.js');

const episodesController = {
    async getEpisode(req, res) {
        const { month, color, subject } = req.query;

        const filters = {};

        if (month) filters.month = month;
        if (subject) {
            const subjects = subject.split(',').map(s => s.trim());
            filters.subjects = { $in: subjects };
        }
        if (color) {
            const colors = color.split(',').map(c => c.trim());
            filters.colorNames = { $in: colors };
        }

        try {
            const results = await dbClient.db.collection('episodes').find(filters).toArray();
            return res.json(results);
        } catch (err) {
            return res.status(500).json({ error: 'Internal server error' });
        }
    }
};

module.exports = episodesController;