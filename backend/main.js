const { spawn } = await import('child_process');

const startPythonProcess = (fileName) => {
    return new Promise((resolve, reject) => {
        const pythonProcess = spawn('python', [fileName])
        let pythonData = '';
        let pythonErrors = '';

        pythonProcess.stdout.on('data', (data) => {
            pythonData += data.toString();
        })

        pythonProcess.stderr.on('data', (data) => {
            pythonErrors+=data.toString();
        })
        pythonProcess.on('close', (code) => {
            console.log(`Python process ended on code: ${code}`);
            console.log("python data", pythonData);
            pythonData = JSON.parse(pythonData);
            if (pythonData.Status == 200) {
                resolve(pythonData);
            } else {
                reject(new Error(`Python script exited with code ${pythonData.Status}, ${pythonErrors}`));
            }
        })

        pythonProcess.on('error', (error) => {
            reject(new Error(error));
        })
    })
}

export const getRecentNews = async () => {
    try {
        const newsData = await startPythonProcess("../python-endpoints/getRecentNews.py");
        return newsData
    } catch (e) {
        console.error("Error bleh getRecentNews " + e);
        throw e;
    }

}

export const getMostOpinionated = async() => {
    try {
        const newsData = await startPythonProcess("../python-endpoints/getMostOpinionated.py");
        return newsData
    } catch (e) {
        console.error("Error bleh getmostOpinionated " + e);
        throw e;
    }
}

export const getLeastOpinionated = async() => {
    try {
        const newsData = await startPythonProcess("../python-endpoints/getLeastOpinionated.py");
        return newsData
    } catch (e) {
        console.error("Error bleh getLeastOpinionated " + e);
        throw e;
    }
}
