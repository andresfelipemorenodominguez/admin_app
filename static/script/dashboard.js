// script.js - Versión optimizada y modular
// ============================================
// CONSTANTES Y CONFIGURACIÓN
// ============================================

const CONFIG = {
    selectors: {
        sidebar: '.sidebar',
        mainContent: '.main-content',
        navLinks: '.nav-link',
        profileBtn: '#profile-btn',
        userProfile: '.user-profile',
        currentDate: '#current-date',
        quickActionBtns: '.quick-action-btn',
        viewAllBtn: '.view-all-btn'
    },
    
    sectionMap: {
        'Inicio': 'inicio-section',
        'Agregar Estudiante': 'agregar-estudiante-section',
        'Agregar Profesor': 'agregar-profesor-section',
        'Reportes': 'reportes-section'
    },
    
    quickActions: {
        'agregar-estudiante': { section: 'agregar-estudiante-section', navIndex: 1 },
        'agregar-profesor': { section: 'agregar-profesor-section', navIndex: 2 },
        'reportes': { section: 'reportes-section', navIndex: 3 }
    },
    
    validation: {
        emailRegex: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
        passwordMinLength: 8,
        nameMinLength: 5
    }
};

// ============================================
// DATOS DE EJEMPLO PARA LAS TABLAS
// ============================================

const SAMPLE_DATA = {
    estudiantes: [
        {
            id: 'EST001',
            nombre: 'María González López',
            email: 'maria.gonzalez@ejemplo.com',
            grado: '10° Secundaria',
            grupo: 'A',
            fechaRegistro: '2024-02-15',
            estado: 'activo'
        },
        {
            id: 'EST002',
            nombre: 'Carlos Rodríguez Martínez',
            email: 'carlos.rodriguez@ejemplo.com',
            grado: '11° Secundaria',
            grupo: 'B',
            fechaRegistro: '2024-01-20',
            estado: 'activo'
        },
        {
            id: 'EST003',
            nombre: 'Ana Sánchez Pérez',
            email: 'ana.sanchez@ejemplo.com',
            grado: '9° Secundaria',
            grupo: 'C',
            fechaRegistro: '2024-03-05',
            estado: 'activo'
        },
        {
            id: 'EST004',
            nombre: 'Luis Fernández García',
            email: 'luis.fernandez@ejemplo.com',
            grado: '10° Secundaria',
            grupo: 'A',
            fechaRegistro: '2024-02-28',
            estado: 'inactivo'
        },
        {
            id: 'EST005',
            nombre: 'Laura Martínez Díaz',
            email: 'laura.martinez@ejemplo.com',
            grado: '8° Secundaria',
            grupo: 'B',
            fechaRegistro: '2024-03-10',
            estado: 'activo'
        },
        {
            id: 'EST006',
            nombre: 'Pedro Gómez Ruiz',
            email: 'pedro.gomez@ejemplo.com',
            grado: '11° Secundaria',
            grupo: 'A',
            fechaRegistro: '2024-01-15',
            estado: 'activo'
        },
        {
            id: 'EST007',
            nombre: 'Sofía Hernández Castro',
            email: 'sofia.hernandez@ejemplo.com',
            grado: '10° Secundaria',
            grupo: 'C',
            fechaRegistro: '2024-02-10',
            estado: 'activo'
        },
        {
            id: 'EST008',
            nombre: 'Javier Torres Romero',
            email: 'javier.torres@ejemplo.com',
            grado: '9° Secundaria',
            grupo: 'B',
            fechaRegistro: '2024-03-01',
            estado: 'inactivo'
        }
    ],
    
    profesores: [
        {
            id: 'PROF001',
            nombre: 'Carlos Rodríguez Martínez',
            email: 'carlos.rodriguez@institucion.edu.co',
            asignaturas: ['Matemáticas', 'Física'],
            telefono: '3101234567',
            fechaRegistro: '2024-01-10',
            estado: 'activo'
        },
        {
            id: 'PROF002',
            nombre: 'Ana María Sánchez Pérez',
            email: 'ana.sanchez@institucion.edu.co',
            asignaturas: ['Español', 'Literatura'],
            telefono: '3209876543',
            fechaRegistro: '2024-02-05',
            estado: 'activo'
        },
        {
            id: 'PROF003',
            nombre: 'Luis Alberto Fernández',
            email: 'luis.fernandez@institucion.edu.co',
            asignaturas: ['Ciencias Naturales', 'Biología'],
            telefono: '3155551234',
            fechaRegistro: '2024-01-25',
            estado: 'activo'
        },
        {
            id: 'PROF004',
            nombre: 'María Elena García Torres',
            email: 'maria.garcia@institucion.edu.co',
            asignaturas: ['Inglés', 'Francés'],
            telefono: '3187778888',
            fechaRegistro: '2024-03-01',
            estado: 'activo'
        },
        {
            id: 'PROF005',
            nombre: 'Roberto Jiménez López',
            email: 'roberto.jimenez@institucion.edu.co',
            asignaturas: ['Educación Física', 'Deportes'],
            telefono: '3123334444',
            fechaRegistro: '2024-02-20',
            estado: 'licencia'
        }
    ]
};

// ============================================
// MÓDULO DE UTILIDADES
// ============================================

const Utils = {
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    generatePassword(length = 12) {
        const uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        const lowercase = 'abcdefghijklmnopqrstuvwxyz';
        const numbers = '0123456789';
        const symbols = '!@#$%^&*';
        
        let password = '';
        password += uppercase.charAt(Math.floor(Math.random() * uppercase.length));
        password += numbers.charAt(Math.floor(Math.random() * numbers.length));
        password += symbols.charAt(Math.floor(Math.random() * symbols.length));
        
        const allChars = uppercase + lowercase + numbers + symbols;
        for (let i = 3; i < length; i++) {
            password += allChars.charAt(Math.floor(Math.random() * allChars.length));
        }
        
        return password.split('').sort(() => Math.random() - 0.5).join('');
    },

    formatDate(date = new Date()) {
        const options = { 
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        };
        return date.toLocaleDateString('es-ES', options);
    },

    formatDateShort(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('es-ES', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric'
        });
    },

    showError(fieldId, message) {
        const errorElement = document.getElementById(`${fieldId}-error`);
        const inputElement = document.getElementById(fieldId);
        
        if (errorElement) {
            errorElement.textContent = message;
            errorElement.classList.add('show');
        }
        
        if (inputElement) {
            inputElement.classList.remove('success');
            inputElement.classList.add('error');
        }
    },

    clearError(fieldId) {
        const errorElement = document.getElementById(`${fieldId}-error`);
        const inputElement = document.getElementById(fieldId);
        
        if (errorElement) {
            errorElement.textContent = '';
            errorElement.classList.remove('show');
        }
        
        if (inputElement) {
            inputElement.classList.remove('error');
        }
    },

    markAsValid(fieldId) {
        const inputElement = document.getElementById(fieldId);
        if (inputElement) {
            inputElement.classList.remove('error');
            inputElement.classList.add('success');
            this.clearError(fieldId);
        }
    },

    filterTableData(data, searchTerm, fields) {
        if (!searchTerm.trim()) return data;
        
        const term = searchTerm.toLowerCase();
        return data.filter(item => {
            return fields.some(field => {
                const value = item[field];
                if (Array.isArray(value)) {
                    return value.some(v => v.toLowerCase().includes(term));
                }
                return String(value).toLowerCase().includes(term);
            });
        });
    }
};

// ============================================
// MÓDULO DE GESTIÓN DE TABLAS
// ============================================

class TableManager {
    constructor(tableId, data, options = {}) {
        this.tableId = tableId;
        this.originalData = [...data];
        this.filteredData = [...data];
        this.options = options;
        this.searchInputId = options.searchInputId || '';
        this.counterId = options.counterId || '';
        this.infoId = options.infoId || '';
        
        this.init();
    }

    init() {
        this.renderTable();
        this.setupSearch();
        this.updateCounters();
    }

    renderTable() {
        const tableBody = document.querySelector(`#${this.tableId} tbody`);
        if (!tableBody) return;

        if (this.filteredData.length === 0) {
            const colSpan = document.querySelector(`#${this.tableId} thead tr`).children.length;
            tableBody.innerHTML = `
                <tr class="no-results">
                    <td colspan="${colSpan}">
                        <i class="fas fa-search"></i>
                        No se encontraron resultados
                    </td>
                </tr>
            `;
            return;
        }

        tableBody.innerHTML = this.filteredData.map(item => this.renderRow(item)).join('');
    }

    renderRow(item) {
        // Este método debe ser sobrescrito por las clases hijas
        return '';
    }

    setupSearch() {
        if (!this.searchInputId) return;
        
        const searchInput = document.getElementById(this.searchInputId);
        if (!searchInput) return;
        
        const searchHandler = Utils.debounce(() => {
            this.filterData(searchInput.value);
            this.renderTable();
            this.updateCounters();
        }, 300);
        
        searchInput.addEventListener('input', searchHandler);
    }

    filterData(searchTerm) {
        const searchFields = this.options.searchFields || ['nombre', 'email', 'id'];
        this.filteredData = Utils.filterTableData(this.originalData, searchTerm, searchFields);
    }

    updateCounters() {
        if (this.counterId) {
            const counterElement = document.getElementById(this.counterId);
            if (counterElement) {
                counterElement.textContent = `Total: ${this.filteredData.length} ${this.options.itemName || 'items'}`;
            }
        }
        
        if (this.infoId) {
            const infoElement = document.getElementById(this.infoId);
            if (infoElement) {
                const total = this.originalData.length;
                const shown = this.filteredData.length;
                
                const totalSpan = infoElement.querySelector(`#${this.options.totalSpanId}`);
                const shownSpan = infoElement.querySelector(`#${this.options.shownSpanId}`);
                
                if (totalSpan) totalSpan.textContent = total;
                if (shownSpan) shownSpan.textContent = shown;
            }
        }
    }

    refreshData(newData) {
        this.originalData = [...newData];
        this.filteredData = [...newData];
        this.renderTable();
        this.updateCounters();
    }
}

// ============================================
// TABLA DE ESTUDIANTES
// ============================================

class EstudiantesTableManager extends TableManager {
    constructor() {
        super('tabla-estudiantes', SAMPLE_DATA.estudiantes, {
            searchInputId: 'search-estudiantes',
            counterId: 'estudiantes-counter',
            infoId: 'estudiantes-info',
            itemName: 'estudiantes',
            totalSpanId: 'estudiantes-total',
            shownSpanId: 'estudiantes-mostrados',
            searchFields: ['nombre', 'email', 'id', 'grado', 'grupo']
        });
    }

    renderRow(estudiante) {
        const estadoClass = estudiante.estado === 'activo' ? 'badge-success' : 'badge-warning';
        const estadoText = estudiante.estado === 'activo' ? 'Activo' : 'Inactivo';
        
        return `
            <tr>
                <td>
                    <span class="table-badge badge-primary">${estudiante.id}</span>
                </td>
                <td class="nombre-cell">${estudiante.nombre}</td>
                <td class="email-cell">${estudiante.email}</td>
                <td class="grado-cell">
                    <span class="table-badge">${estudiante.grado}</span>
                </td>
                <td class="grupo-cell">
                    <span class="table-badge">${estudiante.grupo}</span>
                </td>
                <td>${Utils.formatDateShort(estudiante.fechaRegistro)}</td>
                <td>
                    <div class="table-actions">
                        <button class="action-btn view" title="Ver detalles">
                            <i class="fas fa-eye"></i>
                        </button>
                        <button class="action-btn edit" title="Editar">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="action-btn delete" title="Eliminar">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `;
    }
}

// ============================================
// TABLA DE PROFESORES
// ============================================

class ProfesoresTableManager extends TableManager {
    constructor() {
        super('tabla-profesores', SAMPLE_DATA.profesores, {
            searchInputId: 'search-profesores',
            counterId: 'profesores-counter',
            infoId: 'profesores-info',
            itemName: 'profesores',
            totalSpanId: 'profesores-total',
            shownSpanId: 'profesores-mostrados',
            searchFields: ['nombre', 'email', 'id', 'asignaturas', 'telefono']
        });
    }

    renderRow(profesor) {
        const estadoClass = profesor.estado === 'activo' ? 'badge-success' : 
                           profesor.estado === 'licencia' ? 'badge-warning' : 'badge-primary';
        const estadoText = profesor.estado === 'activo' ? 'Activo' : 
                          profesor.estado === 'licencia' ? 'En licencia' : 'Inactivo';
        
        const asignaturasText = profesor.asignaturas.length > 2 
            ? `${profesor.asignaturas.slice(0, 2).join(', ')}...`
            : profesor.asignaturas.join(', ');
        
        return `
            <tr>
                <td>
                    <span class="table-badge badge-primary">${profesor.id}</span>
                </td>
                <td class="nombre-cell">${profesor.nombre}</td>
                <td class="email-cell">${profesor.email}</td>
                <td class="asignaturas-cell" title="${profesor.asignaturas.join(', ')}">
                    ${asignaturasText}
                </td>
                <td>${profesor.telefono}</td>
                <td>${Utils.formatDateShort(profesor.fechaRegistro)}</td>
                <td>
                    <div class="table-actions">
                        <button class="action-btn view" title="Ver detalles">
                            <i class="fas fa-eye"></i>
                        </button>
                        <button class="action-btn edit" title="Editar">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="action-btn delete" title="Eliminar">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `;
    }
}

// ============================================
// MÓDULO DE VALIDACIÓN
// ============================================

const Validator = {
    email(email) {
        if (!email) return { valid: false, message: 'El correo electrónico es obligatorio' };
        if (!CONFIG.validation.emailRegex.test(email)) {
            return { valid: false, message: 'Ingresa un correo electrónico válido' };
        }
        return { valid: true };
    },

    required(value, fieldName, minLength = 0) {
        if (!value || value.trim() === '') {
            return { valid: false, message: 'Este campo es obligatorio' };
        }
        
        if (minLength > 0 && value.length < minLength) {
            return { 
                valid: false, 
                message: `Debe tener al menos ${minLength} caracteres` 
            };
        }
        
        return { valid: true };
    },

    password(password) {
        const minLength = CONFIG.validation.passwordMinLength;
        const validation = this.required(password, 'contraseña', minLength);
        
        if (!validation.valid) return validation;
        
        if (!/(?=.*[A-Z])/.test(password)) {
            return { valid: false, message: 'Debe contener al menos una mayúscula' };
        }
        
        if (!/\d/.test(password)) {
            return { valid: false, message: 'Debe contener al menos un número' };
        }
        
        return { valid: true };
    },

    calculatePasswordStrength(password) {
        let score = 0;
        const criteria = [
            password.length >= 8,
            /[A-Z]/.test(password),
            /\d/.test(password),
            /[!@#$%^&*]/.test(password)
        ];
        
        criteria.forEach(criterion => criterion && score++);
        
        if (score === 4) return { level: 'strong', percentage: 100, color: 'var(--success)' };
        if (score >= 2) return { level: 'medium', percentage: 66, color: 'var(--warning)' };
        return { level: 'weak', percentage: 33, color: 'var(--error)' };
    }
};

// ============================================
// GESTOR DE MODALES
// ============================================

class ModalManager {
    constructor(modalId, options = {}) {
        this.modal = document.getElementById(modalId);
        this.closeBtn = options.closeBtnId ? 
            document.getElementById(options.closeBtnId) : null;
        this.onClose = options.onClose || null;
        this.onOpen = options.onOpen || null;
        
        this.init();
    }

    init() {
        if (!this.modal) return;
        
        if (this.closeBtn) {
            this.closeBtn.addEventListener('click', () => this.close());
        }
        
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) this.close();
        });
        
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.isOpen()) this.close();
        });
    }

    open() {
        if (this.modal) {
            this.modal.classList.add('active');
            document.body.style.overflow = 'hidden';
            if (this.onOpen) this.onOpen();
        }
    }

    close() {
        if (this.modal) {
            this.modal.classList.remove('active');
            document.body.style.overflow = 'auto';
            if (this.onClose) this.onClose();
        }
    }

    isOpen() {
        return this.modal?.classList.contains('active') || false;
    }
}

// ============================================
// GESTOR DE FORMULARIOS BASE
// ============================================

class BaseFormHandler {
    constructor(formId, options = {}) {
        this.form = document.getElementById(formId);
        this.options = options;
        this.fields = options.fields || {};
        this.initialize();
    }

    initialize() {
        if (!this.form) return;
        
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        this.setupEventListeners();
        this.setupRealTimeValidation();
    }

    setupEventListeners() {
        // Método a ser sobrescrito por subclases
    }

    setupRealTimeValidation() {
        // Método a ser sobrescrito por subclases
    }

    handleSubmit(e) {
        e.preventDefault();
        
        if (this.validateForm()) {
            this.processForm();
        } else {
            this.showFormError('Por favor, corrige los campos marcados con error.');
        }
    }

    validateForm() {
        let isValid = true;
        
        Object.entries(this.fields).forEach(([fieldId, config]) => {
            const input = document.getElementById(fieldId);
            if (!input) return;
            
            const value = input.value.trim();
            const validation = config.validator(value);
            
            if (!validation.valid) {
                Utils.showError(fieldId, validation.message);
                isValid = false;
            } else {
                Utils.markAsValid(fieldId);
            }
        });
        
        return isValid;
    }

    processForm() {
        const formData = new FormData(this.form);
        const data = Object.fromEntries(formData.entries());
        
        console.log('Datos del formulario:', data);
        this.showSuccessMessage();
        this.resetForm();
    }

    resetForm() {
        this.form.reset();
        
        this.form.querySelectorAll('.form-input, .form-select').forEach(input => {
            input.classList.remove('error', 'success');
        });
        
        this.form.querySelectorAll('.error-message').forEach(error => {
            error.classList.remove('show');
            error.textContent = '';
        });
    }

    showSuccessMessage(message = null) {
        const formMessage = document.getElementById(`${this.form.id}-message`);
        if (!formMessage) return;
        
        const defaultMessage = '¡Registro exitoso! Los datos han sido procesados correctamente.';
        
        formMessage.className = 'form-message success';
        formMessage.innerHTML = `
            <div class="form-message-content">
                <div class="form-message-icon">
                    <i class="fas fa-check-circle"></i>
                </div>
                <div class="form-message-text">
                    <h4 class="form-message-title">¡Operación exitosa!</h4>
                    <p class="form-message-details">${message || defaultMessage}</p>
                </div>
            </div>
        `;
        
        setTimeout(() => {
            formMessage.className = 'form-message';
            formMessage.innerHTML = '';
        }, 5000);
    }

    showFormError(message) {
        const formMessage = document.getElementById(`${this.form.id}-message`);
        if (!formMessage) return;
        
        formMessage.className = 'form-message error';
        formMessage.innerHTML = `
            <div class="form-message-content">
                <div class="form-message-icon">
                    <i class="fas fa-exclamation-circle"></i>
                </div>
                <div class="form-message-text">
                    <h4 class="form-message-title">Error de Validación</h4>
                    <p class="form-message-details">${message}</p>
                </div>
            </div>
        `;
        
        const firstError = this.form.querySelector('.error');
        if (firstError) firstError.focus();
    }

    setupPasswordToggle(passwordInputId, toggleBtnId) {
        const toggleBtn = document.getElementById(toggleBtnId);
        const passwordInput = document.getElementById(passwordInputId);
        
        if (toggleBtn && passwordInput) {
            toggleBtn.addEventListener('click', () => {
                const isVisible = passwordInput.type === 'text';
                passwordInput.type = isVisible ? 'password' : 'text';
                
                const icon = toggleBtn.querySelector('i');
                icon.classList.toggle('fa-eye', isVisible);
                icon.classList.toggle('fa-eye-slash', !isVisible);
            });
        }
    }

    updatePasswordStrength(passwordInputId, strengthFillId, strengthLabelId) {
        const passwordInput = document.getElementById(passwordInputId);
        const strengthFill = document.getElementById(strengthFillId);
        const strengthLabel = document.getElementById(strengthLabelId);
        
        if (!passwordInput || !strengthFill || !strengthLabel) return;
        
        const password = passwordInput.value;
        const strength = Validator.calculatePasswordStrength(password);
        
        strengthFill.style.width = `${strength.percentage}%`;
        strengthFill.style.backgroundColor = strength.color;
        strengthLabel.textContent = this.getStrengthText(strength.level);
        strengthLabel.style.color = strength.color;
    }

    getStrengthText(level) {
        const texts = {
            weak: 'Débil',
            medium: 'Moderada',
            strong: 'Fuerte'
        };
        return texts[level] || 'Débil';
    }
}

// ============================================
// FORMULARIO DE ESTUDIANTE
// ============================================

class StudentFormHandler extends BaseFormHandler {
    constructor() {
        super('estudiante-form', {
            fields: {
                'nombre-completo': {
                    validator: (v) => Validator.required(v, 'nombre completo', 5)
                },
                'tipo-documento': {
                    validator: (v) => Validator.required(v, 'tipo de documento')
                },
                'numero-documento': {
                    validator: (v) => Validator.required(v, 'número de documento')
                },
                'correo-electronico': {
                    validator: (v) => Validator.email(v)
                },
                'grado': {
                    validator: (v) => Validator.required(v, 'grado')
                },
                'grupo': {
                    validator: (v) => Validator.required(v, 'grupo')
                },
                'contrasena': {
                    validator: (v) => Validator.password(v)
                }
            }
        });
    }

    setupEventListeners() {
        super.setupEventListeners();
        
        // Botón cancelar
        const cancelBtn = document.getElementById('cancel-form-btn');
        if (cancelBtn) {
            cancelBtn.addEventListener('click', () => {
                if (confirm('¿Estás seguro de que deseas cancelar? Se perderán todos los datos ingresados.')) {
                    this.resetForm();
                    this.updatePasswordStrength('contrasena', 'password-strength-fill', 'password-strength-label');
                }
            });
        }
        
        // Generar contraseña
        const generateBtn = document.getElementById('generate-password-btn');
        if (generateBtn) {
            generateBtn.addEventListener('click', () => {
                const password = Utils.generatePassword();
                document.getElementById('contrasena').value = password;
                this.updatePasswordStrength('contrasena', 'password-strength-fill', 'password-strength-label');
                Utils.markAsValid('contrasena');
            });
        }
        
        // Toggle contraseña
        this.setupPasswordToggle('contrasena', 'toggle-estudiante-password');
    }

    setupRealTimeValidation() {
        const passwordInput = document.getElementById('contrasena');
        const emailInput = document.getElementById('correo-electronico');
        const docInput = document.getElementById('numero-documento');
        
        if (passwordInput) {
            const updateStrength = Utils.debounce(() => {
                this.updatePasswordStrength('contrasena', 'password-strength-fill', 'password-strength-label');
            }, 300);
            
            passwordInput.addEventListener('input', updateStrength);
        }
        
        if (emailInput) {
            emailInput.addEventListener('blur', () => {
                const validation = Validator.email(emailInput.value);
                if (validation.valid) {
                    Utils.markAsValid('correo-electronico');
                } else {
                    Utils.showError('correo-electronico', validation.message);
                }
            });
        }
        
        if (docInput) {
            docInput.addEventListener('input', () => {
                docInput.value = docInput.value.replace(/[^0-9]/g, '');
            });
        }
    }
}

// ============================================
// FORMULARIO DE PROFESOR
// ============================================

class ProfessorFormHandler extends BaseFormHandler {
    constructor() {
        super('profesor-form', {
            fields: {
                'profesor-nombre-completo': {
                    validator: (v) => Validator.required(v, 'nombre completo', 5)
                },
                'profesor-tipo-documento': {
                    validator: (v) => Validator.required(v, 'tipo de documento')
                },
                'profesor-numero-documento': {
                    validator: (v) => Validator.required(v, 'número de documento')
                },
                'profesor-correo-electronico': {
                    validator: (v) => Validator.email(v)
                },
                'profesor-telefono': {
                    validator: (v) => Validator.required(v, 'teléfono')
                },
                'profesor-asignaturas': {
                    validator: (v) => this.validateAsignaturas(v)
                },
                'profesor-contrasena': {
                    validator: (v) => Validator.password(v)
                }
            }
        });
    }

    validateAsignaturas(value) {
        if (!value || value.length === 0) {
            return { valid: false, message: 'Debe seleccionar al menos una asignatura' };
        }
        return { valid: true };
    }

    setupEventListeners() {
        super.setupEventListeners();
        
        // Botón cancelar
        const cancelBtn = document.getElementById('cancel-profesor-form-btn');
        if (cancelBtn) {
            cancelBtn.addEventListener('click', () => {
                if (confirm('¿Estás seguro de que deseas cancelar? Se perderán todos los datos ingresados.')) {
                    this.resetForm();
                    this.updatePasswordStrength('profesor-contrasena', 'profesor-password-strength-fill', 'profesor-password-strength-label');
                }
            });
        }
        
        // Generar contraseña
        const generateBtn = document.getElementById('generate-profesor-password-btn');
        if (generateBtn) {
            generateBtn.addEventListener('click', () => {
                const password = Utils.generatePassword();
                document.getElementById('profesor-contrasena').value = password;
                this.updatePasswordStrength('profesor-contrasena', 'profesor-password-strength-fill', 'profesor-password-strength-label');
                Utils.markAsValid('profesor-contrasena');
            });
        }
        
        // Toggle contraseña
        this.setupPasswordToggle('profesor-contrasena', 'toggle-profesor-password');
        
        // Actualizar contador de asignaturas
        const asignaturasSelect = document.getElementById('profesor-asignaturas');
        if (asignaturasSelect) {
            asignaturasSelect.addEventListener('change', () => {
                this.updateAsignaturasCount();
            });
        }
    }

    updateAsignaturasCount() {
        const select = document.getElementById('profesor-asignaturas');
        const counter = document.getElementById('asignaturas-seleccionadas');
        
        if (select && counter) {
            const selectedCount = Array.from(select.selectedOptions).length;
            counter.textContent = `${selectedCount} asignatura${selectedCount !== 1 ? 's' : ''} seleccionada${selectedCount !== 1 ? 's' : ''}`;
        }
    }

    setupRealTimeValidation() {
        const passwordInput = document.getElementById('profesor-contrasena');
        const emailInput = document.getElementById('profesor-correo-electronico');
        
        if (passwordInput) {
            const updateStrength = Utils.debounce(() => {
                this.updatePasswordStrength('profesor-contrasena', 'profesor-password-strength-fill', 'profesor-password-strength-label');
            }, 300);
            
            passwordInput.addEventListener('input', updateStrength);
        }
        
        if (emailInput) {
            emailInput.addEventListener('blur', () => {
                const validation = Validator.email(emailInput.value);
                if (validation.valid) {
                    Utils.markAsValid('profesor-correo-electronico');
                } else {
                    Utils.showError('profesor-correo-electronico', validation.message);
                }
            });
        }
        
        this.updateAsignaturasCount();
    }
}

// ============================================
// GESTOR DE NAVEGACIÓN
// ============================================

class NavigationManager {
    constructor() {
        this.currentSection = 'inicio-section';
        this.init();
    }

    init() {
        this.setupNavigation();
        this.setupQuickActions();
    }

    setupNavigation() {
        document.addEventListener('click', (e) => {
            const navLink = e.target.closest('.nav-link');
            if (navLink) {
                e.preventDefault();
                this.navigateToSection(navLink);
            }
        });
    }

    navigateToSection(navLink) {
        const sectionName = navLink.querySelector('.nav-text').textContent;
        const targetSectionId = CONFIG.sectionMap[sectionName];
        
        if (!targetSectionId) return;
        
        // Actualizar navegación activa
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        navLink.classList.add('active');
        
        // Ocultar todas las secciones
        document.querySelectorAll('.content-section').forEach(section => {
            section.classList.remove('active');
        });
        
        // Mostrar sección objetivo
        const targetSection = document.getElementById(targetSectionId);
        if (targetSection) {
            targetSection.classList.add('active');
            this.currentSection = targetSectionId;
        }
    }

    setupQuickActions() {
        document.addEventListener('click', (e) => {
            const quickActionBtn = e.target.closest('.quick-action-btn');
            if (quickActionBtn) {
                const target = quickActionBtn.dataset.target;
                this.handleQuickAction(target);
            }
        });
    }

    handleQuickAction(action) {
        const config = CONFIG.quickActions[action];
        if (!config) return;
        
        // Ocultar todas las secciones
        document.querySelectorAll('.content-section').forEach(section => {
            section.classList.remove('active');
        });
        
        // Mostrar sección objetivo
        const targetSection = document.getElementById(config.section);
        if (targetSection) {
            targetSection.classList.add('active');
            this.currentSection = config.section;
        }
        
        // Actualizar navegación activa
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        
        const navLinks = document.querySelectorAll(CONFIG.selectors.navLinks);
        if (navLinks[config.navIndex]) {
            navLinks[config.navIndex].classList.add('active');
        }
    }
}

// ============================================
// GESTOR DE INTERFAZ
// ============================================

class UIManager {
    constructor() {
        this.modals = {};
        this.init();
    }

    init() {
        this.setupModals();
        this.updateCurrentDate();
        this.setupResizeHandler();
    }

    setupModals() {
        // Modal de perfil
        this.modals.profile = new ModalManager('profile-modal', {
            closeBtnId: 'modal-close-btn'
        });
        
        // Modal de editar perfil
        this.modals.editProfile = new ModalManager('edit-profile-modal', {
            closeBtnId: 'edit-modal-close-btn'
        });
        
        // Modal de cambiar contraseña
        this.modals.changePassword = new ModalManager('change-password-modal', {
            closeBtnId: 'change-password-close-btn'
        });
        
        // Configurar interacciones entre modales
        this.setupModalInteractions();
        
        // Abrir modal de perfil
        document.querySelector(CONFIG.selectors.profileBtn)?.addEventListener('click', 
            () => this.modals.profile.open());
        
        document.querySelector(CONFIG.selectors.userProfile)?.addEventListener('click', 
            () => this.modals.profile.open());
        
        // Logout
        document.getElementById('logout-btn')?.addEventListener('click', () => {
            if (confirm('¿Estás seguro de que deseas cerrar sesión?')) {
                alert('Sesión cerrada. Redirigiendo a la página de inicio...');
                this.modals.profile.close();
            }
        });
    }

    setupModalInteractions() {
        // Editar perfil
        document.querySelector('.edit-btn')?.addEventListener('click', () => {
            this.modals.profile.close();
            setTimeout(() => this.modals.editProfile.open(), 150);
        });
        
        // Cambiar contraseña
        document.querySelector('.password-btn')?.addEventListener('click', () => {
            this.modals.profile.close();
            setTimeout(() => {
                this.modals.changePassword.open();
                document.getElementById('current-password')?.focus();
            }, 150);
        });
        
        // Cancelar edición
        document.getElementById('cancel-edit-btn')?.addEventListener('click', () => {
            this.modals.editProfile.close();
            setTimeout(() => this.modals.profile.open(), 150);
        });
        
        // Cancelar cambio de contraseña
        document.getElementById('cancel-password-btn')?.addEventListener('click', () => {
            this.modals.changePassword.close();
            setTimeout(() => this.modals.profile.open(), 150);
        });
    }

    updateCurrentDate() {
        const dateElement = document.getElementById('current-date');
        if (dateElement) {
            dateElement.textContent = Utils.formatDate();
        }
    }

    setupResizeHandler() {
        const adjustLayout = () => {
            const sidebar = document.querySelector(CONFIG.selectors.sidebar);
            const mainContent = document.querySelector(CONFIG.selectors.mainContent);
            
            if (!sidebar || !mainContent) return;
            
            if (window.innerWidth > 768) {
                mainContent.style.marginLeft = `${sidebar.offsetWidth}px`;
            } else {
                mainContent.style.marginLeft = '0';
            }
        };
        
        adjustLayout();
        window.addEventListener('resize', Utils.debounce(adjustLayout, 250));
    }
}

// ============================================
// INICIALIZACIÓN DE LA APLICACIÓN
// ============================================

class App {
    constructor() {
        this.ui = null;
        this.navigation = null;
        this.forms = {};
        this.tables = {};
    }

    init() {
        try {
            // Inicializar componentes
            this.ui = new UIManager();
            this.navigation = new NavigationManager();
            
            // Inicializar formularios
            this.forms.student = new StudentFormHandler();
            this.forms.professor = new ProfessorFormHandler();
            
            // Inicializar tablas (solo si estamos en la sección de reportes o la navegamos)
            this.initializeTables();
            
            console.log('Aplicación inicializada correctamente');
            console.log('Componentes cargados:', {
                ui: !!this.ui,
                navigation: !!this.navigation,
                forms: Object.keys(this.forms),
                tables: Object.keys(this.tables)
            });
            
        } catch (error) {
            console.error('Error al inicializar la aplicación:', error);
        }
    }

    initializeTables() {
        // Inicializar tablas de reportes
        this.tables.estudiantes = new EstudiantesTableManager();
        this.tables.profesores = new ProfesoresTableManager();
    }
}

// ============================================
// EJECUCIÓN
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    const app = new App();
    app.init();
});