import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
// Importamos los estilos de Bootstrap para que se vea lindo desde el principio
import 'bootstrap/dist/css/bootstrap.min.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
