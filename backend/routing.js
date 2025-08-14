import { getRecentNews, getLeastOpinionated, getMostOpinionated } from "./main.js";

export const callEndpoints = async (endpoint) => {
    if (endpoint === "getRecentNews") {
        return await getRecentNews();
    } else if (endpoint === "getLeastOpinionated") {
        return await getLeastOpinionated();
    } else if (endpoint === "getMostOpinionated") {
        return await getMostOpinionated();
    } else {
        return {"Status": 404, "Message": "Endpoint doesn't exist"};
    }
} 