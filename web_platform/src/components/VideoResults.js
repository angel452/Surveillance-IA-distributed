import React, { useCallback, useEffect } from "react";
import axios from "axios";
import './VideoResults.css';

const VideoResults = ({ videoName, setFinalResults, scanning }) => {
  const [results, setResults] = React.useState(null);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState(null);
  const [visibleFiles, setVisibleFiles] = React.useState({});

  const [selectedObjects, setSelectedObjects] = React.useState([]);
  const [selectedColors, setSelectedColors] = React.useState([]);
  const [selectedEnvironmentType, setSelectedEnvironmentType] = React.useState([]);
  const [selectedProximity, setSelectedProximity] = React.useState([]);
  const [priorityObjects, setPriorityObjects] = React.useState([]);

  // Funcion para alternar la visibilidad de los objetos de un arcihvo
  const toggleVisibility = (fileName) => {
    setVisibleFiles(prevState => ({
      ...prevState,
      [fileName]: !prevState[fileName],  // Cambiar la visibilidad de este archivo
    }));
  };

  // Funcion para manejar el clic enlos botones de filtro
  const toggleSelection = (category, value) => {
    switch (category) {
      case "objects":
        setSelectedObjects(prevState =>
          prevState.includes(value)
            ? prevState.filter(item => item !== value)
            : [...prevState, value]
        );
        break;
      case "colors":
        setSelectedColors(prevState =>
          prevState.includes(value)
            ? prevState.filter(item => item !== value)
            : [...prevState, value]
        );
        break;
      case "environmentTypes":
        setSelectedEnvironmentType(prevState =>
          prevState.includes(value)
            ? prevState.filter(item => item !== value)
            : [...prevState, value]
        );
        break;
      case "proximity":
        setSelectedProximity(prevState =>
          prevState.includes(value)
            ? prevState.filter(item => item !== value)
            : [...prevState, value]
        );
        break;
      case "priorityObjects":  // Nuevo caso para Priority Object
        setPriorityObjects(prevState =>
          prevState.includes(value)
            ? prevState.filter(item => item !== value)  // Si está seleccionado, desmarcarlo
            : [...prevState, value]  // Si no está seleccionado, marcarlo como priority
        );
        break;
      default:
        break;
    }
  };

  const handleMakeQuery = () => {
    // Tipo 1: Si solo selectedEnvironmentType tiene un valor (y no hay objetos, colores o proximidad seleccionados), entonces será tipo 1.
    // Tipo 2: Si se seleccionaron alguno de los objetos, colores o proximidad y no hay un selectedEnvironmentType, entonces será tipo 2.
      // Puedes escoger entre :
        // Objeto
        // Objeto color
        // Objeto proximidad
        // Objeto color proximidad 
    // Tipo 3: Si el selectedObjects contiene algún valor y también el priorityObjects está seleccionado, entonces será tipo 3.

    let queryType = 1;  // Por defecto, será tipo 1

    if(selectedObjects.length > 0 || selectedColors.length > 0 || selectedProximity.length > 0) {
      if(selectedEnvironmentType.length === 0) {
        queryType = 2;
      }
    }

    if(selectedObjects.length > 0 && priorityObjects.length > 0) {
      queryType = 3;
    }

    const queryData = {
      type: queryType,
      video_name: videoName,
      environment_type: selectedEnvironmentType || null,
      object_name: selectedObjects.length > 0 ? selectedObjects.join(",") : null,
      color: selectedColors.length > 0 ? selectedColors.join(",") : null,
      proximity: selectedProximity || null,
    }

    console.log("Query data:", queryData);

    // Realizamos la solicitud POST a la ruta de make_query en el backend
    axios.post('http://localhost:5000/api/videos/make_query', queryData).then(response => {
      console.log("Results from API:", response.data);
      setFinalResults(response.data);
    })
    .catch(error => {
      console.error("Error executing query:", error);
      alert("Error executing query");
    });
  };

  const fetchResults = useCallback(async () => {
    try {
      const response = await axios.get(`http://localhost:5000/api/videos/results/${videoName}`);
      setResults(response.data.results);
    } catch (error) {
      console.error('Error fetching results:', error);
      setError(error);
    } finally {
      setLoading(false);
    }
  }, [videoName]);

  // const fetchResults = async () => {
  //   try {
  //       const response = await axios.get(`http://localhost:5000/api/videos/results/${videoName}`);
  //       setResults(response.data.results);
  //     } catch (error) {
  //       console.error('Error fetching results:', error);
  //       setError(error);
  //     } finally {
  //       setLoading(false);
  //     }
  // };

  useEffect(() => {
    // Realizar la consulta solo si el escaneo termino (scanning es falso)
    if(!scanning && videoName) {
      fetchResults();
    }
    else {
        console.error('No video name provided');
    }
  }, [videoName, scanning, fetchResults]);

  if (scanning) {
    return <p>Scanning in progress...</p>; // Mientras se escanea, mostramos un mensaje
  }
  
  if (loading) {
    return <p>Loading...</p>;
  }
  
  if (error) {
    return <p>Error: {error}</p>;
  }

  return (
    <div>
      {results && results.length > 0 ? (
        <div>
          <table>
            <thead>
              <tr>
                <th>Video Name</th>
                <th>Environment Type</th>
                <th>Objects Detected</th>
              </tr>
            </thead>
            <tbody>
              {results.map((result, index) => {
                if (result.type === "json") {
                  return (
                    <tr key={index}>
                      <td>{result.fileName}</td>
                      <td>
                        {/* Convertir el Environment Type en botones */}
                        <button
                          onClick={() =>
                            toggleSelection("environmentTypes", result.scene?.environment_type)
                          }
                          style={{
                            backgroundColor: selectedEnvironmentType.includes(result.scene?.environment_type)
                              ? "#279644"   // Seleccionado
                              : "#0665BD",  // No seleccionado
                            fontWeight: "bold"
                          }}
                        >
                          {result.scene?.environment_type}
                        </button>
                      </td>
                      <td>
                        {/* Recorremos los archivos de detección relacionados con este video */}
                        {results
                          .filter((r) => r.type === "txt")
                          .map((txtResult, txtIndex) => {
                            if (txtResult.fileName.includes("detections")) {
                              const detections = txtResult.content
                                .split("\n")
                                .filter((line) => line.trim() !== "");

                              // Determinar si este archivo debe ser visible
                              const isVisible = visibleFiles[txtResult.fileName];

                              // Determinar el segundo donde se tomo el frame: EJ: detections_13 -> Segundo 13
                              const second = txtResult.fileName.match(/detections_(\d+)/)[1];

                              return (
                                <div key={txtIndex}>
                                  {/* Boton de visibilidad */}
                                  <button onClick={() => toggleVisibility(txtResult.fileName)}>
                                    Segundo {second}:
                                  </button>

                                  {isVisible && (
                                    <ul>
                                      {detections.map((line, lineIndex) => {
                                        const parts = line.split(",");
                                        const objectName = parts[0].trim();

                                        // Buscar el bloque de color entre paréntesis y extraer los números RGB
                                        //const colorStr1 = parts[5].trim(); // (65
                                        //const colorStr2 = parts[6].trim(); // 87
                                        //const colorStr3 = parts[7].trim(); // 87)
                                        //const colorStr = `${colorStr1},${colorStr2},${colorStr3}`;
                                        //const colorMatches = colorStr.match(/\((\d+)\s*,\s*(\d+)\s*,\s*(\d+)\)/);                                        const color = colorMatches
                                        //  ? `rgb(${colorMatches[1]}, ${colorMatches[2]}, ${colorMatches[3]})`
                                        //  : "black";
                                        const color = parts[5].trim();

                                        // Extraer la proximidad (debe estar en la posición 8)
                                        const proximity = parts[6]?.trim();

                                        return (
                                          <li key={lineIndex}>
                                            {/* Convertir el nombre del objeto y otros valores en botones */}
                                            <button
                                              onClick={() => toggleSelection("objects", objectName)}
                                              style={{
                                                backgroundColor: selectedObjects.includes(objectName)
                                                ? "#279644"   // Seleccionado
                                                : "#0665BD",  // No seleccionado
                                                fontWeight: "bold"
                                              }}
                                            >
                                              {objectName}
                                            </button>
                                            |
                                            <button
                                              onClick={() => toggleSelection("colors", color)}
                                              style={{
                                                backgroundColor: selectedColors.includes(color)
                                                ? "#279644"   // Seleccionado
                                                : `${color}`, // No seleccionado
                                                fontWeight: "bold"
                                              }}
                                            >
                                              {color}
                                            </button>
                                            |
                                            <button
                                              onClick={() => toggleSelection("proximity", proximity)}
                                              style={{
                                                backgroundColor: selectedProximity.includes(proximity)
                                                ? "#279644"   // Seleccionado
                                                : "#0665BD",  // No seleccionado
                                                fontWeight: "bold"
                                              }}
                                            >
                                              {proximity}
                                            </button>
                                            |
                                            <button
                                              className="priority-button"
                                              onClick={() => toggleSelection("priorityObjects", objectName)}  // Usamos "priorityObjects"
                                              style={{
                                                backgroundColor: priorityObjects.includes(objectName) 
                                                  ? "#279644"
                                                  : "#0665BD",  // Cambiar color según selección
                                                  fontWeight: "bold"
                                              }}
                                            >
                                              Priority Object
                                            </button>
                                          </li>
                                        );
                                      })}
                                    </ul>
                                  )}
                                </div>
                              );
                            }
                            return null;
                          })}
                      </td>
                    </tr>
                  );
                }
                return null;
              })}
            </tbody>
          </table>

          {/* Botón para hacer la consulta */}
          <button onClick={handleMakeQuery}>Make Query</button>
        </div>
      ) : (
        <p>No results found</p>
      )}
    </div>
  );
} 

export default VideoResults;