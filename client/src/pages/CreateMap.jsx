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

  const titleCase = (str) => {
    return str.charAt(0).toUpperCase() + str.substr(1).toLowerCase();
  };

  const handleChange = (e) => {
    setNewMap(prev => (
      { ...prev, [e.target.name]: titleCase(e.target.value.replace(/\s/g, '')) }
    ))
  };

  const handleTitleChange = (e) => {
    setNewMap(prev => (
      { ...prev, [e.target.name]: e.target.value.trim() }
    ))
  };

  const handleBusinessTypeChange = (e) => {
    const types = e.target.value.replace(/\s/g, '').split(",")
    const titleCaseTypes = types.map(
      (item) => {
        return titleCase(item)
      }
    )
    setNewMap(prev => (
      { ...prev, businessTypes: titleCaseTypes }
    ))
  };

  const handleClick = async e => {
    e.preventDefault()
    try {
      setLoading(true)
      await axios.post("http://localhost:8800/maps", newMap)
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
  }

  //  TODO: make the business type input a checkbox list
  return (
    <div>
      <div className='grid grid-cols-2 gap-10'>
        <ViewMaps />
        <div className='grid grid-cols-1 gap-1'>
          <h1 className="card-title justify-center">Create New Map</h1>
          <input type="text" placeholder="Enter City" className="input input-bordered w-full max-w-xs" onChange={handleChange} name="city" />
          <input type="text" placeholder="Enter State" className="input input-bordered w-full max-w-xs" onChange={handleChange} name="state" />
          <input type="text" placeholder="Enter Map Title" className="input input-bordered w-full max-w-xs" onChange={handleTitleChange} name="title" />
          <input type="text" placeholder="Enter Business Types" className="input input-bordered w-full max-w-xs" onChange={handleBusinessTypeChange} name="businessTypes" />
          <AddButton />
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
                <h2 className="card-title">{map.title}</h2>
                <div className="card-actions">
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
