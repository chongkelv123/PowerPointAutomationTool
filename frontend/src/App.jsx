import { useState } from 'react'
import './App.css'
import { pptApi } from './services/api'

function App() {
  const [title, setTitle] = useState('')
  const [slides, setSlides] = useState([{ title: '', content: '' }])
  const [status, setStatus] = useState('')
  const [loading, setLoading] = useState(false)

  const addSlide = () => {
    setSlides([...slides, { title: '', content: '' }])
  }

  const removeSlide = (index) => {
    const newSlides = slides.filter((_, i) => i !== index)
    setSlides(newSlides)
  }

  const updateSlide = (index, field, value) => {
    const newSlides = [...slides]
    newSlides[index][field] = value
    setSlides(newSlides)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setStatus('')

    try {
      const result = await pptApi.createPresentation(title, slides)
      setStatus(`Success! Created: ${result.data.filename}`)
      setTitle('')
      setSlides([{ title: '', content: '' }])
    } catch (error) {
      setStatus(`Error: ${error.message}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <h1>PowerPoint Automation Tool</h1>
      <p className="subtitle">Create presentations quickly and easily</p>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="title">Presentation Title:</label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Enter presentation title"
            required
          />
        </div>

        <div className="slides-section">
          <h2>Slides</h2>
          {slides.map((slide, index) => (
            <div key={index} className="slide-card">
              <div className="slide-header">
                <h3>Slide {index + 1}</h3>
                {slides.length > 1 && (
                  <button
                    type="button"
                    onClick={() => removeSlide(index)}
                    className="btn-remove"
                  >
                    Remove
                  </button>
                )}
              </div>
              <div className="form-group">
                <label htmlFor={`slide-title-${index}`}>Slide Title:</label>
                <input
                  type="text"
                  id={`slide-title-${index}`}
                  value={slide.title}
                  onChange={(e) => updateSlide(index, 'title', e.target.value)}
                  placeholder="Enter slide title"
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor={`slide-content-${index}`}>Content:</label>
                <textarea
                  id={`slide-content-${index}`}
                  value={slide.content}
                  onChange={(e) => updateSlide(index, 'content', e.target.value)}
                  placeholder="Enter slide content"
                  rows="4"
                />
              </div>
            </div>
          ))}
        </div>

        <button type="button" onClick={addSlide} className="btn-secondary">
          + Add Slide
        </button>

        <button type="submit" disabled={loading} className="btn-primary">
          {loading ? 'Creating...' : 'Create Presentation'}
        </button>
      </form>

      {status && (
        <div className={`status ${status.startsWith('Error') ? 'error' : 'success'}`}>
          {status}
        </div>
      )}
    </div>
  )
}

export default App
