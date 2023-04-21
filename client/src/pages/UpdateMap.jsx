import axios from 'axios'
import React, { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'

// Update map title
const UpdateMap = () => {
  const [newTitle, setNewTitle] = useState({
    newTitle: "",
  });

  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const mapId = location.pathname.split("/")[2];

  const handleChange = (e) => {
    setNewTitle(prev => ({ ...prev, [e.target.name]: e.target.value }))
  };

  const handleClick = async e => {
    e.preventDefault()
    try {
      setLoading(true)
      await axios.put("http://localhost:8800/maps/" + mapId, newTitle)
      setLoading(false)
      navigate("/")
    } catch (err) {
      console.log(err)
    }
  };

  console.log(newTitle);

  function UpdateButton() {
    if (loading) {
      return <button className="btn btn-l btn-secondary loading btn-disabled">Update</button>
    } else {
      return <button className="btn btn-l btn-secondary" onClick={handleClick}>Update</button>
    }
  };

  return (
    <div className='grid grid-cols-1 gap-2'>
      <h1 className="card-title justify-center">Update Map Title</h1>
      <input type="text" placeholder="New Title" className="input input-bordered w-full max-w-xs" onChange={handleChange} name="newTitle" />
      <UpdateButton />
      <button className="btn btn-sm"><Link to={`/`}>Back</Link></button>
    </div>
  );
};

export default UpdateMap
