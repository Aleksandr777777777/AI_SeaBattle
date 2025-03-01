import axios from "axios"

const API_URL = "http://localhost:8000";
export const getGameState = async () => {
    const responce = await axios.get(`${API_URL}/`);
    return responce.data
}