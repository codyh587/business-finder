import axios from 'axios'
import L, { latLngBounds, marker } from 'leaflet';
import React, { useEffect, useState } from 'react'
import { MapContainer, TileLayer, Popup, CircleMarker } from 'react-leaflet'
import { Link, useLocation } from 'react-router-dom'
import 'leaflet/dist/leaflet.css'
import "leaflet-easybutton/src/easy-button.js";
import "leaflet-easybutton/src/easy-button.css";
import "font-awesome/css/font-awesome.min.css";

// View leaflet map
const ViewMap = () => {
  const location = useLocation();
  const mapId = location.pathname.split("/")[2];
  const [mapData, setMapData] = useState([]);
  const [mapLocation, setMapLocation] = useState({ lat: null, lng: null });
  const [mapBounds, setMapBounds] = useState([[null, null], [null, null]]);
  const [mapTitle, setMapTitle] = useState("");
  const [map, setMap] = useState(null);
  const markerBounds = latLngBounds([]);

  useEffect(() => {
    const fetchMap = async (id) => {
      try {
        const res = await axios.get("http://localhost:8800/maps/" + id)
        setMapData(res.data)
      } catch (err) {
        console.log(err)
      }
    }

    const fetchMapLocationAndTitle = async (id) => {
      try {
        const res = await axios.get("http://localhost:8800/maps")
        res.data.forEach(element => {
          if (element.id == id) {
            setMapLocation({
              'lat': element.location[0],
              'lng': element.location[1]
            })
            setMapBounds([
              [element.bounds[0], element.bounds[1]],
              [element.bounds[2], element.bounds[3]]
            ])
            setMapTitle(element.title)
          }
        })
      } catch (err) {
        console.log(err)
      }
    }

    fetchMap(mapId)
    fetchMapLocationAndTitle(mapId)
  }, []);

  // Zoom in/out button
  useEffect(() => {
    if (!map) return;
    var button = L.easyButton({
      states: [
        {
          stateName: 'zoom-markers',
          icon: 'fa-map-marker',
          title: 'Zoom out to all markers',
          onClick: function (btn, map) {
            map.fitBounds(markerBounds)

            btn.state('zoom-state');
          }
        },
        {
          stateName: 'zoom-state',
          icon: 'fa-building',
          title: 'Zoom in to city border',
          onClick: function (btn, map) {
            map.fitBounds(mapBounds)
            btn.state('zoom-markers');
          }
        }
      ]
    })

    button.addTo(map);
  }, [map]);

  console.log(mapLocation);
  console.log(mapBounds);
  console.log(markerBounds);

  if (
    mapLocation['lat'] && mapLocation['lng'] &&
    mapBounds[0][0] && mapBounds[0][1] && mapBounds[1][0] && mapBounds[1][1]
  ) {

    mapData.forEach(element => {
      markerBounds.extend(element.c)
    });

    return (
      <div className="flex-col space-y-3">
        <h2 className="card-title justify-center">View Map: {mapTitle}</h2>
        <MapContainer
          center={mapLocation}
          bounds={mapBounds}
          boundsOptions={{ padding: [20, 20] }}
          ref={setMap}
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
          />
          {
            mapData.map(
              (item) => (
                <CircleMarker
                  center={item.c}
                  radius={3.5}
                  color={"#FF5F1F"}
                  fillOpacity={1}
                  eventHandlers={{
                    mouseover: (event) => event.target.openPopup(),
                  }}
                >
                  <Popup>
                    <b>{item.n}</b> <br />
                    {item.a} <br />
                    <hr></hr>
                    <i>Type: {item.t}</i>
                  </Popup>
                </CircleMarker>
              )
            )
          }
        </MapContainer>
        <button className="btn btn-sm w-min"><Link to={`/`}>Back</Link></button>
      </div>
    );
  };
};

export default ViewMap
