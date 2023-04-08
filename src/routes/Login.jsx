import React from 'react'
import { Link } from 'react-router-dom'

const Login = () => {
  return (
    <div class="h-screen bg-white flex flex-col space-y-10 justify-center items-center">
      <div class="bg-white w-96 shadow-xl rounded p-5">
        <h1 class="text-3xl font-medium">HBase-Simulation</h1>
        <p class="text-sm">Grupo#5<br/>Ma. Isabel Solano 20504<br/>Christopher Garcia 20541</p>
        <br/>
        <Link className="login-button-clickable" to="/menu">
            <button class="text-center w-full bg-blue-900 rounded-md text-white py-3 font-medium">
                Ingresar
            </button>
        </Link>
      </div>
    </div>
  )

}

export default Login
