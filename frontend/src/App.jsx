import { useState } from 'react'
import { pptApi } from './services/api'

function App() {
  const [title, setTitle] = useState('')
  const [slides, setSlides] = useState([{ title: '', content: '', imageFile: null, imageUrl: '' }])
  const [status, setStatus] = useState('')
  const [loading, setLoading] = useState(false)

  const addSlide = () => {
    setSlides([...slides, { title: '', content: '', imageFile: null, imageUrl: '' }])
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

  const handleImageUpload = (index, file) => {
    const newSlides = [...slides]
    newSlides[index].imageFile = file
    newSlides[index].imageUrl = '' // Clear URL if file is selected
    setSlides(newSlides)
  }

  const removeImage = (index) => {
    const newSlides = [...slides]
    newSlides[index].imageFile = null
    newSlides[index].imageUrl = ''
    setSlides(newSlides)
  }

  const convertFileToBase64 = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader()
      reader.readAsDataURL(file)
      reader.onload = () => resolve(reader.result)
      reader.onerror = (error) => reject(error)
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setStatus('')

    try {
      // Process slides to match API format
      const content = await Promise.all(
        slides.map(async (slide) => {
          // Split content by newlines to create bullet points
          const lines = slide.content.trim().split('\n').filter(line => line.trim())

          const slideData = {
            title: slide.title,
            content: {
              bullet_points: lines.length > 0 ? lines : undefined,
            },
          }

          // Handle images
          if (slide.imageFile) {
            const base64 = await convertFileToBase64(slide.imageFile)
            slideData.images = [{
              base64: base64,
              position: {
                left: 5.5,
                top: 2,
                width: 4,
                height: 3.5
              }
            }]
          } else if (slide.imageUrl) {
            slideData.images = [{
              url: slide.imageUrl,
              position: {
                left: 5.5,
                top: 2,
                width: 4,
                height: 3.5
              }
            }]
          }

          return slideData
        })
      )

      const presentationData = {
        title,
        content
      }

      const result = await pptApi.generatePPT(presentationData)
      setStatus(`Success! Your presentation "${result.filename}" has been downloaded.`)

      // Reset form
      setTitle('')
      setSlides([{ title: '', content: '', imageFile: null, imageUrl: '' }])
    } catch (error) {
      setStatus(`Error: ${error.message}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 px-4">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            PowerPoint Automation Tool
          </h1>
          <p className="text-gray-600">
            Create professional presentations quickly and easily
          </p>
        </div>

        <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-lg p-8">
          {/* Presentation Title */}
          <div className="mb-6">
            <label htmlFor="title" className="block text-sm font-semibold text-gray-700 mb-2">
              Presentation Title
            </label>
            <input
              type="text"
              id="title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Enter your presentation title"
              required
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
            />
          </div>

          {/* Slides Section */}
          <div className="mb-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Slides</h2>

            {slides.map((slide, index) => (
              <div key={index} className="mb-6 p-6 bg-gray-50 rounded-lg border border-gray-200">
                <div className="flex justify-between items-center mb-4">
                  <h3 className="text-lg font-medium text-gray-700">Slide {index + 1}</h3>
                  {slides.length > 1 && (
                    <button
                      type="button"
                      onClick={() => removeSlide(index)}
                      className="px-3 py-1 bg-red-500 text-white rounded-md hover:bg-red-600 transition text-sm"
                    >
                      Remove
                    </button>
                  )}
                </div>

                <div className="space-y-4">
                  {/* Slide Title */}
                  <div>
                    <label htmlFor={`slide-title-${index}`} className="block text-sm font-medium text-gray-700 mb-2">
                      Slide Title
                    </label>
                    <input
                      type="text"
                      id={`slide-title-${index}`}
                      value={slide.title}
                      onChange={(e) => updateSlide(index, 'title', e.target.value)}
                      placeholder="Enter slide title"
                      required
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>

                  {/* Slide Content */}
                  <div>
                    <label htmlFor={`slide-content-${index}`} className="block text-sm font-medium text-gray-700 mb-2">
                      Content (one bullet point per line)
                    </label>
                    <textarea
                      id={`slide-content-${index}`}
                      value={slide.content}
                      onChange={(e) => updateSlide(index, 'content', e.target.value)}
                      placeholder="Enter slide content&#10;Each line will be a bullet point&#10;Like this"
                      rows="4"
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>

                  {/* Image Upload */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Image (optional)
                    </label>

                    {!slide.imageFile && !slide.imageUrl && (
                      <div className="flex gap-4">
                        <div className="flex-1">
                          <input
                            type="file"
                            accept="image/*"
                            onChange={(e) => handleImageUpload(index, e.target.files[0])}
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          />
                          <p className="text-xs text-gray-500 mt-1">Upload from your computer</p>
                        </div>
                        <div className="flex-1">
                          <input
                            type="url"
                            value={slide.imageUrl}
                            onChange={(e) => updateSlide(index, 'imageUrl', e.target.value)}
                            placeholder="https://example.com/image.jpg"
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          />
                          <p className="text-xs text-gray-500 mt-1">Or paste an image URL</p>
                        </div>
                      </div>
                    )}

                    {slide.imageFile && (
                      <div className="flex items-center gap-3 p-3 bg-blue-50 rounded-lg border border-blue-200">
                        <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                        <span className="text-sm text-gray-700 flex-1">{slide.imageFile.name}</span>
                        <button
                          type="button"
                          onClick={() => removeImage(index)}
                          className="text-red-600 hover:text-red-800 text-sm font-medium"
                        >
                          Remove
                        </button>
                      </div>
                    )}

                    {slide.imageUrl && !slide.imageFile && (
                      <div className="flex items-center gap-3 p-3 bg-blue-50 rounded-lg border border-blue-200">
                        <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
                        </svg>
                        <span className="text-sm text-gray-700 flex-1 truncate">{slide.imageUrl}</span>
                        <button
                          type="button"
                          onClick={() => removeImage(index)}
                          className="text-red-600 hover:text-red-800 text-sm font-medium"
                        >
                          Remove
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}

            <button
              type="button"
              onClick={addSlide}
              className="w-full py-3 px-4 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition font-medium border-2 border-dashed border-gray-300"
            >
              + Add Another Slide
            </button>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className={`w-full py-4 px-6 rounded-lg font-semibold text-white transition-all ${
              loading
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700 transform hover:scale-[1.02]'
            }`}
          >
            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Generating Presentation...
              </span>
            ) : (
              'Generate PowerPoint'
            )}
          </button>
        </form>

        {/* Status Message */}
        {status && (
          <div
            className={`mt-6 p-4 rounded-lg border ${
              status.startsWith('Error')
                ? 'bg-red-50 border-red-200 text-red-800'
                : 'bg-green-50 border-green-200 text-green-800'
            }`}
          >
            <div className="flex items-start gap-3">
              {status.startsWith('Error') ? (
                <svg className="w-5 h-5 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              ) : (
                <svg className="w-5 h-5 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              )}
              <p className="text-sm font-medium">{status}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
