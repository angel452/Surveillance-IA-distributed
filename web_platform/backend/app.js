const express = require('express');
const cors = require('cors');
const videoRoutes = require('./routes/video');

const app = express();
app.use(cors());
app.use(express.json());
app.use('/api/videos', videoRoutes);

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Backend running on http://localhost:${PORT}`);
});
