import axios from 'axios'
import React, { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

// Create map
const CreateMap = () => {
  const navigate = useNavigate()

  const [newMap, setNewMap] = useState({
    city: "",
    state: "",
    title: "",
    businessTypes: [],
  });

  const handleChange = (e) => {
    setNewMap(prev => (
      { ...prev, [e.target.name]: e.target.value }
    ))
  };

  const handleBusinessTypeChange = (e) => {
    const types = e.target.value.split(",")
    setNewMap(prev => (
      { ...prev, businessTypes: types }
    ))
  };

  const handleClick = async e => {
    e.preventDefault()
    try {
      await axios.post("http://localhost:8800/maps", newMap)
      navigate("/")
      console.log(newMap)
    } catch (err) {
      console.log(err)
    }
  };

  //  TODO: make the business type input a checkbox list
  return (
    <div>
      <ViewMaps />
      <div className='form'>
        <h1>Create New Map</h1>
        <input type="text" placeholder='City' onChange={handleChange} name="city" />
        <input type="text" placeholder='State' onChange={handleChange} name="state" />
        <input type="text" placeholder='Title' onChange={handleChange} name="title" />
        <input type="text" placeholder='Business Types' onChange={handleBusinessTypeChange} name="businessTypes" />
        <button onClick={handleClick}>Add</button>
      </div>
    </div>
  );
};

// Current map listing, contains update, delete, and view buttons
const ViewMaps = () => {
  const [maps, setMaps] = useState([]);

  useEffect(() => {
    const fetchAllMaps = async () => {
      try {
        const res = await axios.get("http://localhost:8800/maps")
        setMaps(res.data)
      } catch (err) {
        console.log(err)
      }
    }
    fetchAllMaps()
  }, []);

  const handleDelete = async (id) => {
    try {
      await axios.delete("http://localhost:8800/maps/" + id)
      // delay reload until python can be run synchronously
      await new Promise(resolve => setTimeout(resolve, 100));
      window.location.reload()
    } catch (err) {
      console.log(err)
    }
  };

  return (
    <div>
      <h1>My Maps</h1>
      <div className="maps">
        {
          maps.map(
            (map) => (
              <div className="map" key={map.id}>
                <h2>{map.title}</h2>
                <button className="view"><Link to={`/viewMap/${map.id}`}>View</Link></button>
                <button className="update"><Link to={`/updateMap/${map.id}`}>Update</Link></button>
                <button className="delete" onClick={() => handleDelete(map.id)}>Delete</button>
              </div>
            )
          )
        }
      </div>
    </div>
  );
};

export default CreateMap
