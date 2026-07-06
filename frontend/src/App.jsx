import {useState, useEffect} from 'react'
import './App.css'

export default function App(){
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch('/api/inventory')
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok')
        }
        return response.json()
      })
      .then((data) => {
        setItems(data)
        setLoading(false)
      })
      .catch((error) => {
        setError(error)
        setLoading(false)
      })
  }, [])

  if (loading) {
    return <div>Loading Inventory...</div>
  }

  if (error) {
    return <div>Error: {error.message}</div>
  }

  return (
    <div>
      <h1>Inventory</h1>
      <form>
        <input 
          type="text"
          placeholder="Barcode"
          value={barcode}
          onChange={(e) => setBarcode(e.target.value)}
          required 
        />
        <input
          type="number"
          placeholder="Quantity"
          value={inStock}
          onChange={(e) => setInStock(e.target.value)}
          required
        />
        <input 
          type="number"
          step="0.01"
          placeholder="Price"
          value={price}
          onChange={(e) => setPrice(e.target.value)}
          required
        />
        <button type="submit">Add Item</button>
      </form>
      {formError && <p style={{ color: 'red' }}>{formError}</p>}
      {items.length === 0 ? (
        <p>No items found in the inventory.</p>
      ) : (
        <ul>
          {items.map((item) => (
            <li key={item.id}>
              {item.name} - {item.brand} - {item.price} - Stock: {item.in_stock}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}