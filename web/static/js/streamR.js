class FileExplorer {
    constructor() {
        this.currentPath = '';
        this.isGridView = true;
        this.container = document.getElementById('gridContainer');
        this.viewToggle = document.getElementById('viewToggle');
        this.driveSelect = document.getElementById('driveSelect');
        this.searchBar = document.querySelector('.search-bar');

        this.initializeEventListeners();
        this.loadDrives();
    }

    initializeEventListeners() {
        this.viewToggle.addEventListener('click', () => this.toggleView());
        this.driveSelect.addEventListener('change', () => this.loadCurrentPath());
        this.searchBar.addEventListener('input', () => this.handleSearch());

        // Navigate with sidebar
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', () => {
                const path = item.dataset.path;
                this.navigateTo(path);
            });
        });
    }

    async loadDrives() {
        try {
            const response = await fetch('http://localhost:5000/drives');
            const drives = await response.json();

            this.driveSelect.innerHTML = drives.map(drive =>
                `<option value="${drive.path}">${drive.name} (${drive.path})</option>`
            ).join('');

            this.loadCurrentPath();
        } catch (error) {
            console.error('Failed to load drives:', error);
        }
    }

    async loadCurrentPath() {
        const drive = this.driveSelect.value;
        const path = this.currentPath ? `${drive}/${this.currentPath}` : drive;

        try {
            const response = await fetch(`http://localhost:5000/files?path=${encodeURIComponent(path)}`);
            const files = await response.json();
            this.displayFiles(files);
        } catch (error) {
            console.error('Failed to load files:', error);
        }
    }

    displayFiles(files) {
        this.container.className = this.isGridView ? 'grid-container' : 'list-container';

        const content = files.map(file => this.isGridView ?
            this.createGridItem(file) :
            this.createListItem(file)
        ).join('');

        this.container.innerHTML = content;

        // Add click handlers
        this.container.querySelectorAll('.grid-item, .list-item').forEach(item => {
            item.addEventListener('click', (e) => this.handleItemClick(e, item));
        });
    }

    createGridItem(file) {
        const icon = file.type === 'folder' ? '📁' : this.getFileIcon(file.name);
        return `
            <div class="grid-item" data-path="${file.path}">
                <div class="icon">${icon}</div>
                <div class="name">${file.name}</div>
            </div>
        `;
    }

    createListItem(file) {
        const icon = file.type === 'folder' ? '📁' : this.getFileIcon(file.name);
        return `
            <div class="list-item" data-path="${file.path}">
                <div class="icon">${icon}</div>
                <div class="name">${file.name}</div>
                <div class="type">${file.type}</div>
                <div class="size">${this.formatSize(file.size)}</div>
            </div>
        `;
    }

    getFileIcon(filename) {
        const ext = filename.split('.').pop().toLowerCase();
        const icons = {
            txt: '📄',
            pdf: '📕',
            doc: '📘',
            docx: '📘',
            xls: '📗',
            xlsx: '📗',
            jpg: '🖼️',
            jpeg: '🖼️',
            png: '🖼️',
            mp3: '🎵',
            mp4: '🎥',
            default: '📄'
        };
        return icons[ext] || icons.default;
    }

    formatSize(bytes) {
        if (bytes === 0) return '0 B';
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return `${(bytes / Math.pow(k, i)).toFixed(2)} ${sizes[i]}`;
    }

    toggleView() {
        this.isGridView = !this.isGridView;
        this.loadCurrentPath();
    }

    async handleItemClick(event, item) {
        const path = item.dataset.path;
        await this.navigateTo(path);
    }

    async navigateTo(path) {
        this.currentPath = path;
        await this.loadCurrentPath();
    }

    async handleSearch() {
        const searchTerm = this.searchBar.value;
        if (searchTerm.length < 3) {
            this.loadCurrentPath();
            return;
        }

        try {
            const response = await fetch(`http://localhost:5000/search?term=${encodeURIComponent(searchTerm)}&path=${encodeURIComponent(this.currentPath)}`);
            const files = await response.json();
            this.displayFiles(files);
        } catch (error) {
            console.error('Failed to search:', error);
        }
    }
}

// Initialize the file explorer when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new FileExplorer();
});