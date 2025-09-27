// JIRA Export Mobile App - Ionic + JavaScript
// Миграция с NativeScript на Ionic Framework

class JiraExportApp {
    constructor() {
        this.jiraUrl = '';
        this.email = '';
        this.apiToken = '';
        this.isLoggedIn = false;
        this.issues = [];
        this.selectedIssues = new Set();
        this.currentStartAt = 0;
        this.maxResults = 50;
        this.filters = {
            project: '',
            status: [],
            issueType: [],
            assignee: ''
        };
        
        this.initializeApp();
    }

    async initializeApp() {
        await customElements.whenDefined('ion-app');
        this.setupEventListeners();
        this.loadSavedCredentials();
    }

    setupEventListeners() {
        // Авторизация
        document.getElementById('loginBtn').addEventListener('click', () => this.login());
        
        // Фильтры
        document.getElementById('applyFiltersBtn').addEventListener('click', () => this.applyFilters());
        
        // Задачи
        document.getElementById('refreshBtn').addEventListener('click', () => this.refreshIssues());
        document.getElementById('refresher').addEventListener('ionRefresh', (event) => this.handleRefresh(event));
        document.getElementById('infiniteScroll').addEventListener('ionInfinite', (event) => this.loadMoreIssues(event));
        
        // Действия
        document.getElementById('exportPdfBtn').addEventListener('click', () => this.exportToPdf());
        document.getElementById('selectAllBtn').addEventListener('click', () => this.selectAllIssues());
        document.getElementById('unselectAllBtn').addEventListener('click', () => this.unselectAllIssues());
        document.getElementById('openJiraBtn').addEventListener('click', () => this.openSelectedInJira());
        
        // Обработка изменения вкладок
        const tabBar = document.querySelector('ion-tab-bar');
        tabBar.addEventListener('ionTabsDidChange', (event) => this.handleTabChange(event));
    }

    loadSavedCredentials() {
        const savedJiraUrl = localStorage.getItem('jiraUrl');
        const savedEmail = localStorage.getItem('email');
        const savedApiToken = localStorage.getItem('apiToken');
        
        if (savedJiraUrl) {
            document.getElementById('jiraUrl').value = savedJiraUrl;
            this.jiraUrl = savedJiraUrl;
        }
        if (savedEmail) {
            document.getElementById('email').value = savedEmail;
            this.email = savedEmail;
        }
        if (savedApiToken) {
            document.getElementById('apiToken').value = savedApiToken;
            this.apiToken = savedApiToken;
            this.isLoggedIn = true;
            this.updateLoginStatus('Авторизован');
        }
    }

    async login() {
        const jiraUrlInput = document.getElementById('jiraUrl');
        const emailInput = document.getElementById('email');
        const apiTokenInput = document.getElementById('apiToken');
        
        this.jiraUrl = jiraUrlInput.value.trim();
        this.email = emailInput.value.trim();
        this.apiToken = apiTokenInput.value.trim();
        
        if (!this.jiraUrl || !this.email || !this.apiToken) {
            await this.showToast('Заполните все поля для авторизации', 'warning');
            return;
        }
        
        const loading = await this.showLoading('Проверка авторизации...');
        
        try {
            const response = await this.makeJiraRequest('/rest/api/2/myself');
            
            if (response.ok) {
                this.isLoggedIn = true;
                this.updateLoginStatus('Авторизован');
                
                // Сохраняем данные авторизации
                localStorage.setItem('jiraUrl', this.jiraUrl);
                localStorage.setItem('email', this.email);
                localStorage.setItem('apiToken', this.apiToken);
                
                await this.showToast('Успешная авторизация', 'success');
                
                // Переключаемся на вкладку фильтров
                const tabs = document.querySelector('ion-tabs');
                tabs.selectedTab = 'filters';
            } else {
                throw new Error('Ошибка авторизации');
            }
        } catch (error) {
            this.updateLoginStatus('Ошибка авторизации');
            await this.showToast('Ошибка авторизации. Проверьте данные.', 'danger');
        } finally {
            loading.dismiss();
        }
    }

    updateLoginStatus(status) {
        document.getElementById('loginStatus').textContent = status;
    }

    async applyFilters() {
        if (!this.isLoggedIn) {
            await this.showToast('Сначала выполните авторизацию', 'warning');
            return;
        }
        
        // Получаем значения фильтров
        this.filters.project = document.getElementById('projectKey').value.trim();
        this.filters.status = Array.from(document.getElementById('statusFilter').selectedOptions || [])
            .map(option => option.value);
        this.filters.issueType = Array.from(document.getElementById('issueTypeFilter').selectedOptions || [])
            .map(option => option.value);
        this.filters.assignee = document.getElementById('assigneeFilter').value.trim();
        
        // Сбрасываем пагинацию
        this.currentStartAt = 0;
        this.issues = [];
        
        await this.loadIssues();
        
        // Переключаемся на вкладку задач
        const tabs = document.querySelector('ion-tabs');
        tabs.selectedTab = 'issues';
    }

    async loadIssues(append = false) {
        if (!append) {
            this.currentStartAt = 0;
            this.issues = [];
        }
        
        const loading = await this.showLoading('Загрузка задач...');
        
        try {
            const jql = this.buildJQL();
            const url = `/rest/api/2/search?jql=${encodeURIComponent(jql)}&startAt=${this.currentStartAt}&maxResults=${this.maxResults}&fields=key,summary,status,issuetype,assignee,priority,created,updated`;
            
            const response = await this.makeJiraRequest(url);
            const data = await response.json();
            
            if (append) {
                this.issues = [...this.issues, ...data.issues];
            } else {
                this.issues = data.issues;
            }
            
            this.renderIssues();
            this.currentStartAt += this.maxResults;
            
            // Обновляем infinite scroll
            const infiniteScroll = document.getElementById('infiniteScroll');
            if (data.issues.length < this.maxResults) {
                infiniteScroll.disabled = true;
            } else {
                infiniteScroll.disabled = false;
            }
            
        } catch (error) {
            await this.showToast('Ошибка загрузки задач', 'danger');
        } finally {
            loading.dismiss();
        }
    }

    buildJQL() {
        let jqlParts = [];
        
        if (this.filters.project) {
            jqlParts.push(`project = "${this.filters.project}"`);
        }
        
        if (this.filters.status.length > 0) {
            const statusList = this.filters.status.map(s => `"${s}"`).join(', ');
            jqlParts.push(`status IN (${statusList})`);
        }
        
        if (this.filters.issueType.length > 0) {
            const typeList = this.filters.issueType.map(t => `"${t}"`).join(', ');
            jqlParts.push(`issuetype IN (${typeList})`);
        }
        
        if (this.filters.assignee) {
            jqlParts.push(`assignee = "${this.filters.assignee}"`);
        }
        
        return jqlParts.length > 0 ? jqlParts.join(' AND ') : 'order by created DESC';
    }

    renderIssues() {
        const issuesList = document.getElementById('issuesList');
        
        if (!this.currentStartAt) {
            issuesList.innerHTML = '';
        }
        
        this.issues.slice(this.currentStartAt - this.maxResults).forEach(issue => {
            const listItem = this.createIssueListItem(issue);
            issuesList.appendChild(listItem);
        });
        
        this.updateSelectedCount();
    }

    createIssueListItem(issue) {
        const item = document.createElement('ion-item');
        item.setAttribute('button', '');
        item.innerHTML = `
            <ion-checkbox slot="start" data-issue-key="${issue.key}" ${this.selectedIssues.has(issue.key) ? 'checked' : ''}></ion-checkbox>
            <ion-label>
                <h2>${issue.key}: ${issue.fields.summary}</h2>
                <p>Статус: ${issue.fields.status.name}</p>
                <p>Тип: ${issue.fields.issuetype.name}</p>
                <p>Исполнитель: ${issue.fields.assignee ? issue.fields.assignee.displayName : 'Не назначен'}</p>
            </ion-label>
            <ion-badge slot="end" color="${this.getPriorityColor(issue.fields.priority)}">${issue.fields.priority ? issue.fields.priority.name : 'Без приоритета'}</ion-badge>
        `;
        
        // Обработчик клика по чекбоксу
        const checkbox = item.querySelector('ion-checkbox');
        checkbox.addEventListener('ionChange', (event) => {
            if (event.detail.checked) {
                this.selectedIssues.add(issue.key);
            } else {
                this.selectedIssues.delete(issue.key);
            }
            this.updateSelectedCount();
        });
        
        return item;
    }

    getPriorityColor(priority) {
        if (!priority) return 'medium';
        
        switch (priority.name.toLowerCase()) {
            case 'highest':
            case 'critical':
                return 'danger';
            case 'high':
                return 'warning';
            case 'medium':
                return 'primary';
            case 'low':
                return 'secondary';
            case 'lowest':
                return 'light';
            default:
                return 'medium';
        }
    }

    async refreshIssues() {
        await this.loadIssues();
    }

    async handleRefresh(event) {
        await this.loadIssues();
        event.target.complete();
    }

    async loadMoreIssues(event) {
        await this.loadIssues(true);
        event.target.complete();
    }

    selectAllIssues() {
        this.issues.forEach(issue => {
            this.selectedIssues.add(issue.key);
        });
        this.updateCheckboxes();
        this.updateSelectedCount();
    }

    unselectAllIssues() {
        this.selectedIssues.clear();
        this.updateCheckboxes();
        this.updateSelectedCount();
    }

    updateCheckboxes() {
        document.querySelectorAll('ion-checkbox[data-issue-key]').forEach(checkbox => {
            const issueKey = checkbox.getAttribute('data-issue-key');
            checkbox.checked = this.selectedIssues.has(issueKey);
        });
    }

    updateSelectedCount() {
        document.getElementById('selectedCount').textContent = this.selectedIssues.size;
    }

    async exportToPdf() {
        if (this.selectedIssues.size === 0) {
            await this.showToast('Выберите задачи для экспорта', 'warning');
            return;
        }
        
        const loading = await this.showLoading('Экспорт в PDF...');
        
        try {
            const selectedIssuesList = this.issues.filter(issue => this.selectedIssues.has(issue.key));
            
            // Отправляем запрос на backend для генерации PDF
            const response = await fetch('/api/export/pdf', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    issues: selectedIssuesList,
                    jiraUrl: this.jiraUrl
                })
            });
            
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `jira-export-${new Date().toISOString().split('T')[0]}.pdf`;
                a.click();
                window.URL.revokeObjectURL(url);
                
                await this.showToast('PDF успешно экспортирован', 'success');
            } else {
                throw new Error('Ошибка экспорта');
            }
        } catch (error) {
            await this.showToast('Ошибка экспорта в PDF', 'danger');
        } finally {
            loading.dismiss();
        }
    }

    async openSelectedInJira() {
        if (this.selectedIssues.size === 0) {
            await this.showToast('Выберите задачи для открытия', 'warning');
            return;
        }
        
        // Открываем каждую выбранную задачу в новой вкладке
        this.selectedIssues.forEach(issueKey => {
            const url = `${this.jiraUrl}/browse/${issueKey}`;
            window.open(url, '_blank');
        });
    }

    async makeJiraRequest(endpoint) {
        const url = `${this.jiraUrl}${endpoint}`;
        const auth = btoa(`${this.email}:${this.apiToken}`);
        
        return fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': `Basic ${auth}`,
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        });
    }

    async showLoading(message) {
        const loading = document.createElement('ion-loading');
        loading.message = message;
        document.body.appendChild(loading);
        await loading.present();
        return loading;
    }

    async showToast(message, color = 'dark') {
        const toast = document.createElement('ion-toast');
        toast.message = message;
        toast.duration = 3000;
        toast.color = color;
        toast.position = 'bottom';
        document.body.appendChild(toast);
        await toast.present();
        return toast;
    }

    handleTabChange(event) {
        const selectedTab = event.detail.tab;
        
        // Обновляем данные при переключении на определенные вкладки
        if (selectedTab === 'issues' && this.isLoggedIn && this.issues.length === 0) {
            this.loadIssues();
        }
    }
}

// Инициализация приложения после загрузки DOM
document.addEventListener('DOMContentLoaded', () => {
    new JiraExportApp();
});