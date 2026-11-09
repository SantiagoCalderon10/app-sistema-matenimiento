const API_URL = 'http://localhost:8000/api'; // Ajusta según el puerto de tu backend Django

// Control de pestañas expuesto globalmente
window.cambiarVista = function(vista) {
    document.getElementById('vista-personal').style.display = vista === 'personal' ? 'block' : 'none';
    document.getElementById('vista-operaciones').style.display = vista === 'operaciones' ? 'block' : 'none';
    if (vista === 'personal') cargarPersonal();
    if (vista === 'operaciones') cargarAsignaciones();
};

// Función global para mostrar alertas flotantes
function mostrarAlerta(mensaje, esError = false) {
    const alerta = document.getElementById('alerta-flotante');
    alerta.textContent = mensaje;
    alerta.style.backgroundColor = esError ? '#c62828' : '#2e7d32'; // Rojo si es error, Verde si es éxito
    
    alerta.classList.add('mostrar');
    
    setTimeout(() => {
        alerta.classList.remove('mostrar');
    }, 3000);
}

// --- MÓDULO 1: PERSONAL ---
async function cargarPersonal() {
    try {
        const res = await fetch(`${API_URL}/personal/`);
        if (!res.ok) throw new Error('Error al obtener datos');
        
        const datos = await res.json();
        const lista = document.getElementById('lista-personal');
        lista.innerHTML = '';
        
        if (datos.length === 0) {
            lista.innerHTML = '<li>No hay personal registrado.</li>';
            return;
        }

        datos.forEach(item => {
            const li = document.createElement('li');
            li.textContent = `Doc: ${item.documento_identidad} - Cargo: ${item.cargo} (Tel: ${item.telefono || 'N/A'})`;
            lista.appendChild(li);
        });
    } catch (e) {
        console.error("Error al cargar personal:", e);
        mostrarAlerta('No se pudo conectar con el servidor para cargar el personal', true);
    }
}

document.getElementById('form-personal').addEventListener('submit', async (e) => {
    e.preventDefault();
    const documento = document.getElementById('p-documento').value;
    const cargo = document.getElementById('p-cargo').value;
    const telefono = document.getElementById('p-telefono').value;

    try {
        const res = await fetch(`${API_URL}/personal/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ documento_identidad: documento, cargo, telefono })
        });
        
        if (res.ok) {
            mostrarAlerta('¡Personal registrado con éxito!');
            document.getElementById('form-personal').reset();
            cargarPersonal();
        } else {
            const errorData = await res.json();
            mostrarAlerta(`Error: ${JSON.stringify(errorData)}`, true);
        }
    } catch (err) {
        console.error("Error de red:", err);
        mostrarAlerta('Error de red al intentar registrar', true);
    }
});

// --- MÓDULO 2: OPERACIONES ---
async function cargarAsignaciones() {
    try {
        const res = await fetch(`${API_URL}/asignaciones/`);
        if (!res.ok) throw new Error('Error al cargar asignaciones');
        
        const datos = await res.json();
        const contenedor = document.getElementById('contenedor-asignaciones');
        contenedor.innerHTML = '';

        if (!datos || datos.length === 0) {
            contenedor.innerHTML = '<p>No hay asignaciones programadas actualmente.</p>';
            return;
        }

        datos.forEach(asig => {
            const div = document.createElement('div');
            div.className = 'asignacion-card';
            div.innerHTML = `
                <strong>Centro de Trabajo:</strong> ${asig.centro_trabajo_nombre || 'N/A'}<br>
                <strong>Actividad:</strong> ${asig.tipo_actividad_nombre || 'N/A'}<br>
                <strong>Operario:</strong> ${asig.operario_nombre || 'N/A'}<br><br>
                <button class="btn-accion" onclick="registrarMarca(${asig.id}, 'entrada')">Registrar Entrada</button>
                <button class="btn-accion" onclick="registrarMarca(${asig.id}, 'salida')">Registrar Salida</button>
            `;
            contenedor.appendChild(div);
        });
    } catch (e) {
        const contenedor = document.getElementById('contenedor-asignaciones');
        contenedor.innerHTML = '<p>Error al conectar con la API de operaciones.</p>';
        console.error(e);
    }
}

window.registrarMarca = async function(asignacionId, tipo) {
    try {
        const res = await fetch(`${API_URL}/asignaciones/${asignacionId}/registrar_centro/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ tipo })
        });
        
        if (res.ok) {
            mostrarAlerta(`¡Marca de ${tipo} guardada correctamente!`);
        } else {
            mostrarAlerta('Error al registrar la marca de tiempo', true);
        }
    } catch (err) {
        console.error(err);
        mostrarAlerta('Error de red al guardar la marca', true);
    }
};

// Cargar vista por defecto al iniciar
cargarPersonal();