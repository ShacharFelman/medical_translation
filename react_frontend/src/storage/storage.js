export function readFromStorage(key) {
    return localStorage.getItem(key);
}

export function writeToStorage(key, data) {
    localStorage.setItem(key, data);
}
