import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api/v1/";

const api = axios.create({
    baseURL: API_URL,
    headers: {
        "Content-Type": "application/json"
    }
});

// 🔹 Función para obtener museos con el token directamente
export const getMuseos = async () => {
    try {
        const response = await api.get("museos", {
            headers: {
                Authorization: `Bearer bckHyvJNpxIfKlooAzZYZE4ANM5fpX`
            }
        });
        return response.data;
    } catch (error) {
        console.error("Error al obtener museos:", error);
        throw error;
    }
};

export default api;
