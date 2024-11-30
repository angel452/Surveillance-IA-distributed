const { spawn } = require('child_process');
const path = require('path');
const multer = require('multer');
const fs = require('fs');

const uploadFolder = path.join(__dirname, '..', 'uploads'); // Carpeta para los videos subidos
const outputFolder = path.join(__dirname, '..', 'detections'); // Carpeta para los resultados

// Configuración de multer para manejar la carga de archivos
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
      // Establecer la carpeta de destino para los archivos subidos
      cb(null, uploadFolder);
  },
  filename: (req, file, cb) => {
      // Establecer el nombre del archivo como su nombre original
      cb(null, file.originalname);
  },
});
// Crear instancia de multer con la configuración definida
const upload = multer({ storage });

// Crear carpetas si no existen
if (!fs.existsSync(uploadFolder)) fs.mkdirSync(uploadFolder);
if (!fs.existsSync(outputFolder)) fs.mkdirSync(outputFolder);

// Método para subir un video
exports.uploadVideo = (req, res) => {
  // Usar multer para manejar la carga del archivo
  upload.single('video')(req, res, (err) => {
      if (err) {
          // En caso de error, devolver un mensaje de error
          return res.status(500).json({ message: 'Error uploading video', error: err.message });
      }

      // Si todo sale bien, devolver el mensaje de éxito con la ruta del archivo
      res.status(200).json({ message: 'Video uploaded successfully', filePath: req.file.path });
  });
};

// Método para iniciar el proceso de escaneo de videos
exports.scanVideos = (req, res) => {
  console.log('Scanning videos...');

  const scriptPath = path.join(__dirname, '..', 'python', 'scanner.py');
  
  const { spawn } = require('child_process');
  const pythonProcess = spawn('python', [scriptPath, uploadFolder, path.join(__dirname, '..', 'detections')]);

  let outputData = '';
  let errorData = '';

  pythonProcess.stdout.on('data', (data) => {
      outputData += data.toString();
      console.log(`stdout: ${data.toString()}`);
  });

  pythonProcess.stderr.on('data', (data) => {
      errorData += data.toString();
      console.error(`stderr: ${data.toString()}`);
  });

  pythonProcess.on('close', (code) => {
      if (code === 0) {
          res.status(200).json({
              message: 'Scan completed successfully',
              results: outputData.split('\n'),
          });
      } else {
          res.status(500).json({
              message: 'Error during scanning',
              error: errorData,
          });
      }
  });
};
