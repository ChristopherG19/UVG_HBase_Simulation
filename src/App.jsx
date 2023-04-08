import './App.css'
import { Route, Routes } from "react-router-dom"

import Login from './routes/Login'
import Menu from './routes/Menu'
import TerminalPage from './routes/Terminal'

const App = () => (

  <div className="App">
    <Routes>
      <Route exact path="/" element = {<Login/>}/>
      <Route exact path="/menu" element = {<Menu/>}/>
      <Route exact path="/terminal" element = {<TerminalPage/>}/>
    </Routes>
  </div>
  
)

export default App