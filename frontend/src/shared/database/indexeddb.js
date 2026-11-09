class LocalDatabase {
    constructor() {
        this.dbName = 'LocativoOfflineDB';
        this.version = 1;
    }

    async abrir() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open(this.dbName, this.version);
            
            request.onerror = () => reject(request.error);
            request.onsuccess = () => resolve(request.result);
            
            request.onupgradeneeded = (event) => {
                const db = event.target.result;
                if (!db.objectStoreNames.contains('programacion')) {
                    db.createObjectStore('programacion', { keyPath: 'id' });
                }
                if (!db.objectStoreNames.contains('cola_eventos')) {
                    db.createObjectStore('cola_eventos', { keyPath: 'uuid' });
                }
                if (!db.objectStoreNames.contains('fotografias')) {
                    db.createObjectStore('fotografias', { keyPath: 'id', autoIncrement: true });
                }
            };
        });
    }

    async guardarEnCola(evento) {
        const db = await this.abrir();
        return new Promise((resolve, reject) => {
            const transaction = db.transaction(['cola_eventos'], 'readwrite');
            const store = transaction.objectStore('cola_eventos');
            const request = store.put(evento);
            
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    async obtenerEventosPendientes() {
        const db = await this.abrir();
        return new Promise((resolve, reject) => {
            const transaction = db.transaction(['cola_eventos'], 'readonly');
            const store = transaction.objectStore('cola_eventos');
            const request = store.getAll();
            
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    async eliminarEventoCola(uuid) {
        const db = await this.abrir();
        return new Promise((resolve, reject) => {
            const transaction = db.transaction(['cola_eventos'], 'readwrite');
            const store = transaction.objectStore('cola_eventos');
            const request = store.delete(uuid);
            
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }
}

export const dbLocal = new LocalDatabase();