import axios from 'axios'
import React, { useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'

// Update map title
const UpdateMap = () => {
  const [newTitle, setNewTitle] = useState({
    newTitle: "",
  });

  const navigate = useNavigate();
  const location = useLocation();
  const mapId = location.pathname.split("/")[2];

  const handleChange = (e) => {
    setNewTitle(prev => ({ ...prev, [e.target.name]: e.target.value }))
  };

  const handleClick = async e => {
    e.preventDefault()
    try {
      await axios.put("http://localhost:8800/maps/" + mapId, newTitle)
      navigate("/")
    } catch (err) {
      console.log(err)
    }
  };

  console.log(newTitle);

  return (
    <div>
      <div className='form'>
        <h1>Update Map Title</h1>
        <input type="text" placeholder='New Title' onChange={handleChange} name="newTitle" />
        <button onClick={handleClick}>Update</button>
      </div>
    </div>
  );
};

export default UpdateMap
