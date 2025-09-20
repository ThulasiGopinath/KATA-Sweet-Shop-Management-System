import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [sweets, setSweets] = useState([]);
  const [name, setName] = useState('');
  const [price, setPrice] = useState('');
  const [category, setCategory] = useState('');
  const [quantity, setQuantity] = useState('');
  const [updateId, setUpdateId] = useState(null);
  const [updateName, setUpdateName] = useState('');
  const [updatePrice, setUpdatePrice] = useState('');
  const [updateCategory, setUpdateCategory] = useState('');
  const [updateQuantity, setUpdateQuantity] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [token, setToken] = useState('');
  const [isAdmin, setIsAdmin] = useState(false);
  const [isRegistering, setIsRegistering] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [searchCategory, setSearchCategory] = useState('');
  const [minPrice, setMinPrice] = useState('');
  const [maxPrice, setMaxPrice] = useState('');

  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    if (storedToken) {
      setToken(storedToken);
      setIsLoggedIn(true);

      try {
        const tokenParts = storedToken.split('.');
        const payload = JSON.parse(atob(tokenParts[1]));
        setIsAdmin(payload.is_admin);
      } catch (error) {
        console.error("Failed to decode token:", error);
        localStorage.removeItem('token');
        setToken('');
        setIsLoggedIn(false);
        setIsAdmin(false);
      }

      fetchSweets();
    }
  }, []);

  const fetchSweets = () => {
    fetch('http://localhost:8000/sweets')
      .then(response => response.json())
      .then(data => setSweets(data))
      .catch(error => console.error('Error fetching sweets:', error));
  };

  const handleSearch = () => {
    const queryParams = new URLSearchParams();
    if (searchTerm) queryParams.append('name', searchTerm);
    if (searchCategory) queryParams.append('category', searchCategory);
    if (minPrice) queryParams.append('min_price', minPrice);
    if (maxPrice) queryParams.append('max_price', maxPrice);

    fetch(`http://localhost:8000/sweets/search?${queryParams.toString()}`)
      .then(response => response.json())
      .then(data => setSweets(data))
      .catch(error => console.error('Error fetching sweets:', error));
  };

  const handleAddSweet = (e) => {
    e.preventDefault();
    fetch('http://localhost:8000/add-sweet', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({ name, price: parseFloat(price), category, quantity: parseInt(quantity) }),
    })
      .then(response => response.json())
      .then(() => {
        setName('');
        setPrice('');
        setCategory('');
        setQuantity('');
        fetchSweets();
      })
      .catch(error => console.error('Error adding sweet:', error));
  };

  const handleDeleteSweet = (id) => {
    fetch(`http://localhost:8000/delete-sweet/${id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })
      .then(() => {
        fetchSweets();
      })
      .catch(error => console.error('Error deleting sweet:', error));
  };

  const handleUpdateSweet = (e) => {
    e.preventDefault();
    fetch(`http://localhost:8000/update-sweet/${updateId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({ name: updateName, price: parseFloat(updatePrice), category: updateCategory, quantity: parseInt(updateQuantity) }),
    })
      .then(response => response.json())
      .then(() => {
        setUpdateId(null);
        setUpdateName('');
        setUpdatePrice('');
        setUpdateCategory('');
        setUpdateQuantity('');
        fetchSweets();
      })
      .catch(error => console.error('Error updating sweet:', error));
  };

  const handlePurchase = (id, quantity) => {
    fetch(`http://localhost:8000/sweets/purchase/${id}?quantity=${quantity}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })
      .then(response => response.json())
      .then(data => {
        if (data.detail) {
          alert(data.detail);
        }
        fetchSweets();
      })
      .catch(error => console.error('Error during purchase:', error));
  };

  const handleRestock = (id, quantity) => {
    fetch(`http://localhost:8000/sweets/restock/${id}?quantity=${quantity}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })
      .then(response => response.json())
      .then(() => fetchSweets())
      .catch(error => console.error('Error during restock:', error));
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    const isAdmin = username.toLowerCase() === 'admin';
    try {
      const response = await fetch('http://localhost:8000/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password, is_admin: isAdmin }),
      });
      if (response.ok) {
        alert('Registration successful! Please log in.');
        setIsRegistering(false);
      } else {
        const errorData = await response.json();
        alert(errorData.detail);
      }
    } catch (error) {
      console.error('Registration error:', error);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const formData = new URLSearchParams();
      formData.append('username', username);
      formData.append('password', password);

      const response = await fetch('http://localhost:8000/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('token', data.access_token);
        setToken(data.access_token);
        setIsLoggedIn(true);

        const tokenParts = data.access_token.split('.');
        const payload = JSON.parse(atob(tokenParts[1]));
        setIsAdmin(payload.is_admin);

        fetchSweets();
      } else {
        const errorData = await response.json();
        alert(errorData.detail);
      }
    } catch (error) {
      console.error('Login error:', error);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsLoggedIn(false);
    setToken('');
    setIsAdmin(false);
  };

  return (
    <div className="App">
      <h1>Sweet Shop</h1>

      {!isLoggedIn ? (
        <div className="auth-container">
          {isRegistering ? (
            <form onSubmit={handleRegister} className="form-container">
              <h2>Register</h2>
              <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              <div className="admin-checkbox">
                <label>
                  <input
                    type="checkbox"
                    checked={isRegistering && username.toLowerCase() === 'admin'}
                    onChange={() => { }}
                    readOnly
                  />
                  Register as Admin
                </label>
              </div>

              <button type="submit">Register</button>
              <p onClick={() => setIsRegistering(false)}>Already have an account? Log in</p>
            </form>
          ) : (
            <form onSubmit={handleLogin} className="form-container">
              <h2>Login</h2>
              <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
              <button type="submit">Login</button>
              <p onClick={() => setIsRegistering(true)}>Don't have an account? Register</p>
            </form>
          )}
        </div>
      ) : (
        <>
          <button onClick={handleLogout} className="logout-button">Logout</button>

          {/* Add Sweet Form */}
          <form onSubmit={handleAddSweet} className="form-container">
            <h3>Add a New Sweet</h3>
            <input
              type="text"
              placeholder="Sweet Name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
            <input
              type="number"
              placeholder="Price"
              value={price}
              onChange={(e) => setPrice(e.target.value)}
              required
            />
            <input
              type="text"
              placeholder="Category"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              required
            />
            <input
              type="number"
              placeholder="Quantity"
              value={quantity}
              onChange={(e) => setQuantity(e.target.value)}
              required
            />
            <button type="submit">Add Sweet</button>
          </form>

          <form onSubmit={(e) => { e.preventDefault(); handleSearch(); }} className="form-container search-form">
            <h3>Search Sweets</h3>
            <input
              type="text"
              placeholder="Search by Name"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
            <input
              type="text"
              placeholder="Search by Category"
              value={searchCategory}
              onChange={(e) => setSearchCategory(e.target.value)}
            />
            <input
              type="number"
              placeholder="Min Price"
              value={minPrice}
              onChange={(e) => setMinPrice(e.target.value)}
            />
            <input
              type="number"
              placeholder="Max Price"
              value={maxPrice}
              onChange={(e) => setMaxPrice(e.target.value)}
            />
            <button type="submit">Search</button>
            <button type="button" onClick={fetchSweets}>Clear Search</button>
          </form>

          {/* Update Sweet Form */}
          {updateId && (
            <form onSubmit={handleUpdateSweet} className="form-container">
              <h3>Update Sweet</h3>
              <input
                type="text"
                value={updateName}
                onChange={(e) => setUpdateName(e.target.value)}
                required
              />
              <input
                type="number"
                value={updatePrice}
                onChange={(e) => setUpdatePrice(e.target.value)}
                required
              />
              <input
                type="text"
                value={updateCategory}
                onChange={(e) => setUpdateCategory(e.target.value)}
                required
              />
              <input
                type="number"
                value={updateQuantity}
                onChange={(e) => setUpdateQuantity(e.target.value)}
                required
              />
              <button type="submit">Update Sweet</button>
              <button type="button" onClick={() => setUpdateId(null)}>Cancel</button>
            </form>
          )}

          {/* Sweets List */}
          <div className="sweets-list-container">
            {sweets.length > 0 ? (
              sweets.map(sweet => (
                <div key={sweet.id} className="sweet-card">
                  <div className="sweet-details">
                    <h3>{sweet.name}</h3>
                    <p>Price: ${sweet.price.toFixed(2)}</p>
                    <p>Category: {sweet.category}</p>
                    <p>Quantity: {sweet.quantity}</p>
                  </div>
                  <div className="sweet-actions">
                    <div className="stock-actions">
                      {/* Purchase button should be visible to all logged-in users */}
                      <button onClick={() => handlePurchase(sweet.id, 1)}>Purchase 1</button>

                      {/* Restock button should only be visible to admin users */}
                      {isAdmin && (
                        <button onClick={() => handleRestock(sweet.id, 1)}>Restock 1</button>
                      )}
                    </div>

                    {/* Delete button should only be visible to admin users */}
                    {isAdmin && (
                      <button onClick={() => handleDeleteSweet(sweet.id)}>Delete</button>
                    )}

                    <button onClick={() => {
                      setUpdateId(sweet.id);
                      setUpdateName(sweet.name);
                      setUpdatePrice(sweet.price);
                      setUpdateCategory(sweet.category);
                      setUpdateQuantity(sweet.quantity);
                    }}>Update</button>
                  </div>
                </div>
              ))
            ) : (
              <p>No sweets available. Please add some!</p>
            )}
          </div>
        </>
      )}
    </div>
  );
}

export default App;