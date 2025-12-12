document.addEventListener('DOMContentLoaded', function() {
    // Elementos del DOM
    const form = document.getElementById('passwordRequestForm');
    const successMessage = document.getElementById('successMessage');
    const errorMessage = document.getElementById('errorMessage');
    const backToLoginBtn = document.getElementById('backToLogin');
    const newRequestBtn = document.getElementById('newRequest');
    const tryAgainBtn = document.getElementById('tryAgain');
    
    // Campos del formulario
    const userIdentifier = document.getElementById('userIdentifier');
    const userEmail = document.getElementById('userEmail');
    const requestReason = document.getElementById('requestReason');
    
    // Elementos para mostrar errores
    const userIdentifierError = document.getElementById('userIdentifierError');
    const userEmailError = document.getElementById('userEmailError');
    const requestReasonError = document.getElementById('requestReasonError');
    
    // Datos del administrador (simulados)
    const adminId = document.getElementById('adminId').value;
    const adminName = document.getElementById('adminName').value;
    const adminEmail = document.getElementById('adminEmail').value;
    
    // Función para validar el formulario
    function validateForm() {
        let isValid = true;
        
        // Resetear mensajes de error
        userIdentifierError.textContent = '';
        userEmailError.textContent = '';
        requestReasonError.textContent = '';
        
        // Validar identificador de usuario
        if (!userIdentifier.value.trim()) {
            userIdentifierError.textContent = 'El identificador de usuario es obligatorio';
            isValid = false;
        }
        
        // Validar correo electrónico
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!userEmail.value.trim()) {
            userEmailError.textContent = 'El correo electrónico es obligatorio';
            isValid = false;
        } else if (!emailPattern.test(userEmail.value)) {
            userEmailError.textContent = 'Por favor, introduce un correo electrónico válido';
            isValid = false;
        }
        
        // Validar motivo de la solicitud
        if (!requestReason.value.trim()) {
            requestReasonError.textContent = 'El motivo de la solicitud es obligatorio';
            isValid = false;
        } else if (requestReason.value.trim().length < 10) {
            requestReasonError.textContent = 'Por favor, proporciona una explicación más detallada (mínimo 10 caracteres)';
            isValid = false;
        }
        
        return isValid;
    }
    
    // Función para mostrar mensaje de éxito
    function showSuccessMessage() {
        form.classList.add('hidden');
        errorMessage.classList.add('hidden');
        successMessage.classList.remove('hidden');
    }
    
    // Función para mostrar mensaje de error
    function showErrorMessage() {
        form.classList.add('hidden');
        successMessage.classList.add('hidden');
        errorMessage.classList.remove('hidden');
    }
    
    // Función para mostrar formulario
    function showForm() {
        form.classList.remove('hidden');
        successMessage.classList.add('hidden');
        errorMessage.classList.add('hidden');
    }
    
    // Función para resetear formulario
    function resetForm() {
        form.reset();
        userIdentifierError.textContent = '';
        userEmailError.textContent = '';
        requestReasonError.textContent = '';
    }
    
    // Función para simular envío al servidor
    function submitFormToServer(formData) {
        // Simulamos una solicitud HTTP con un retraso
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                // Simulamos un 90% de probabilidad de éxito
                const success = Math.random() > 0.1;
                
                if (success) {
                    // Simulamos respuesta exitosa
                    resolve({
                        status: 'success',
                        message: 'Solicitud procesada correctamente',
                        adminName: adminName,
                        adminEmail: adminEmail
                    });
                } else {
                    // Simulamos error del servidor
                    reject({
                        status: 'error',
                        message: 'Error en el servidor al procesar la solicitud'
                    });
                }
            }, 1500); // 1.5 segundos de simulación
        });
    }
    
    // Manejar envío del formulario
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Validar formulario
        if (!validateForm()) {
            return;
        }
        
        // Deshabilitar botones durante el envío
        const submitButton = form.querySelector('button[type="submit"]');
        const originalText = submitButton.innerHTML;
        submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Enviando...';
        submitButton.disabled = true;
        
        // Crear objeto con los datos del formulario
        const formData = {
            userIdentifier: userIdentifier.value,
            userEmail: userEmail.value,
            requestReason: requestReason.value,
            adminId: adminId,
            adminName: adminName,
            adminEmail: adminEmail,
            timestamp: new Date().toISOString()
        };
        
        try {
            // Enviar datos al servidor (simulado)
            await submitFormToServer(formData);
            
            // Mostrar mensaje de éxito
            showSuccessMessage();
            
            // En un caso real, aquí podrías enviar los datos a un servidor
            console.log('Datos enviados al servidor:', formData);
            
        } catch (error) {
            // Mostrar mensaje de error
            showErrorMessage();
            console.error('Error al enviar la solicitud:', error);
        } finally {
            // Restaurar botón
            submitButton.innerHTML = originalText;
            submitButton.disabled = false;
        }
    });
    
    // Manejar clic en "Volver a Iniciar Sesión"
    backToLoginBtn.addEventListener('click', function() {
        // En un caso real, redirigiría a la página de login
        alert('Redirigiendo a la página de inicio de sesión...');
        // window.location.href = 'login.html'; // Descomenta para redirigir
    });
    
    // Manejar clic en "Nueva Solicitud"
    newRequestBtn.addEventListener('click', function() {
        resetForm();
        showForm();
    });
    
    // Manejar clic en "Intentar de nuevo"
    tryAgainBtn.addEventListener('click', function() {
        showForm();
    });
    
    // Validación en tiempo real para mejorar la experiencia de usuario
    userIdentifier.addEventListener('blur', function() {
        if (!userIdentifier.value.trim()) {
            userIdentifierError.textContent = 'El identificador de usuario es obligatorio';
        } else {
            userIdentifierError.textContent = '';
        }
    });
    
    userEmail.addEventListener('blur', function() {
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!userEmail.value.trim()) {
            userEmailError.textContent = 'El correo electrónico es obligatorio';
        } else if (!emailPattern.test(userEmail.value)) {
            userEmailError.textContent = 'Por favor, introduce un correo electrónico válido';
        } else {
            userEmailError.textContent = '';
        }
    });
    
    requestReason.addEventListener('blur', function() {
        if (!requestReason.value.trim()) {
            requestReasonError.textContent = 'El motivo de la solicitud es obligatorio';
        } else if (requestReason.value.trim().length < 10) {
            requestReasonError.textContent = 'Por favor, proporciona una explicación más detallada (mínimo 10 caracteres)';
        } else {
            requestReasonError.textContent = '';
        }
    });
});