function fetchRecentNews() {
    // fetch('https://localhost:3000/api/getRecentNews')
    //     .then(response=>{
    //         if (!response.ok) {
    //             throw new Error("It doesn't fucking exist rn");
    //         }

    //         return response.json();
    //     })
    //     .then(data=>{
    //         return data.news;
    //     })
    //     .catch(error=>{
    //         console.error(error);
    //     })

    return [{"title": "Humungous", "desc":"This is the largest waste of my time"}, {"title":"Small", "desc":"This will not help me get a job"}];
}


const displayRecentNews = () => {
    const recentNews = fetchRecentNews();
    const recentNewsContainer = document.getElementById("newNewsArticles");
    recentNews.forEach((news) => {
        const container = document.createElement("div");
        const title = document.createElement("h4");
        const desc = document.createElement("p");
        
        recentNewsContainer.appendChild(container);
        container.appendChild(title);
        container.appendChild(desc);


        title.innerHTML = news.title;
        desc.innerHTML = news.desc;
        recentNewsContainer.appendChild(container);
    })
}

const fetchLeastOpinionated = () => {
    // fetch("https://localhost:3000/api/getLeastOpinionated")
    //     .then(response => {
    //         if (!response.ok) {
    //             throw new Error("Bruh least opinionated endpoint doesn't work");
    //         }
    //         return response.json();
    //     })
    //     .then(data=> {
    //         return data.sources;
    //     })
    //     .catch(error=> {
    //         console.error(error);
    //     })
    return [{"title": "Humungous", "desc":"This is the largest waste of my time", "score":4.5}, {"title":"Small", "desc":"This will not help me get a job","score":5.5}];

}

const fetchMostOpinionated = () => {
    // fetch("https://localhost:3000/api/getMostOpinionated")
    //     .then(response => {
    //         if (!response.ok) {
    //             throw new Error("Bruh most opinionated endpoint doesn't work");
    //         }
    //         return response.json();
    //     })
    //     .then(data=> {
    //         return data.sources;
    //     })
    //     .catch(error=> {
    //         console.error(error);
    //     })

    return [{"title": "Humungous", "desc":"This is the largest waste of my time", "score":1.5}, {"title":"Small", "desc":"This will not help me get a job","score":2.5}];
}

const displayOpinionatedSources = (opinionated) => {
    let opNews;
    let newsSourceContainer;
    if (!opinionated) {
        opNews = fetchLeastOpinionated();
        newsSourceContainer = document.getElementById("topNewsCorperations");
    } else {
        opNews = fetchMostOpinionated();
        newsSourceContainer = document.getElementById("bottomNewsCorperations");
    }
    opNews.forEach((newsSource) => {
        const container = document.createElement("div");
        const title = document.createElement("h4");
        const desc = document.createElement("p");
        const opScore = document.createElement("p");
        
        newsSourceContainer.appendChild(container);
        container.appendChild(title);
        container.appendChild(desc);
        container.appendChild(opScore);


        title.innerHTML = newsSource.title;
        desc.innerHTML = newsSource.desc;
        opScore.innerHTML = "Opinionated Metric: " + newsSource.score
        newsSourceContainer.appendChild(container);
    })
}
document.addEventListener("DOMContentLoaded", () => {
    displayRecentNews();
    //True meaning the opinionated ones and False meaniing the non-opinionated ones
    displayOpinionatedSources(true);
    displayOpinionatedSources(false);
});

