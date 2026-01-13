import { useEffect, useState } from 'react'
import axios from 'axios'
import Swal from 'sweetalert2' // Alertas lindas
import './index.css' // Importamos los estilos espaciales

function App() {
  const [episodios, setEpisodios] = useState([])

  // Función para obtener los datos del Backend (Python)
  const cargarEpisodios = async () => {
    try {
      const respuesta = await axios.get('http://localhost:5000/api/episodios')
      setEpisodios(respuesta.data)
    } catch (error) {
      console.error('Error al conectar:', error)
      Swal.fire(
        'Error de Conexión',
        'No se pudo contactar al sistema central.',
        'error',
      )
    }
  }

  // Carga inicial y auto-refresco cada 10 segundos para ver cambios de estado
  useEffect(() => {
    cargarEpisodios()
    const intervalo = setInterval(cargarEpisodios, 10000)
    return () => clearInterval(intervalo)
  }, [])

  // PUNTO 2: Reservar (Bloquea por 4 min en Redis)
  const reservar = async id => {
    try {
      // Usamos concatenación para evitar errores de comillas
      const url = 'http://localhost:5000/api/reservar/' + id
      const respuesta = await axios.post(url)

      Swal.fire({
        title: 'Reserva Confirmada',
        text: 'Tienes 4 minutos para confirmar el pago.',
        icon: 'success',
        timer: 3000,
        showConfirmButton: false,
        background: '#161b22',
        color: '#fff',
      })
      cargarEpisodios()
    } catch (error) {
      const mensaje = error.response?.data?.mensaje || 'Error al reservar'
      Swal.fire({
        title: 'No disponible',
        text: mensaje,
        icon: 'warning',
        background: '#161b22',
        color: '#fff',
      })
    }
  }

  // PUNTO 3: Pagar (Confirma alquiler por 24hs)
  const pagar = async (id, precio) => {
    try {
      const url = 'http://localhost:5000/api/pagar/' + id
      const respuesta = await axios.post(url, { monto: precio })

      Swal.fire({
        title: '¡Acceso Concedido!',
        text: 'Disfruta el capítulo por 24 horas.',
        icon: 'success',
        background: '#161b22',
        color: '#fff',
        confirmButtonColor: '#198754',
      })
      cargarEpisodios()
    } catch (error) {
      Swal.fire({
        title: 'Error de Pago',
        text: error.response?.data?.mensaje || 'No se pudo procesar',
        icon: 'error',
        background: '#161b22',
        color: '#fff',
      })
      cargarEpisodios()
    }
  }

  // Función auxiliar para dibujar las etiquetas de estado
  const renderEstado = estado => {
    switch (estado) {
      case 'Disponible':
        return (
          <span className="badge badge-status bg-success text-white">
            DISPONIBLE
          </span>
        )
      case 'Reservado':
        return (
          <span className="badge badge-status bg-warning text-dark">
            RESERVADO ⏳
          </span>
        )
      case 'Alquilado':
        return (
          <span className="badge badge-status bg-danger text-white">
            ALQUILADO 🔒
          </span>
        )
      default:
        return <span className="badge bg-secondary">{estado}</span>
    }
  }

  return (
    <div className="container py-5">
      <header className="text-center mb-5">
        <h1
          className="display-3 fw-bold text-warning mb-2"
          style={{ textShadow: '0 0 15px rgba(247, 185, 38, 0.6)' }}>
          THE MANDALORIAN
        </h1>
        {/* Subtítulo en blanco para que se lea sobre el fondo negro */}
        <p className="lead text-light opacity-75 fw-bold">
          Sistema de Alquiler Intergaláctico
        </p>
      </header>

      <div className="row g-4">
        {episodios.map(epi => (
          <div key={epi.id} className="col-md-6 col-lg-4 col-xl-3">
            {/* Tarjeta con estilo personalizado */}
            <div
              className={`card card-mandalorian h-100 ${
                epi.estado === 'Reservado' ? 'border-warning' : ''
              }`}>
              <div className="card-body d-flex flex-column">
                {/* Título y Precio */}
                <div className="d-flex justify-content-between align-items-start mb-3">
                  {/* CORRECCIÓN: Título en BLANCO (text-white) para que se vea sobre fondo oscuro */}
                  <h5 className="card-title text-dark fw-bold mb-0 pe-2">
                    {epi.titulo}
                  </h5>
                  <span className="badge bg-dark border border-secondary text-warning fs-6">
                    ${epi.precio}
                  </span>
                </div>

                {/* Estado Visual */}
                <div className="mb-4">
                  <span className="text-secondary small text-uppercase me-2 fw-bold">
                    Estado:
                  </span>
                  {renderEstado(epi.estado)}
                </div>

                {/* Botones de Acción Lógica */}
                <div className="mt-auto">
                  {epi.estado === 'Disponible' ? (
                    <button
                      className="btn btn-mando w-100"
                      onClick={() => reservar(epi.id)}>
                      RESERVAR
                    </button>
                  ) : epi.estado === 'Reservado' ? (
                    <div className="d-grid gap-2">
                      <div className="text-center small text-warning mb-1">
                        <i>⏱️ Tienes 4 min para confirmar</i>
                      </div>
                      <button
                        className="btn btn-success fw-bold shadow"
                        onClick={() => pagar(epi.id, epi.precio)}>
                        CONFIRMAR PAGO
                      </button>
                    </div>
                  ) : (
                    <button
                      className="btn btn-outline-secondary w-100"
                      disabled
                      style={{ opacity: 0.5 }}>
                      NO DISPONIBLE
                    </button>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default App
