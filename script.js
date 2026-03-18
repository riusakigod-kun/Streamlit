// ========================================
// Dashboard Interactivo - Lógica JavaScript
// ========================================

// Variables globales
const sidebar = document.getElementById('sidebar');
const toggleBtn = document.getElementById('toggleSidebar');
const contentArea = document.getElementById('contentArea');
const pageTitle = document.getElementById('pageTitle');
const pageDescription = document.getElementById('pageDescription');

// ============ TOOGLE SIDEBAR MÓVIL ============
toggleBtn?.addEventListener('click', () => {
    sidebar.classList.toggle('open');
});

// Cerrar sidebar al hacer clic fuera
document.addEventListener('click', (e) => {
    if (!sidebar?.contains(e.target) && !toggleBtn?.contains(e.target)) {
        sidebar?.classList.remove('open');
    }
});

// ============ TOGGLE SUBMENU ============
function toggleSubmenu(element, submenuId) {
    const submenu = document.getElementById(`submenu-${submenuId}`);
    
    if (!submenu) return;

    // Alternar submenu
    submenu.classList.toggle('open');
    element.classList.toggle('active');

    // Animar icono
    const icon = element.querySelector('i');
    if (icon) {
        if (submenu.classList.contains('open')) {
            icon.style.transform = 'rotate(0deg)';
        } else {
            icon.style.transform = 'rotate(-90deg)';
        }
    }
}

// ============ SELECCIONAR MENU ============
function selectMenu(element, page) {
    // Obtener el padre más cercano que sea menu-item o submenu-item
    let menuElement = element;
    while (menuElement && !menuElement.classList.contains('menu-item') && !menuElement.classList.contains('submenu-item')) {
        menuElement = menuElement.parentElement;
    }

    if (!menuElement) return;

    // Remover activos anteriores
    document.querySelectorAll('.menu-item').forEach(item => {
        item.classList.remove('active');
    });
    document.querySelectorAll('.submenu-item').forEach(item => {
        item.classList.remove('active');
    });

    // Marcar nuevo activo
    menuElement.classList.add('active');

    // Cerrar sidebar en móvil
    if (window.innerWidth <= 768) {
        sidebar?.classList.remove('open');
    }

    // Actualizar contenido
    updateContent(page);
}

// ============ DATA PARA CONTENIDO ============
const pageData = {
    'resumen': {
        title: '📊 Resumen General',
        desc: 'Visualiza el estado general de tu flota de equipos',
        content: `
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                <div class="bg-gradient-to-br from-blue-500 to-blue-600 text-white p-6 rounded-lg">
                    <div class="text-3xl font-bold">42</div>
                    <p class="text-sm opacity-90">Equipos Totales</p>
                </div>
                <div class="bg-gradient-to-br from-green-500 to-green-600 text-white p-6 rounded-lg">
                    <div class="text-3xl font-bold">35</div>
                    <p class="text-sm opacity-90">Equipos Activos</p>
                </div>
                <div class="bg-gradient-to-br from-yellow-500 to-yellow-600 text-white p-6 rounded-lg">
                    <div class="text-3xl font-bold">5</div>
                    <p class="text-sm opacity-90">En Mantenimiento</p>
                </div>
                <div class="bg-gradient-to-br from-red-500 to-red-600 text-white p-6 rounded-lg">
                    <div class="text-3xl font-bold">2</div>
                    <p class="text-sm opacity-90">Inactivos</p>
                </div>
            </div>
            <p class="text-gray-600">Selecciona una opción en el menú para ver más detalles.</p>
        `
    },
    'ver-equipos': {
        title: '📦 Inventario de Equipos',
        desc: 'Ver todos los equipos registrados en el sistema',
        content: `
            <div class="overflow-x-auto">
                <table class="w-full border-collapse">
                    <thead>
                        <tr class="bg-gradient-to-r from-blue-500 to-blue-600 text-white">
                            <th class="p-3 text-left">ID</th>
                            <th class="p-3 text-left">Modelo</th>
                            <th class="p-3 text-left">Empresa</th>
                            <th class="p-3 text-left">Estado</th>
                            <th class="p-3 text-center">Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr class="border-b hover:bg-gray-50">
                            <td class="p-3">CM-001</td>
                            <td class="p-3">Excavadora CAT 320</td>
                            <td class="p-3">Minería XYZ</td>
                            <td class="p-3"><span class="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">Activo</span></td>
                            <td class="p-3 text-center"><a href="#" class="text-blue-600 hover:underline">Ver</a></td>
                        </tr>
                        <tr class="border-b hover:bg-gray-50">
                            <td class="p-3">CM-002</td>
                            <td class="p-3">Excavadora Komatsu PC210</td>
                            <td class="p-3">Cerro Verde</td>
                            <td class="p-3"><span class="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">Activo</span></td>
                            <td class="p-3 text-center"><a href="#" class="text-blue-600 hover:underline">Ver</a></td>
                        </tr>
                        <tr class="border-b hover:bg-gray-50">
                            <td class="p-3">CM-003</td>
                            <td class="p-3">Retroexcavadora JD 310L</td>
                            <td class="p-3">Las Bambas</td>
                            <td class="p-3"><span class="bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm">Mantenimiento</span></td>
                            <td class="p-3 text-center"><a href="#" class="text-blue-600 hover:underline">Ver</a></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        `
    },
    'equipos-activos': {
        title: '✅ Equipos Activos',
        desc: 'Equipos que se encuentran en operación',
        content: `
            <div class="space-y-4">
                <div class="bg-green-50 border-l-4 border-green-500 p-4 rounded">
                    <h3 class="font-bold text-green-900">CM-001: Excavadora CAT 320</h3>
                    <p class="text-gray-600">Empresa: Minería XYZ | Conductor: Pedro Mamani</p>
                    <p class="text-sm text-green-700 mt-2">✓ Operando desde 08:30 AM</p>
                </div>
                <div class="bg-green-50 border-l-4 border-green-500 p-4 rounded">
                    <h3 class="font-bold text-green-900">CM-002: Excavadora Komatsu PC210</h3>
                    <p class="text-gray-600">Empresa: Cerro Verde | Conductor: Félix Arce</p>
                    <p class="text-sm text-green-700 mt-2">✓ Operando desde 07:15 AM</p>
                </div>
                <div class="bg-green-50 border-l-4 border-green-500 p-4 rounded">
                    <h3 class="font-bold text-green-900">CM-004: Camión Volvo</h3>
                    <p class="text-gray-600">Empresa: Minería XYZ | Conductor: Juan Flores</p>
                    <p class="text-sm text-green-700 mt-2">✓ Operando desde 09:00 AM</p>
                </div>
            </div>
            <p class="text-gray-500 mt-4">Total: 35 equipos activos</p>
        `
    },
    'mantenimiento': {
        title: '🔧 Equipos en Mantenimiento',
        desc: 'Equipos actualmente en mantenimiento',
        content: `
            <div class="space-y-4">
                <div class="bg-yellow-50 border-l-4 border-yellow-500 p-4 rounded">
                    <h3 class="font-bold text-yellow-900">CM-003: Retroexcavadora JD 310L</h3>
                    <p class="text-gray-600">Empresa: Las Bambas</p>
                    <p class="text-sm text-yellow-700 mt-2">⏱ Mantenimiento desde: 18/03/2026</p>
                    <p class="text-sm text-yellow-700">📋 Motivo: Cambio de aceite e inspección</p>
                </div>
                <div class="bg-yellow-50 border-l-4 border-yellow-500 p-4 rounded">
                    <h3 class="font-bold text-yellow-900">CM-005: Camión MAN</h3>
                    <p class="text-gray-600">Empresa: Cerro Verde</p>
                    <p class="text-sm text-yellow-700 mt-2">⏱ Mantenimiento desde: 16/03/2026</p>
                    <p class="text-sm text-yellow-700">📋 Motivo: Reparación de neumáticos</p>
                </div>
            </div>
            <p class="text-gray-500 mt-4">Total: 5 equipos en mantenimiento</p>
        `
    },
    'conductores': {
        title: '👥 Gestión de Conductores',
        desc: 'Personal autorizado para operar equipos',
        content: `
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="bg-gradient-to-br from-blue-50 to-indigo-50 p-4 rounded-lg border border-blue-200">
                    <div class="flex items-center gap-3 mb-3">
                        <div class="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-white font-bold">PM</div>
                        <div>
                            <h3 class="font-bold">Pedro Mamani</h3>
                            <p class="text-sm text-gray-600">Operador Senior</p>
                        </div>
                    </div>
                    <p class="text-sm text-gray-600">Licencia: Vigente</p>
                    <p class="text-sm text-gray-600">Equipos: 3</p>
                </div>
                <div class="bg-gradient-to-br from-green-50 to-emerald-50 p-4 rounded-lg border border-green-200">
                    <div class="flex items-center gap-3 mb-3">
                        <div class="w-10 h-10 bg-green-500 rounded-full flex items-center justify-center text-white font-bold">FA</div>
                        <div>
                            <h3 class="font-bold">Félix Arce</h3>
                            <p class="text-sm text-gray-600">Operador</p>
                        </div>
                    </div>
                    <p class="text-sm text-gray-600">Licencia: Vigente</p>
                    <p class="text-sm text-gray-600">Equipos: 2</p>
                </div>
            </div>
            <p class="text-gray-500 mt-4">Total: 12 conductores registrados</p>
        `
    },
    'alertas': {
        title: '⚠️ Alertas Críticas',
        desc: 'Alertas activas del sistema',
        content: `
            <div class="space-y-3">
                <div class="bg-red-50 border-l-4 border-red-500 p-4 rounded">
                    <div class="flex justify-between items-start">
                        <div>
                            <h3 class="font-bold text-red-900">Mantenimiento vencido</h3>
                            <p class="text-red-700">CM-007 necesita revisión urgente</p>
                        </div>
                        <span class="bg-red-500 text-white text-xs px-2 py-1 rounded">🔴 Crítico</span>
                    </div>
                </div>
                <div class="bg-orange-50 border-l-4 border-orange-500 p-4 rounded">
                    <div class="flex justify-between items-start">
                        <div>
                            <h3 class="font-bold text-orange-900">Horas de operación altas</h3>
                            <p class="text-orange-700">CM-001 ha operado 12 horas sin descanso</p>
                        </div>
                        <span class="bg-orange-500 text-white text-xs px-2 py-1 rounded">🟠 Advertencia</span>
                    </div>
                </div>
                <div class="bg-yellow-50 border-l-4 border-yellow-500 p-4 rounded">
                    <div class="flex justify-between items-start">
                        <div>
                            <h3 class="font-bold text-yellow-900">Control de combustible</h3>
                            <p class="text-yellow-700">CM-004 combustible bajo - 15% del tanque</p>
                        </div>
                        <span class="bg-yellow-500 text-white text-xs px-2 py-1 rounded">🟡 Info</span>
                    </div>
                </div>
            </div>
            <p class="text-gray-500 mt-4">Total: 7 alertas activas</p>
        `
    },
    'linea-amarilla': {
        title: '🟡 Línea Amarilla',
        desc: 'Equipos asignados a la línea amarilla',
        content: `
            <div class="bg-yellow-50 p-6 rounded-lg border border-yellow-200">
                <h3 class="font-bold text-lg mb-4">Información General</h3>
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                    <div>
                        <p class="text-gray-600 text-sm">Equipos Totales</p>
                        <p class="text-2xl font-bold text-yellow-900">18</p>
                    </div>
                    <div>
                        <p class="text-gray-600 text-sm">En Operación</p>
                        <p class="text-2xl font-bold text-green-600">15</p>
                    </div>
                    <div>
                        <p class="text-gray-600 text-sm">En Mantenimiento</p>
                        <p class="text-2xl font-bold text-yellow-600">2</p>
                    </div>
                    <div>
                        <p class="text-gray-600 text-sm">Inactivos</p>
                        <p class="text-2xl font-bold text-red-600">1</p>
                    </div>
                </div>
                <p class="text-gray-600">Responsable: Ing. Quispe R.</p>
            </div>
        `
    },
    'linea-blanca': {
        title: '🔵 Línea Blanca',
        desc: 'Equipos asignados a la línea blanca',
        content: `
            <div class="bg-blue-50 p-6 rounded-lg border border-blue-200">
                <h3 class="font-bold text-lg mb-4">Información General</h3>
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                    <div>
                        <p class="text-gray-600 text-sm">Equipos Totales</p>
                        <p class="text-2xl font-bold text-blue-900">34</p>
                    </div>
                    <div>
                        <p class="text-gray-600 text-sm">En Operación</p>
                        <p class="text-2xl font-bold text-green-600">30</p>
                    </div>
                    <div>
                        <p class="text-gray-600 text-sm">En Mantenimiento</p>
                        <p class="text-2xl font-bold text-yellow-600">3</p>
                    </div>
                    <div>
                        <p class="text-gray-600 text-sm">Inactivos</p>
                        <p class="text-2xl font-bold text-red-600">1</p>
                    </div>
                </div>
                <p class="text-gray-600">Responsable: Ing. López M.</p>
            </div>
        `
    }
};

// ============ ACTUALIZAR CONTENIDO ============
function updateContent(page) {
    const data = pageData[page] || pageData['resumen'];

    // Actualizar header
    pageTitle.textContent = data.title;
    pageDescription.textContent = data.desc;

    // Actualizar contenido con animación
    contentArea.style.opacity = '0';
    contentArea.style.transform = 'translateY(20px)';

    setTimeout(() => {
        contentArea.innerHTML = data.content;
        contentArea.style.transition = 'all 0.4s ease-out';
        contentArea.style.opacity = '1';
        contentArea.style.transform = 'translateY(0)';
    }, 150);
}

// ============ MENU DE USUARIO ============
function openUserMenu() {
    alert('👤 Menú de Usuario\n\n• Ver Perfil\n• Configuración\n• Cerrar sesión');
}

// ============ RESPONSIVO ============
window.addEventListener('resize', function() {
    if (window.innerWidth > 768) {
        sidebar?.classList.remove('open');
    }
});

// ============ INICIALIZACIÓN ============
document.addEventListener('DOMContentLoaded', () => {
    // Cargar contenido inicial
    updateContent('resumen');

    // Asegurar que el primer menú esté activo
    const firstMenuItem = document.querySelector('.menu-item');
    if (firstMenuItem) {
        firstMenuItem.classList.add('active');
    }
});