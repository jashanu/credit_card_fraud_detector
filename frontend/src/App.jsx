import { useState } from 'react'
import './App.css'

function App() {
  const [formData, setFormData] = useState({
    amt: '',
    category: 'shopping_net',
    hour: '',
    age: '',
    city_pop: ''
  })
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const categories = [
    'shopping_net', 'misc_net', 'grocery_pos', 'shopping_pos',
    'gas_transport', 'misc_pos', 'grocery_net', 'travel',
    'entertainment', 'personal_care', 'kids_pets', 'food_dining',
    'home', 'health_fitness'
  ]

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await fetch('http://127.0.0.1:8000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          amt: parseFloat(formData.amt),
          category: formData.category,
          hour: parseInt(formData.hour),
          age: parseInt(formData.age),
          city_pop: parseInt(formData.city_pop)
        })
      })

      if (!response.ok) throw new Error('Request failed')

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError('Could not reach the fraud detection API. Is the backend running?')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <h1>Credit Card Fraud Detector</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Amount ($)
          <input type="number" name="amt" value={formData.amt} onChange={handleChange} required />
        </label>

        <label>
          Category
          <select name="category" value={formData.category} onChange={handleChange}>
            {categories.map(cat => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
        </label>

        <label>
          Hour of day (0-23)
          <input type="number" name="hour" min="0" max="23" value={formData.hour} onChange={handleChange} required />
        </label>

        <label>
          Cardholder age
          <input type="number" name="age" value={formData.age} onChange={handleChange} required />
        </label>

        <label>
          City population
          <input type="number" name="city_pop" value={formData.city_pop} onChange={handleChange} required />
        </label>

        <button type="submit" disabled={loading}>
          {loading ? 'Checking...' : 'Check Transaction'}
        </button>
      </form>

      {error && <p className="error">{error}</p>}

      {result && (
        <div className={result.is_fraud ? 'result fraud' : 'result safe'}>
          <h2>{result.is_fraud ? '⚠️ Likely Fraud' : '✅ Looks Normal'}</h2>
          <p>Fraud probability: {(result.fraud_probability * 100).toFixed(1)}%</p>
        </div>
      )}
    </div>
  )
}

export default App