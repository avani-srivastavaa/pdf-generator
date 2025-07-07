
import React, { useState } from 'react';
import axios from 'axios';
import './FormStyles.css';

function GenerateForm() {
  const [formData, setFormData] = useState({
  name: "",
  position: "",
  role: "",
  from_date: "",
  to_date: "",
  duration: "",  
  type: "certificate"
});


  const handleChange = e => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const token = localStorage.getItem("token");

  const handleGenerate = async (e) => {
    e.preventDefault();
    const response = await axios.post(
  `${process.env.REACT_APP_API_URL}/generate`,
  formData,
  {
    responseType: 'blob',
    headers: {
      Authorization: `Bearer ${token}`
    },
    withCredentials: true // <- ADD THIS
  }
);


    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `${formData.type}_${formData.name}.pdf`);
    document.body.appendChild(link);
    link.click();
  };

  return (
    <div className="form-container">
    <div className="company-name">
      {/* <span className="purple">PURPLERAIN</span> <span className="white">TECHSAFE</span> */}
    </div>
      <select name="type" onChange={handleChange}>
        <option value="certificate">Certificate</option>
        <option value="recommendation_letter">Recommendation</option>
        <option value="joining_letter">Joining</option>
        <option value="appreciation_letter">Appreciation</option>
      </select>
      <input
  name="from_date"
  placeholder="From Date (YYYY-MM-DD)"
  type="date"
  onChange={handleChange}
/>
<input
  name="to_date"
  placeholder="To Date (YYYY-MM-DD)"
  type="date"
  onChange={handleChange}
/>
      <input name="name" placeholder="Name" onChange={handleChange} />
      <input name="position" placeholder="Position" onChange={handleChange} />
      <input name="role" placeholder="Role" onChange={handleChange} />
      <input name="duration" placeholder="Duration (eg. 3 Months)" onChange={handleChange} />
      <input name="date" placeholder="Date" onChange={handleChange} />
      <button onClick={handleGenerate}>Generate</button>
    </div>
  );
}

export default GenerateForm;
