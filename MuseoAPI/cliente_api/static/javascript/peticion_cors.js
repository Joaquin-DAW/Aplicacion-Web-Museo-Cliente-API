fetch("http://127.0.0.1:8000/api/v1/museos", {
    method: "GET",
    headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer orMCMMA3mh0Ltb1Zj9N2ROv9TKhKdq` 
    }
})
.then(response => {
    if (!response.ok) {
        throw new Error(`Error en la petición: ${response.statusText}`);
    }
    return response.json();
})
.then(data => {
    console.log("📌 Respuesta recibida:", data);
})
.catch(error => {
    console.error("🚨 Error en la petición:", error);
});

