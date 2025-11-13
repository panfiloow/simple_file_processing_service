// Main JavaScript utilities for File Processing Service

class App {
    constructor() {
        this.init();
    }

    init() {
        this.setupLogout();
        this.setupGlobalHandlers();
        this.checkAuthentication();
    }

    // Проверка аутентификации на страницах, требующих авторизации
    checkAuthentication() {
        const protectedPages = ['/dashboard', '/upload'];
        const currentPath = window.location.pathname;
        
        if (protectedPages.includes(currentPath) && !this.isAuthenticated()) {
            window.location.href = '/login';
            return;
        }

        if (this.isAuthenticated()) {
            this.updateUIForAuthenticatedUser();
        }
    }

    isAuthenticated() {
        return !!localStorage.getItem('access_token');
    }

    async updateUIForAuthenticatedUser() {
        try {
            const user = await this.getCurrentUser();
            if (user) {
                this.updateUserInfoInUI(user);
            }
        } catch (error) {
            console.error('Failed to get user info:', error);
            this.handleAuthError();
        }
    }

    async getCurrentUser() {
        const token = localStorage.getItem('access_token');
        if (!token) return null;

        try {
            const response = await fetch('/api/auth/me', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                return await response.json();
            } else {
                throw new Error('Failed to get user info');
            }
        } catch (error) {
            throw error;
        }
    }

    updateUserInfoInUI(user) {
        // Обновляем навигацию для авторизованного пользователя
        const navItems = document.querySelectorAll('.nav-item');
        navItems.forEach(item => {
            if (item.querySelector('.nav-link[href="/login"]') || 
                item.querySelector('.nav-link[href="/register"]')) {
                item.style.display = 'none';
            }
        });

        // Добавляем информацию о пользователе в шаблон
        const userElements = document.querySelectorAll('[data-user-email]');
        userElements.forEach(element => {
            element.textContent = user.email;
        });
    }

    setupLogout() {
        document.addEventListener('click', (e) => {
            if (e.target.id === 'logoutBtn' || e.target.closest('#logoutBtn')) {
                e.preventDefault();
                this.logout();
            }
        });
    }

    async logout() {
        const refreshToken = localStorage.getItem('refresh_token');
        
        if (refreshToken) {
            try {
                await fetch('/api/auth/logout', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                    },
                    body: JSON.stringify({ refresh_token: refreshToken })
                });
            } catch (error) {
                console.error('Logout error:', error);
            }
        }

        // Очищаем localStorage и перенаправляем на главную
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/';
    }

    setupGlobalHandlers() {
        // Глобальная обработка ошибок авторизации
        window.addEventListener('unauthorized', () => {
            this.handleAuthError();
        });

        // Глобальная обработка сетевых ошибок
        window.addEventListener('online', () => {
            this.showGlobalAlert('Соединение восстановлено', 'success');
        });

        window.addEventListener('offline', () => {
            this.showGlobalAlert('Отсутствует интернет-соединение', 'warning');
        });
    }

    handleAuthError() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        
        if (window.location.pathname !== '/login') {
            window.location.href = '/login';
        }
    }

    showGlobalAlert(message, type = 'info') {
        // Создаем глобальный контейнер для алертов, если его нет
        let alertContainer = document.getElementById('globalAlertContainer');
        if (!alertContainer) {
            alertContainer = document.createElement('div');
            alertContainer.id = 'globalAlertContainer';
            alertContainer.className = 'position-fixed top-0 start-50 translate-middle-x mt-3 z-3';
            alertContainer.style.zIndex = '1060';
            document.body.appendChild(alertContainer);
        }

        const alertId = 'alert-' + Date.now();
        const alertHTML = `
            <div id="${alertId}" class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;

        alertContainer.insertAdjacentHTML('beforeend', alertHTML);

        // Автоматически скрываем через 5 секунд
        setTimeout(() => {
            const alert = document.getElementById(alertId);
            if (alert) {
                alert.remove();
            }
        }, 5000);
    }

    // Утилиты для работы с API
    async apiCall(url, options = {}) {
        const token = localStorage.getItem('access_token');
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                ...(token && { 'Authorization': `Bearer ${token}` }),
                ...options.headers
            }
        };

        const response = await fetch(url, { ...defaultOptions, ...options });

        if (response.status === 401) {
            window.dispatchEvent(new Event('unauthorized'));
            throw new Error('Unauthorized');
        }

        return response;
    }

    // Утилиты для форматирования
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('ru-RU', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    // Утилиты для валидации
    validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    validatePassword(password) {
        return password.length >= 6;
    }
}

// Вспомогательные функции
const Utils = {
    // Дебаунс для поиска и фильтрации
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

    // Генерация случайного ID
    generateId() {
        return Math.random().toString(36).substr(2, 9);
    },

    // Копирование текста в буфер обмена
    async copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);
            return true;
        } catch (err) {
            // Fallback для старых браузеров
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            return true;
        }
    },

    // Показ тостов/уведомлений
    showToast(message, type = 'info') {
        // Реализация тостов может быть добавлена при необходимости
        console.log(`[${type.toUpperCase()}] ${message}`);
    }
};

// Инициализация приложения при загрузке DOM
document.addEventListener('DOMContentLoaded', () => {
    window.app = new App();
    window.utils = Utils;
});

// Экспорт для использования в других модулях
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { App, Utils };
}