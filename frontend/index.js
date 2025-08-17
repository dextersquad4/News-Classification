async function fetchRecentNews() {
    try{
        const response = await fetch("https://localhost:3000/api/getRecentNews");

        if (!response.ok){
            throw new Error("It doesn't work");
        }
        const data = await response.json();
        return data.news;
    } catch (error){
        console.error(error);
        return null;
    }
}


const displayRecentNews = () => {
    fetchRecentNews().then(response => {
        if (!response) {
            throw new Error("Bruh recent news endpoint is returning nothing");
        }
        const recentNewsContainer = document.getElementById("newNewsArticles");
        response.forEach((news) => {
            const container = document.createElement("div");
            container.addEventListener('click', () => {
                window.location.href = news.url;
            });
            const title = document.createElement("h4");
            const desc = document.createElement("p");
            
            recentNewsContainer.appendChild(container);
            container.appendChild(title);
            container.appendChild(desc);


            title.innerHTML = news.title;
            desc.innerHTML = news.description;
            recentNewsContainer.appendChild(container);
        })
    })
    .catch(error=> {
        console.error(error);
    })
}

const fetchLeastOpinionated = async() => {
    try{
        const response = await fetch("https://localhost:3000/api/getLeastOpinionated");

        if (!response.ok){
            throw new Error("It doesn't work");
        }

        const data = await response.json();
        return data.sources;
    } catch (error){
        console.error(error);
        return null;
    }
}
const fetchMostOpinionated = async() => {
    try{
        const response = await fetch("https://localhost:3000/api/getMostOpinionated");

        if (!response.ok){
            throw new Error("It doesn't work");
        }
        const data = await response.json();
        return data.sources;
    } catch (error){
        console.error(error);
        return null;
    }
}

const displayOpinionatedSources = (opinionated) => {
    if (!opinionated) {
        fetchLeastOpinionated().then(result=> {
            const newsSourceContainer = document.getElementById("topNewsCorperations");
            createOpinionatedDisplay(result, newsSourceContainer);
        });
    } else {
        fetchMostOpinionated().then(result=> {
            const newsSourceContainer = document.getElementById("bottomNewsCorperations");
            createOpinionatedDisplay(result, newsSourceContainer);
        });
    }
}

const createOpinionatedDisplay = (newsSources, newsSourceContainer) => {
    newsSources.forEach((newsSource) => {
        const container = document.createElement("div");
        container.addEventListener('click', ()=> {
            window.location.href = "https://" + newsSource.title;
        });
        const title = document.createElement("h4");
        const opScore = document.createElement("p");
        
        newsSourceContainer.appendChild(container);
        container.appendChild(title);
        container.appendChild(opScore);


        title.innerHTML = newsSource.title;
        opScore.innerHTML = "Opinionated Metric: " + newsSource.rating
        newsSourceContainer.appendChild(container);
    })
}
document.addEventListener("DOMContentLoaded", () => {
    displayRecentNews();
    //True meaning the opinionated ones and False meaniing the non-opinionated ones
    displayOpinionatedSources(true);
    displayOpinionatedSources(false);
});

