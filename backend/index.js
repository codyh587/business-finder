import cors from 'cors'
import express from 'express'
import path, { dirname } from 'path'
import { PythonShell } from 'python-shell'
import { fileURLToPath } from 'url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const mapIndexPath = path.join(__dirname, 'generate_maps', 'maps', 'map_index.json')
const createMapPath = path.join(__dirname, 'generate_maps', 'generateMapData.py')
const indexHandlerPath = path.join(__dirname, 'generate_maps', 'mapIndexHandler.py')

const app = express()
app.use(express.json())
app.use(cors())

// get map index
app.get("/maps", (req, res) => {
    res.header("Content-Type", 'application/json')
    res.sendFile(mapIndexPath)
})

// get specific map file
app.get("/maps/:id", (req, res) => {
    const mapId = req.params.id
    res.header("Content-Type", 'application/json')
    res.sendFile(path.join(__dirname, 'generate_maps', 'maps', mapId + '.json'))
})

// create map with generateMapData.py
// TODO: verify input values are correct (Python probably works)
app.post("/maps", (req, res) => {
    const values = {
        "city": req.body.city,
        "state": req.body.state,
        "title": req.body.title,
        "businessTypes": req.body.businessTypes
    }

    var pyshell = new PythonShell(createMapPath, { pythonOptions: ["-u"] });
    for (const value of Object.values(values)) pyshell.send(value)

    pyshell.on("message", function (message) { console.log(message) })
    pyshell.end(function (err) { if (err) throw err })

    return res.json("Map generated successfully")
})

// update map with mapIndexHandler.py
app.put("/maps/:id", (req, res) => {
    const mapId = req.params.id
    const newTitle = req.body.newTitle

    var pyshell = new PythonShell(indexHandlerPath, { pythonOptions: ["-u"] })
    pyshell.send("UPDATE")
    pyshell.send(mapIndexPath)
    pyshell.send(mapId)
    pyshell.send(newTitle)

    pyshell.on("message", function (message) { console.log(message) })
    pyshell.end(function (err) { if (err) throw err })

    return res.json("Map updated successfully")
})

// delete map with mapIndexHandler.py
app.delete("/maps/:id", (req, res) => {
    const mapId = req.params.id

    var pyshell = new PythonShell(indexHandlerPath, { pythonOptions: ["-u"] })
    pyshell.send("DELETE")
    pyshell.send(mapIndexPath)
    pyshell.send(mapId)

    pyshell.on("message", function (message) { console.log(message) })
    pyshell.end(function (err) { if (err) throw err })

    return res.json("Map deleted successfully")
})

app.listen(8800, () => {
    console.log("Connected to server")
})
