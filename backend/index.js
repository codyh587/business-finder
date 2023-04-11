import express from 'express'
import cors from 'cors'

const app = express()
app.use(express.json())
app.use(cors())

app.get("/maps", (req, res) => {
    res.json("maps get successful")
})

app.post("/maps", (req, res) => {
    const values = {
        "id": 0,
        "city": req.body.city,
        "businessTypes": req.body.businessTypes
    }

    return res.json("maps create successful")
})

app.put("/maps/:id", (req, res) => {
    return res.json("maps update successful")
})

app.delete("/maps/:id", (req, res) => {
    return res.json("maps delete successful")
})

app.listen(8800, () => {
    console.log("Connected to server")
})
