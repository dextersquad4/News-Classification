export const getRecentNews = async () => {
    return {'Status': 200, "Message": "Reached get recent news endpoint", "news": [{"title": "Humungous", "desc":"This is the largest waste of my time"}, {"title":"Small", "desc":"This will not help me get a job"}]};
}

export const getMostOpinionated = async() => {
    return {'Status': 200, "Message": "Reached get most opinionated", "sources": [{"title": "Humungous", "desc":"This is the largest waste of my time", "score":1.5}, {"title":"Small", "desc":"This will not help me get a job","score":2.5}]};
}

export const getLeastOpinionated = async() => {
    return {'Status': 200, "Message": "Reached get least opinionated", "sources": [{"title": "Humungous", "desc":"This is the largest waste of my time", "score":4.5}, {"title":"Small", "desc":"This will not help me get a job","score":5.5}]};
}
