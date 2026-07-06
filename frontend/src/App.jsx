import {useState, useEffect} from 'react'
import './App.css'

export default function App(){
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const [barcode, setBarcode] = useState('')
  const [inStock, setInStock] = useState('')
  const [price, setPrice] = useState('')
  const [formError, setFormError] = useState(null)

  const fetchItems = () => {
    setLoading(true)
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
  }

  /* Fetch the items when the component mounts */
  useEffect(() => {
    fetchItems()
  }, [])

  const handleSubmit = (e) => {
    e.preventDefault()
    setFormError(null)

    fetch('/api/inventory', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        barcode,
        in_stock: Number(inStock, 10),
        price: Number(price),
      }),
    })
      .then((response) => {
        if(!response.ok){
          return response.json().then((data) => {
            throw new Error(data.error || 'Failed to add item')
          })
        }
        return response.json()
      })
      .then((data) => {
        setBarcode('')
        setInStock('')
        setPrice('')
        fetchItems()
      })
      .catch((error) => {
        setFormError(error.message)
      })
  }

  if (loading) {
    return <div>Loading Inventory...</div>
  }

  if (error) {
    return <div>Error: {error.message}</div>
  }

  return (
    <div>
      <h1>Inventory</h1>
      <form onSubmit={handleSubmit}>
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
              {item.name} <br /> -brand: {item.brand} <br /> - ingredients: {item.ingredients} <br /> - price: ${item.price} <br /> - stock: {item.in_stock}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}