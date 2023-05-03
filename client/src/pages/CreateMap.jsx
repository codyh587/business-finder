import axios from 'axios'
import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

// Create map form
const CreateMap = () => {
  const [newMap, setNewMap] = useState({
    city: "",
    state: "",
    title: "",
    businessTypes: [],
  });

  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setNewMap(prev => (
      { ...prev, [e.target.name]: e.target.value.trim().replace(/\s+/g, '+') }
    ))
  };

  const handleTitleChange = (e) => {
    setNewMap(prev => (
      { ...prev, [e.target.name]: e.target.value.trim() }
    ))
  };

  const handleBusinessTypeChange = (e) => {
    const types = e.target.value.replace(/\s/g, '').split(",")
    setNewMap(prev => (
      { ...prev, businessTypes: types }
    ))
  };

  const handleClick = async e => {
    e.preventDefault()
    try {
      setLoading(true)
      await axios.post("/api/maps", newMap)
      setLoading(false)
      window.location.reload()
      console.log(newMap)
    } catch (err) {
      console.log(err)
    }
  };

  function AddButton() {
    if (loading) {
      return <button className="btn btn-l loading btn-disabled">Add</button>
    } else {
      return <button className="btn btn-l" onClick={handleClick}>Add</button>
    }
  };

  return (
    <div>
      <div className='inline-flex flex-row h-fit gap-14 items-start'>
        <ViewMaps />
        <div className='grid grid-cols-1 gap-2'>
          <h1 className="card-title justify-center">Create New Map</h1>
          <input type="text" placeholder="Enter City" className="input input-bordered w-full max-w-xs" onChange={handleChange} name="city" />
          <input type="text" placeholder="Enter State" className="input input-bordered w-full max-w-xs" onChange={handleChange} name="state" />
          <input type="text" placeholder="Enter Map Title" className="input input-bordered w-full max-w-xs" onChange={handleTitleChange} name="title" />
          <div className="tooltip" data-tip="Enter a comma-separated list of valid business types. View valid inputs below.">
            <input type="text" placeholder="Enter Business Types" className="input input-bordered w-full max-w-xs" onChange={handleBusinessTypeChange} name="businessTypes" />
          </div>
          <AddButton />
          <button className="btn btn-sm"><Link to={`/validTypes`}>Valid Business Types</Link></button>
        </div>
      </div>
    </div>
  );
};

// Separate React component: create current maps listing, contains update, delete, and view buttons
const ViewMaps = () => {
  const [maps, setMaps] = useState([]);

  useEffect(() => {
    const fetchAllMaps = async () => {
      try {
        const res = await axios.get("/api/maps")
        setMaps(res.data)
      } catch (err) {
        console.log(err)
      }
    }
    fetchAllMaps()
  }, []);

  const handleDelete = async (id) => {
    try {
      await axios.delete("/api/maps/" + id)
      window.location.reload()
    } catch (err) {
      console.log(err)
    }
  };

  return (
    <div className="grid grid-cols-1 gap-2">
      <h1 className="card-title justify-center">My Maps</h1>
      {
        maps.map(
          (map) => (
            <div className="card card-compact card-bordered bg-base-100 shadow-xl">
              <div className="card-body">
                <h2 className="card-title justify-center">{map.title}</h2>
                <div className="card-actions justify-center">
                  <button className="btn btn-xs btn-primary"><Link to={`/viewMap/${map.id}`}>View</Link></button>
                  <button className="btn btn-xs btn-secondary"><Link to={`/updateMap/${map.id}`}>Update</Link></button>
                  <button className="btn btn-xs btn-accent text-white" onClick={() => handleDelete(map.id)}>Delete</button>
                </div>
              </div>
            </div>
          )
        )
      }
    </div>
  );
};

export default CreateMap
