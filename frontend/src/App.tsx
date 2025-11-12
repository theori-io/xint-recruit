import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

interface Todo {
  id: string
  title: string
  completed: boolean
  user_id?: string
}

// Configure axios to include auth token
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

function App() {
  const [todos, setTodos] = useState<Todo[]>([])
  const [newTodo, setNewTodo] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [loginLoading, setLoginLoading] = useState(false)

  useEffect(() => {
    const token = localStorage.getItem('auth_token')
    if (token) {
      setIsAuthenticated(true)
      fetchTodos()
    }
  }, [])

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      setLoginLoading(true)
      setError(null)
      const response = await axios.post(`${API_URL}/api/auth/login`, {
        username,
        password,
      })
      localStorage.setItem('auth_token', response.data.access_token)
      setIsAuthenticated(true)
      setUsername('')
      setPassword('')
      await fetchTodos()
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed')
    } finally {
      setLoginLoading(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('auth_token')
    setIsAuthenticated(false)
    setTodos([])
  }

  const fetchTodos = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await axios.get<Todo[]>(`${API_URL}/api/todos`)
      setTodos(response.data)
    } catch (err: any) {
      if (err.response?.status === 401) {
        setError('Session expired. Please login again.')
        handleLogout()
      } else {
        setError('Failed to fetch todos')
      }
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleAddTodo = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!newTodo.trim()) return

    try {
      setError(null)
      const response = await axios.post<Todo>(`${API_URL}/api/todos`, {
        title: newTodo.trim(),
      })
      setTodos([...todos, response.data])
      setNewTodo('')
    } catch (err: any) {
      if (err.response?.status === 401) {
        setError('Session expired. Please login again.')
        handleLogout()
      } else {
        setError('Failed to add todo')
      }
      console.error(err)
    }
  }

  const handleToggleTodo = async (todo: Todo) => {
    try {
      setError(null)
      const response = await axios.put<Todo>(
        `${API_URL}/api/todos/${todo.id}`,
        {
          completed: !todo.completed,
        }
      )
      setTodos(todos.map((t) => (t.id === todo.id ? response.data : t)))
    } catch (err: any) {
      if (err.response?.status === 401) {
        setError('Session expired. Please login again.')
        handleLogout()
      } else {
        setError('Failed to update todo')
      }
      console.error(err)
    }
  }

  const handleDeleteTodo = async (id: string) => {
    try {
      setError(null)
      await axios.delete(`${API_URL}/api/todos/${id}`)
      setTodos(todos.filter((t) => t.id !== id))
    } catch (err: any) {
      if (err.response?.status === 401) {
        setError('Session expired. Please login again.')
        handleLogout()
      } else {
        setError('Failed to delete todo')
      }
      console.error(err)
    }
  }

  if (!isAuthenticated) {
    return (
      <div className="app">
        <div className="container">
          <h1>Todo App</h1>
          <p className="subtitle">Take-Home Assignment</p>
          <p className="subtitle" style={{ fontSize: '0.9rem', marginTop: '0.5rem' }}>
            Test credentials: testuser / testpass123
          </p>

          {error && <div className="error">{error}</div>}

          <form onSubmit={handleLogin} className="todo-form">
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Username"
              className="todo-input"
              required
            />
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Password"
              className="todo-input"
              required
            />
            <button type="submit" className="add-button" disabled={loginLoading}>
              {loginLoading ? 'Logging in...' : 'Login'}
            </button>
          </form>
        </div>
      </div>
    )
  }

  return (
    <div className="app">
      <div className="container">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
          <div>
            <h1>Todo App</h1>
            <p className="subtitle">Take-Home Assignment</p>
          </div>
          <button onClick={handleLogout} className="delete-button" style={{ marginTop: 0 }}>
            Logout
          </button>
        </div>

        {error && <div className="error">{error}</div>}

        <form onSubmit={handleAddTodo} className="todo-form">
          <input
            type="text"
            value={newTodo}
            onChange={(e) => setNewTodo(e.target.value)}
            placeholder="Add a new todo..."
            className="todo-input"
          />
          <button type="submit" className="add-button">
            Add
          </button>
        </form>

        {loading ? (
          <div className="loading">Loading...</div>
        ) : (
          <div className="todo-list">
            {todos.length === 0 ? (
              <div className="empty-state">No todos yet. Add one above!</div>
            ) : (
              todos.map((todo) => (
                <div key={todo.id} className="todo-item">
                  <input
                    type="checkbox"
                    checked={todo.completed}
                    onChange={() => handleToggleTodo(todo)}
                    className="todo-checkbox"
                  />
                  <span
                    className={`todo-title ${todo.completed ? 'completed' : ''}`}
                    dangerouslySetInnerHTML={{ __html: todo.title }}
                  />
                  <button
                    onClick={() => handleDeleteTodo(todo.id)}
                    className="delete-button"
                  >
                    Delete
                  </button>
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default App
