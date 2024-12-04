const { spawn } = require('child_process');
const path = require('path');
const multer = require('multer');
const fs = require('fs');
require('dotenv').config();
const axios = require('axios');
const { type } = require('os');

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

// ##################################### CONTROLADORES (POST) ###################################
// 1. Método para subir un video (/upload)
exports.uploadVideo = (req, res) => {
  // Usar multer para manejar la carga del archivo
  upload.single('video')(req, res, (err) => {
      if (err) {
          // En caso de error, devolver un mensaje de error
          return res.status(500).json({
            message: 'Error uploading video',
            error: err.message 
          });
      }

      // Si todo sale bien, devolver el mensaje de éxito con la ruta del archivo
      res.status(200).json({ 
        message: 'Video uploaded successfully', 
        filePath: req.file.path
     });
  });
};

// 2. Método para iniciar el proceso de escaneo de videos (/scan)
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

// 3. Método para enviar una consulta a la API (/make_query)
exports.make_query = (req, res) => { 
    // Extraer los datos del cuerpo de la solicitud
    let { type, video_name, environment_type, object_name, color, proximity } = req.body;

    // Modificar cada campo para tomar solo el primer valor si es un arreglo
    if (Array.isArray(environment_type) && environment_type.length > 0) {
        environment_type = environment_type[0]; // Tomar solo el primer elemento
    } else if (environment_type && environment_type.length === 0) {
        environment_type = null; // Si el arreglo está vacío, poner null
    }

    if (Array.isArray(object_name) && object_name.length > 0) {
        object_name = object_name[0]; // Tomar solo el primer elemento
    } else if (object_name && object_name.length === 0) {
        object_name = null; // Si el arreglo está vacío, poner null
    }

    if (Array.isArray(proximity) && proximity.length > 0) {
        proximity = proximity[0]; // Tomar solo el primer elemento
    } else if (proximity && proximity.length === 0) {
        proximity = null; // Si el arreglo está vacío, poner null
    }

    // Generar el cuerpo del JSON a enviar a la API
    const queryData = {
        type: type, 
        video_name: video_name || null, 
        environment_type: environment_type || null, 
        object_name: object_name || null,  
        color: color || null,  
        proximity: proximity || null 
    };

    console.log('Query data:', queryData);

    // Recuperar la URL de la API desde la variable de entorno
    const apiUrl = 'http://ec2-18-208-129-187.compute-1.amazonaws.com:1234/receive_characteristics';

    if (!apiUrl) {
        return res.status(500).json({ error: 'API URL is not configured in environment variables' });
    }

    // Enviar el JSON a la API utilizando axios
    axios.post(apiUrl, queryData)
        .then(response => {
            // Responder con los resultados de la API
            res.status(200).json(response.data);
        })
        .catch(error => {
            // Manejar errores al enviar la solicitud a la API
            console.error("Error al enviar la consulta a la API:", error);
            res.status(500).json({ error: 'Error al procesar la consulta' });
        });
};

// 4. Metodo para obtener informacion de los videos (/results/:videoName)
exports.getScanResults = (req, res) => {
    const videoName = req.params.videoName;
    const detectionsFolder = path.join(__dirname, '..', 'detections', videoName);

    // Leemos los archivos JSON en esa carpeta
    const resultFiles = fs.readdirSync(detectionsFolder);
    const jsonFiles = resultFiles.filter(file => file.endsWith('escenario_analysis.json'));
    const txtFiles = resultFiles.filter(file => file.endsWith('.txt'));

    if(jsonFiles.length === 0 && txtFiles.length === 0) {
        return res.status(404).json({ message: 'No results found for video' });
    }

    // Leemos los contenidos de los archivos JSON
    const jsonResults = jsonFiles.map(file => {
        const filePath = path.join(detectionsFolder, file);
        const jsonContent = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
        return {
            type: 'json',
            fileName: file,
            ...jsonContent
        }
    });

    // Leemos los contenidos de los archivos TXT
    const txtResults = txtFiles.map(file => {
        const filePath = path.join(detectionsFolder, file);
        return {
            type: 'txt',
            fileName: file,
            content: fs.readFileSync(filePath, 'utf-8'),
        }
    });

    // Combinamos los resultados de JSON y TXT
    const allResults = [...jsonResults, ...txtResults];

    res.json({ results: allResults });
}

// 5. Metodo para obtener la lista de videos
exports.getVideosList = async (req, res) => {

    const detectionFolder = path.join(__dirname, '..', 'detections');

    try{
        // Lectura de la carpeta de detecciones
        const files = await fs.promises.readdir(detectionFolder);

        // Filtrar por carpetas que contienen los resultados de los videos
        const videoNames = files.filter(file => {
            const fullPath = path.join(detectionFolder, file);
            return fs.statSync(fullPath).isDirectory();
        });

        if(videoNames.length === 0) {
            return res.json({ videos: [] }); // Respuesta vacía si no hay videos
        }

        return res.json({ videos: videoNames });        
    } catch (error) {
        console.error('Error al leer la carpeta de detecciones:', error);
        res.status(500).json({ error: 'Error al leer la carpeta de detecciones' });
    }
};