import axios from 'axios'
import React, { useEffect, useState } from 'react'
import { Link, useLocation } from 'react-router-dom'

const ViewMap = () => {
  const location = useLocation();
  const mapId = location.pathname.split("/")[2];

  const [mapData, setMapData] = useState([]);

  useEffect(() => {
    const fetchMap = async (id) => {
      try {
        const res = await axios.get("http://localhost:8800/maps/" + id)
        setMapData(res.data)
      } catch (err) {
        console.log(err)
      }
    }

    fetchMap(mapId)
  }, []);

  console.log(mapData);

  //  TODO make an actual map with the leaflet api
  return (
    <div>
      <h1>View Map</h1>
      <div className="mapData">
        {
          mapData.map(
            (item) => (
              <div className="item" key = {item.a}>
                <p>{item.n}</p>
                <p>{item.c}</p>
                <p>{item.a}</p>
                <p>{item.t}</p>
              </div>
            )
          )
        }
      </div>
      <button className="back"><Link to={`/`}>Back</Link></button>
    </div>
  );
}

export default ViewMap
