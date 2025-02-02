import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [categories, setCategories] = useState([]);
  const [error, setError] = useState(null);

  const fetchCategories = async () => {
    const url = 'http://127.0.0.1:8000/server_api/product/categories/fetch_all/';

    try {
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'cb254249d8c2209c975006928bb646faddd2a585', // Replace with your actual token
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch categories');
      }

      const data = await response.json();
      setCategories(data.product_category); // Ensure this matches the API structure
    } catch (err) {
      setError(err.message);
    }
  };

  useEffect(() => {
    fetchCategories(); // Fetch all categories on component mount
  }, []);

  return (
    <div className="App">
      <h1>Product Categories</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <ul>
        {categories.map((category) => (
          <li key={category.id}>
            <h3>{category.category_name}</h3>
            <p>{category.description}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
