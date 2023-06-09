import express from 'express'
import helmet from 'helmet'
import path, { dirname } from 'path'
import { PythonShell } from 'python-shell'
import { fileURLToPath } from 'url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const createMapPath = path.join(__dirname, 'generate_maps', 'generateMapData.py')
const indexHandlerPath = path.join(__dirname, 'generate_maps', 'mapIndexHandler.py')

const app = express()
app.use(express.json())
app.use(helmet())

const baseURL = "/api"

// get map index
app.get(baseURL + "/maps", (req, res) => {
    var pyshell = new PythonShell(indexHandlerPath, { pythonOptions: ["-u"] });
    pyshell.send("GET")

    try {
        pyshell.on("message", function (message) { return res.json(JSON.parse(message)) })
        pyshell.end(function (err) { if (err) console.log(err) })
    }
    catch (err) {
        return res.json("Map index get failed")
    }
})

// get specific map file
app.get(baseURL + "/maps/:id", (req, res) => {
    const mapId = req.params.id
    res.header("Content-Type", 'application/json')
    res.sendFile(path.join(__dirname, 'generate_maps', 'maps', mapId + '.json'))
})

// create map with generateMapData.py
app.post(baseURL + "/maps", (req, res) => {
    const values = {
        "city": req.body.city,
        "state": req.body.state,
        "title": req.body.title,
        "businessTypes": req.body.businessTypes
    }

    var pyshell = new PythonShell(createMapPath, { pythonOptions: ["-u"] });
    for (const value of Object.values(values)) pyshell.send(value)

    try {
        pyshell.on("message", function (message) { console.log(message) })
        pyshell.end(function (err) { if (err) console.log(err) })
        pyshell.on("close", () => { return res.json("Map generated successfully") })
    }
    catch (err) {
        return res.json("Map generation failed")
    }
})

// update map with mapIndexHandler.py
app.put(baseURL + "/maps/:id", (req, res) => {
    const mapId = req.params.id
    const newTitle = req.body.newTitle

    var pyshell = new PythonShell(indexHandlerPath, { pythonOptions: ["-u"] })
    pyshell.send("UPDATE")
    pyshell.send(mapId)
    pyshell.send(newTitle)

    try {
        pyshell.on("message", function (message) { console.log(message) })
        pyshell.end(function (err) { if (err) console.log(err) })
        pyshell.on("close", () => { return res.json("Map updated successfully") })
    }
    catch (err) {
        return res.json("Map update failed")
    }
})

// delete map with mapIndexHandler.py
app.delete(baseURL + "/maps/:id", (req, res) => {
    const mapId = req.params.id

    var pyshell = new PythonShell(indexHandlerPath, { pythonOptions: ["-u"] })
    pyshell.send("DELETE")
    pyshell.send(mapId)

    try {
        pyshell.on("message", function (message) { console.log(message) })
        pyshell.end(function (err) { if (err) console.log(err) })
        pyshell.on("close", () => { return res.json("Map deleted successfully") })
    }
    catch (err) {
        return res.json("Map delete failed")
    }
})

const PORT = process.env.PORT || 8800;
app.listen(PORT, (_) => {
    console.log(`Server started on port ${PORT}`);
    console.log(app.get('env'));
});
